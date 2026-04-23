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

## Phase three tokenizer pipeline

Phase three adds a local corpus-prep and tokenizer-training flow. This creates a reusable tokenizer artifact from the cleaned corpus. It does not train a model.

### What it does

- assembles a deterministic prepared corpus from cleaned text in `data/clean/`
- trains a local tokenizer with the Hugging Face `tokenizers` library
- writes tokenizer artifacts and simple diagnostics under `artifacts/`
- validates that the tokenizer can be loaded and used for sample encode/decode checks

### New artifact locations

- `artifacts/corpus/prepared_corpus.txt`: prepared tokenizer corpus
- `artifacts/corpus/prepared_corpus_manifest.json`: source manifest for the prepared corpus
- `artifacts/reports/corpus_prep_report.txt`: corpus prep summary
- `artifacts/tokenizers/default/tokenizer.json`: trained tokenizer
- `artifacts/tokenizers/default/tokenizer_config.json`: tokenizer config snapshot
- `artifacts/tokenizers/default/special_tokens_map.json`: special token listing
- `artifacts/tokenizers/default/training_info.json`: training metadata
- `artifacts/reports/tokenizer_report.txt`: human-readable inspection report
- `artifacts/reports/tokenizer_report.json`: structured inspection report

### Prepare and train the tokenizer

From the repo root:

```powershell
python .\scripts\run_tokenizer_pipeline.py
```

That runs:

1. `scripts/prepare_corpus.py`
2. `scripts/train_tokenizer.py`
3. `scripts/inspect_tokenizer.py`
4. `scripts/validate_data.py`

### Dependency note

Phase three adds one lightweight dependency:

- `tokenizers` for local tokenizer training and loading

### Important limitation

The tokenizer is only a local segmentation artifact. It is not a trained language model and it does not imply any semantic capability by itself.

## Phase four tiny scratch model

Phase four adds a tiny scratch-built causal language model path that uses the Hugging Face Qwen3 architecture family through `Qwen3Config` and `AutoModelForCausalLM.from_config(...)`.

This phase does not use pretrained checkpoints. The model initializes from random weights and is intentionally much smaller than any official Qwen3 release.

### What phase four adds

- tokenizer loading from the phase-three artifacts
- tiny Qwen3-style model construction from config
- scratch pretraining on the prepared local corpus
- SFT dataset validation scaffold for later behavior shaping
- runtime prompt compilation from the local user-model bundle
- local sample generation
- lightweight evaluation runner

### New artifact locations

- `artifacts/models/`: model metadata and initialized-model outputs
- `artifacts/checkpoints/`: scratch-training checkpoints
- `artifacts/samples/`: local generation outputs
- `artifacts/eval_reports/`: eval reports

### Key configs

- `configs/model_architecture.yaml`
- `configs/training_scratch.yaml`
- `configs/training_sft.yaml`
- `configs/runtime_modes.yaml`
- `configs/eval.yaml`

### Dependency note

Phase four adds:

- `torch` for local model execution and training
- `transformers` for `Qwen3Config`, model construction, generation, and tokenizer integration
- `safetensors` for model checkpoint serialization
- `tqdm` for lightweight progress support

### Inspect the setup

```powershell
python .\scripts\inspect_model.py
```

This prints:

- tokenizer location
- vocab size
- tiny model summary
- parameter count
- context length
- current checkpoint directories if any

### Run scratch training

```powershell
python .\scripts\run_scratch_train.py
```

This uses:

- tokenizer artifacts from `artifacts/tokenizers/default/`
- prepared corpus from `artifacts/corpus/prepared_corpus.txt`
- random model initialization from `Qwen3Config`
- CPU-first defaults from `configs/training_scratch.yaml`

### Run sample generation

After at least one checkpoint exists:

```powershell
python .\scripts\run_sample_generation.py --prompt "Summarize the local-first constraints." --mode craig_default
```

You can also test fiction routing and overlays:

```powershell
python .\scripts\run_sample_generation.py --prompt "Write a short Te'Oga opening." --mode elin_fiction
python .\scripts\run_sample_generation.py --prompt "Explain the brittle-system failure mode." --mode craig_default --rs1-specialty
```

### Run evals

After at least one checkpoint exists:

```powershell
python .\scripts\run_eval_suite.py
```

This writes reports under `artifacts/eval_reports/`.

### SFT path

The SFT path is intentionally a scaffold in this phase:

```powershell
python .\scripts\run_sft_train.py
```

It validates the expected dataset schema and keeps the later behavior-shaping path explicit, but it does not claim a full tuned SFT recipe yet.

### Runtime prompt modes

The runtime compiler uses the local bundle structure and supports:

- `craig_default`
- `elin_fiction`
- optional `rs1_specialty` overlay

It will not auto-load `review_before_use/` or other forbidden paths.

### Important limitations

- This is not official Qwen3.
- No official Qwen3 weights are used.
- The model is tiny and randomly initialized.
- CPU-first defaults mean the training loop is for local experimentation, not scale.
- Early outputs may be weak or nonsensical until enough local training happens.

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

- inference serving
- checkpoint management logic beyond folders
- dataset downloaders
- cloud APIs
- Docker or container workflows
- GPU-specific code paths
- notebook-driven workflow automation
 - distributed training
 - pretrained checkpoint loading
 - full SFT recipe

## Raw file handling notes

- The pipeline never modifies files in `data/raw/` directly.
- Ingestion creates staged copies in `data/raw/_ingested/`.
- Cleaning and dataset building operate on staged copies, not the originals.
