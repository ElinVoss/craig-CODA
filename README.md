# model-lab

`model-lab` is a local, CPU-first workspace for building and evaluating small AI systems on Windows without cloud dependencies.

It is organized around two tracks that share one data core:

- Teach-a-model track: collect examples, corrections, ranked preferences, and eval cases for adapting an existing model later.
- Originate-a-model track: prepare a small from-scratch model workflow using local datasets and experiments later.

This repository is the foundation for both tracks. It does not yet include training code.

Phase two adds a simple, local ingestion and dataset-prep pipeline that turns raw text-like files into cleaned text and placeholder dataset outputs.

## What is in this repo

- Standard folder layout for raw data, cleaned data, supervised fine-tuning data, preference data, pretraining text, and eval data.
- Lightweight config files that define the project, schema expectations, and runtime defaults.
- Bootstrap and validation scripts for Windows.
- Small sample data files that show the expected formats.
- A conservative local pipeline for ingesting, cleaning, and building placeholder datasets.

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
- `data/raw/examples/`: tiny example inputs used to smoke-test the pipeline
- `data/raw/_ingested/`: staged copies of raw files created by the ingestion step
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

## Phase two pipeline

The pipeline is intentionally simple and rule-based. It does not label data intelligently. It only prepares outputs from local text using clear heuristics.

### Supported raw inputs

- `.txt`
- `.md`
- `.jsonl` treated as plain text in this phase

Unsupported file types are ignored safely.

### Place raw files

Put source files in `data/raw/` or a subfolder like `data/raw/examples/`.
Do not overwrite raw source files with cleaned outputs.

### Run the full pipeline

```powershell
python .\scripts\run_pipeline.py
```

This runs:

1. ingest raw files into `data/raw/_ingested/`
2. clean text into `data/clean/`
3. build placeholder dataset outputs
4. validate the results

### Output folders after phase two

- `data/clean/`: conservative cleaned text artifacts, one per staged input
- `data/pretrain/`: assembled plain-text corpus for future pretraining work
- `data/sft/`: rule-based supervised examples generated from cleaned text
- `data/prefs/`: rule-based preference pairs generated from cleaned text
- `data/eval/`: rule-based eval cases generated from cleaned text

Generated SFT, preference, and eval files are placeholders. They are traceable to source files, but they are not semantic labels from a real annotator or model.

## Validate the sample data

Run:

```powershell
python .\scripts\validate_data.py
```

This checks required folders and validates the sample JSONL files against the current schema family.

You can also validate generated outputs after running the pipeline with the same script.

## Next milestone

The next milestone is to define local data ingestion and curation flows for:

- capturing teach-a-model examples
- recording preferences and corrections
- preparing eval cases
- preparing a small pretraining corpus

Only after those data formats and eval flows are stable should training code be added.

## Intentionally not implemented yet

- model training
- tokenizer training
- inference serving
- checkpoint management logic beyond folders
- dataset downloaders
- cloud APIs
- Docker or container workflows
- GPU-specific code paths
- notebook-driven workflow automation

## Raw file handling notes

- The pipeline never modifies files in `data/raw/` directly.
- Ingestion creates staged copies in `data/raw/_ingested/`.
- Cleaning and dataset building operate on staged copies, not the originals.
