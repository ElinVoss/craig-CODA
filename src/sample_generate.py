from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM

from .checkpoint_utils import latest_checkpoint
from .io_utils import write_json, write_text
from .memory.retrieve_topk import retrieve_nodes
from .runtime.front_matter_builder import build_prompt_front_matter
from .runtime.prompt_compiler import compile_mode_prompt
from .runtime.response_plan_builder import build_response_plan
from .translation.runtime_context_translator import build_memory_context, render_memory_context
from .tokenizer_loader import load_tokenizer

ROOT = Path(__file__).resolve().parents[1]


def generate_text(model, tokenizer, prompt: str, max_new_tokens: int, temperature: float, top_k: int, device: torch.device) -> str:
    encoded = tokenizer(prompt, return_tensors="pt")
    input_ids = encoded["input_ids"].to(device)
    attention_mask = encoded["attention_mask"].to(device) if "attention_mask" in encoded else None
    with torch.no_grad():
        output_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_k=top_k,
            pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)


def load_model_for_generation(checkpoint_root: str | Path | None = None):
    if checkpoint_root is None:
        checkpoint_root = ROOT / "artifacts" / "checkpoints" / "tiny-qwen3-scratch"
    root = Path(checkpoint_root)
    if not root.is_absolute():
        root = ROOT / root
    checkpoint = latest_checkpoint(root)
    if checkpoint is None:
        raise FileNotFoundError(f"No checkpoints found in {root}")
    model = AutoModelForCausalLM.from_pretrained(checkpoint)
    return model, checkpoint


def maybe_build_memory_context(
    prompt: str,
    retrieval_profile: str,
    mode_name: str,
    top_k: int,
    disabled: bool = False,
) -> str | None:
    if disabled:
        return None
    try:
        results = retrieve_nodes(
            query=prompt,
            retrieval_profile=retrieval_profile,
            mode=mode_name,
            top_k=top_k,
        )
    except FileNotFoundError:
        return None
    if not results:
        return None
    return render_memory_context(build_memory_context(results))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local sample generation from a saved checkpoint.")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--mode", default="craig_default")
    parser.add_argument("--include-context", action="store_true")
    parser.add_argument("--rs1-specialty", action="store_true")
    parser.add_argument("--rs1-creative", action="store_true")
    parser.add_argument("--checkpoint-root", default=str(ROOT / "artifacts" / "checkpoints" / "tiny-qwen3-scratch"))
    parser.add_argument("--tokenizer-dir", default=str(ROOT / "artifacts" / "tokenizers" / "default"))
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=0.9)
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--retrieval-profile", default=None)
    parser.add_argument("--memory-top-k", type=int, default=None)
    parser.add_argument("--disable-memory", action="store_true")
    args = parser.parse_args()

    tokenizer, _ = load_tokenizer(args.tokenizer_dir)
    model, checkpoint = load_model_for_generation(args.checkpoint_root)
    device = torch.device("cpu")
    model.to(device)
    model.eval()

    front_matter = build_prompt_front_matter(args.prompt, overrides={"mode": args.mode})
    response_plan = build_response_plan(
        front_matter=front_matter,
        mode_name=args.mode,
        include_context=args.include_context,
        include_rs1_specialty=args.rs1_specialty,
        include_rs1_creative=args.rs1_creative,
        retrieval_profile=args.retrieval_profile,
        memory_top_k=args.memory_top_k,
    )
    memory_context = maybe_build_memory_context(
        prompt=args.prompt,
        retrieval_profile=response_plan.retrieval_profile,
        mode_name=response_plan.selected_mode,
        top_k=response_plan.memory_top_k,
        disabled=args.disable_memory or not response_plan.include_memory_context,
    )
    system_prompt, included_files = compile_mode_prompt(
        mode_name=response_plan.selected_mode,
        include_context=response_plan.include_context,
        include_rs1_specialty=response_plan.include_rs1_specialty,
        include_rs1_creative=response_plan.include_rs1_creative,
        memory_context=memory_context,
    )
    composed_prompt = f"System:\n{system_prompt}\n\nUser:\n{args.prompt}\n\nAssistant:\n"
    text = generate_text(
        model=model,
        tokenizer=tokenizer,
        prompt=composed_prompt,
        max_new_tokens=int(args.max_new_tokens),
        temperature=float(args.temperature),
        top_k=int(args.top_k),
        device=device,
    )

    output_dir = ROOT / "artifacts" / "samples"
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    write_text(output_dir / f"sample_{stamp}.txt", text + "\n")
    write_json(
        output_dir / f"sample_{stamp}.json",
        {
            "checkpoint": str(checkpoint),
            "mode": response_plan.selected_mode,
            "included_files": [str(path) for path in included_files],
            "prompt": args.prompt,
            "front_matter": front_matter.to_dict(),
            "response_plan": response_plan.to_dict(),
            "memory_context": memory_context,
            "output": text,
        },
    )
    print(f"Loaded checkpoint: {checkpoint}")
    print(f"Wrote sample to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
