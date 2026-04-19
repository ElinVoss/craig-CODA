# model-lab

`model-lab` is a local, CPU-first workspace for building and evaluating small AI systems on Windows without cloud dependencies.

It is organized around two tracks that share one data core:

- Teach-a-model track: collect examples, corrections, ranked preferences, and eval cases for adapting an existing model later.
- Originate-a-model track: prepare a small from-scratch model workflow using local datasets and experiments later.

This repository is the foundation for both tracks. It does not yet include training code.

## What is in this repo

- Standard folder layout for raw data, cleaned data, supervised fine-tuning data, preference data, pretraining text, and eval data.
- Lightweight config files that define the project, schema expectations, and runtime defaults.
- Bootstrap and validation scripts for Windows.
- Small sample data files that show the expected formats.

## Folder structure

```text
model-lab/
  configs/         Project, schema, and runtime configuration
  data/            Shared local data core
  scripts/         Bootstrap and validation helpers
  src/             Future Python package code
  notebooks/       Optional local exploration notebooks
  logs/            Runtime logs
  checkpoints/     Local model checkpoints and artifacts
  exports/         Exported datasets, reports, and deliverables
```

## Data folders

- `data/raw/`: original source material as captured locally
- `data/clean/`: cleaned or normalized versions of raw data
- `data/sft/`: supervised fine-tuning examples
- `data/prefs/`: ranked preference or comparison records
- `data/pretrain/`: plain-text corpora for future from-scratch experiments
- `data/eval/`: evaluation cases and expected characteristics

## Windows setup

### 1. Create a virtual environment

From `D:\model-lab`:

```powershell
python -m venv .venv
```

### 2. Activate it

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the venv again.

### 3. Install requirements

```powershell
pip install -r requirements.txt
```

## Bootstrap

You can create the expected folders and a venv with:

```powershell
.\scripts\bootstrap.ps1
```

The script is conservative. It does not install heavy packages.

## Validate the sample data

Run:

```powershell
python .\scripts\validate_data.py
```

This checks required folders and validates the sample JSONL files against the current schema family.

## Next milestone

The next milestone is to define local data ingestion and curation flows for:

- capturing teach-a-model examples
- recording preferences and corrections
- preparing eval cases
- preparing a small pretraining corpus

Only after those data formats and eval flows are stable should training code be added.

## Intentionally not implemented yet

- model training
- inference serving
- checkpoint management logic beyond folders
- dataset downloaders
- cloud APIs
- Docker or container workflows
- GPU-specific code paths
- notebook-driven workflow automation

