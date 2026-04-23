from __future__ import annotations

import json
from pathlib import Path

from ..io_utils import read_jsonl


def load_eval_records(paths: list[Path], sample_count: int) -> list[dict]:
    records: list[dict] = []
    for path in paths:
        if not path.is_file():
            continue
        items = read_jsonl(path)
        for item in items:
            item["_source_path"] = str(path)
        records.extend(items)
    if sample_count > 0:
        return records[:sample_count]
    return records


def run_automatic_checks(record: dict, output_text: str) -> dict:
    lowered = output_text.lower()
    result = {"automatic_status": "manual", "notes": []}

    if "required" in record:
        required = [token.lower() for token in record["required"]]
        passed = all(token in lowered for token in required)
        result["automatic_status"] = "pass" if passed else "fail"
        if not passed:
            result["notes"].append("Missing one or more required substrings")
        return result

    if "required_any" in record:
        groups = record["required_any"]
        passed = any(all(token.lower() in lowered for token in group) for group in groups)
        result["automatic_status"] = "pass" if passed else "fail"
        if not passed:
            result["notes"].append("No required_any group matched")
        return result

    if "correct_answer" in record:
        passed = record["correct_answer"].strip().lower() in lowered
        result["automatic_status"] = "pass" if passed else "fail"
        return result

    if "pass_signals" in record:
        signals = [signal.lower() for signal in record["pass_signals"]]
        fails = [signal for signal in signals if signal not in lowered]
        result["automatic_status"] = "pass" if not fails else "manual"
        if fails:
            result["notes"].append("Some pass signals were not found automatically")
        for fail_signal in record.get("fail_signals", []):
            if fail_signal.lower() in lowered:
                result["automatic_status"] = "fail"
                result["notes"].append(f"Found fail signal: {fail_signal}")
        return result

    return result


def render_eval_text_report(results: list[dict]) -> str:
    lines = ["Evaluation report", ""]
    for item in results:
        lines.append(f"- id: {item['id']}")
        lines.append(f"  source: {item['_source_path']}")
        lines.append(f"  automatic_status: {item['automatic_status']}")
        lines.append(f"  output_preview: {item['output'][:120]}")
    return "\n".join(lines) + "\n"

