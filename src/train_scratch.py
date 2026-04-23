from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

import torch
import yaml

from .checkpoint_utils import latest_checkpoint, save_checkpoint, trim_old_checkpoints
from .io_utils import read_text, write_json
from .model_factory import build_model
from .sample_generate import generate_text
from .tokenizer_loader import load_tokenizer

ROOT = Path(__file__).resolve().parents[1]


def load_training_config(config_path: str | Path | None = None) -> dict:
    if config_path is None:
        config_path = ROOT / "configs" / "training_scratch.yaml"
    path = Path(config_path)
    if not path.is_absolute():
        path = ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


def tokenize_corpus(tokenizer, corpus_path: Path) -> torch.Tensor:
    text = read_text(corpus_path)
    encoded = tokenizer(text, add_special_tokens=False, return_attention_mask=False)
    input_ids = encoded["input_ids"]
    if len(input_ids) < 4:
        raise ValueError(f"{corpus_path} is too small for causal LM training")
    return torch.tensor(input_ids, dtype=torch.long)


def sample_batch(token_ids: torch.Tensor, batch_size: int, block_size: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
    max_start = token_ids.numel() - block_size - 1
    if max_start <= 0:
        raise ValueError("Tokenized corpus is shorter than block_size + 1")
    starts = torch.randint(0, max_start, (batch_size,))
    inputs = torch.stack([token_ids[start : start + block_size] for start in starts])
    labels = torch.stack([token_ids[start + 1 : start + block_size + 1] for start in starts])
    return inputs.to(device), labels.to(device)


def train(config_path: str | Path | None = None, resume_from: str | Path | None = None) -> dict:
    import json as _json
    config = load_training_config(config_path)
    set_seed(int(config["seed"]))

    tokenizer, tokenizer_meta = load_tokenizer(config["tokenizer_dir"])
    model, _, model_summary = build_model()
    device = torch.device(str(config["device_preference"]))
    model.to(device)
    model.train()

    corpus_path = Path(config["corpus_path"])
    if not corpus_path.is_absolute():
        corpus_path = ROOT / corpus_path
    token_ids = tokenize_corpus(tokenizer, corpus_path)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=float(config["learning_rate"]),
        betas=(float(config["adam_beta1"]), float(config["adam_beta2"])),
        eps=float(config["adam_eps"]),
        weight_decay=float(config["weight_decay"]),
    )

    output_dir = Path(config["output_dir"])
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    start_step = 0
    if resume_from is not None:
        from transformers import AutoModelForCausalLM
        resume_path = Path(resume_from)
        if not resume_path.is_absolute():
            resume_path = ROOT / resume_path
        print(f"Resuming from {resume_path}")
        model = AutoModelForCausalLM.from_pretrained(str(resume_path))
        model.to(device)
        model.train()
        opt_path = resume_path / "optimizer.pt"
        if opt_path.exists():
            optimizer.load_state_dict(torch.load(opt_path, map_location=device, weights_only=True))
        state_path = resume_path / "trainer_state.json"
        if state_path.exists():
            state = _json.loads(state_path.read_text())
            start_step = int(state.get("step", 0))
        print(f"Continuing from step {start_step}")

    losses: list[float] = []
    last_checkpoint: str | None = None
    log_path = output_dir / "training_log.jsonl"
    for step in range(start_step + 1, start_step + int(config["max_steps"]) + 1):
        running_loss = 0.0
        optimizer.zero_grad(set_to_none=True)
        for _ in range(int(config["gradient_accumulation_steps"])):
            inputs, labels = sample_batch(
                token_ids,
                int(config["batch_size"]),
                int(config["block_size"]),
                device,
            )
            outputs = model(input_ids=inputs, labels=labels)
            loss = outputs.loss / int(config["gradient_accumulation_steps"])
            loss.backward()
            running_loss += float(loss.item())
        optimizer.step()
        losses.append(running_loss)

        if step % int(config["log_interval"]) == 0 or step == 1:
            print(f"step={step} loss={running_loss:.4f}", flush=True)
            with open(log_path, "a", encoding="utf-8") as lf:
                import json as _json
                lf.write(_json.dumps({"step": step, "loss": round(running_loss, 6),
                                      "max_steps": int(config["max_steps"])}) + "\n")

        if step % int(config["checkpoint_interval"]) == 0 or step == int(config["max_steps"]):
            ckpt_dir = output_dir / f"step_{step:04d}"
            trainer_state = {
                "step": step,
                "loss": running_loss,
                "avg_loss": sum(losses) / len(losses),
                "model_summary": model_summary,
                "tokenizer_dir": tokenizer_meta["tokenizer_dir"],
            }
            save_checkpoint(model, tokenizer, optimizer, ckpt_dir, trainer_state)
            trim_old_checkpoints(output_dir, int(config["max_checkpoints"]))
            last_checkpoint = str(ckpt_dir)
            print(f"Saved checkpoint to {ckpt_dir}")

        if step % int(config["sample_interval"]) == 0 or step == int(config["max_steps"]):
            sample_text = generate_text(
                model=model,
                tokenizer=tokenizer,
                prompt=str(config["sample_prompt"]),
                max_new_tokens=24,
                temperature=0.9,
                top_k=20,
                device=device,
            )
            print(f"sample[{step}]: {sample_text}")

    summary = {
        "steps_completed": int(config["max_steps"]),
        "final_loss": losses[-1] if losses else None,
        "avg_loss": sum(losses) / len(losses) if losses else None,
        "last_checkpoint": last_checkpoint,
        "token_count": int(token_ids.numel()),
    }
    write_json(output_dir / "run_summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run scratch pretraining for the tiny Qwen3-style model.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "training_scratch.yaml"))
    parser.add_argument("--resume", default=None, help="Checkpoint dir to resume from")
    args = parser.parse_args()

    summary = train(args.config, resume_from=args.resume)
    print(f"Training complete. Last checkpoint: {summary['last_checkpoint']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

