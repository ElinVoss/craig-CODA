from __future__ import annotations

import argparse
from pathlib import Path

import torch
import yaml
from transformers import AutoModelForCausalLM

from ..checkpoint_utils import latest_checkpoint
from ..io_utils import write_json, write_text
from ..runtime.prompt_compiler import compile_mode_prompt
from ..sample_generate import generate_text
from ..tokenizer_loader import load_tokenizer
from .eval_utils import load_eval_records, render_eval_text_report, run_automatic_checks

ROOT = Path(__file__).resolve().parents[2]


def load_eval_config(config_path: str | Path | None = None) -> dict:
    if config_path is None:
        config_path = ROOT / "configs" / "eval.yaml"
    path = Path(config_path)
    if not path.is_absolute():
        path = ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def run_eval_suite(config_path: str | Path | None = None) -> dict:
    config = load_eval_config(config_path)
    tokenizer, _ = load_tokenizer(config["tokenizer_dir"])
    checkpoint_root = Path(config["checkpoint_dir"])
    if not checkpoint_root.is_absolute():
        checkpoint_root = ROOT / checkpoint_root
    checkpoint = latest_checkpoint(checkpoint_root)
    if checkpoint is None:
        raise FileNotFoundError(f"No checkpoints found in {checkpoint_root}")

    model = AutoModelForCausalLM.from_pretrained(checkpoint)
    device = torch.device("cpu")
    model.to(device)
    model.eval()

    dataset_paths = []
    for item in config["datasets"]:
        path = Path(item["path"])
        if not path.is_absolute():
            path = ROOT / path
        dataset_paths.append(path)

    records = load_eval_records(dataset_paths, int(config["sample_count"]))
    system_prompt, included_files = compile_mode_prompt(mode_name=config["generation"]["mode"])

    results: list[dict] = []
    for record in records:
        prompt = record.get("question") or record.get("prompt") or record.get("input") or ""
        full_prompt = f"System:\n{system_prompt}\n\nUser:\n{prompt}\n\nAssistant:\n"
        output = generate_text(
            model=model,
            tokenizer=tokenizer,
            prompt=full_prompt,
            max_new_tokens=int(config["generation"]["max_new_tokens"]),
            temperature=float(config["generation"]["temperature"]),
            top_k=int(config["generation"]["top_k"]),
            device=device,
        )
        result = dict(record)
        result["output"] = output
        result["included_prompt_files"] = [str(path) for path in included_files]
        result.update(run_automatic_checks(record, output))
        results.append(result)

    report_json = Path(config["output_report_json"])
    report_text = Path(config["output_report_text"])
    if not report_json.is_absolute():
        report_json = ROOT / report_json
    if not report_text.is_absolute():
        report_text = ROOT / report_text
    write_json(report_json, {"checkpoint": str(checkpoint), "results": results})
    write_text(report_text, render_eval_text_report(results))
    return {"checkpoint": str(checkpoint), "result_count": len(results), "report_json": str(report_json)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local evaluation suite against a saved checkpoint.")
    parser.add_argument("--config", default=str(ROOT / "configs" / "eval.yaml"))
    args = parser.parse_args()

    summary = run_eval_suite(args.config)
    print(f"Evaluation complete using {summary['checkpoint']}")
    print(f"Report written to {summary['report_json']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

