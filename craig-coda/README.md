# CODA

> Audit. Consolidate. Prune. Disappear.

CODA is a CLI agent tool that manages the artifact space of Craig-CODA.  
It has full read/write access to everything. It never asks permission.  
It checkpoints before every action and logs everything it does.

---

## Install

```bash
git clone <repo>
cd coda
npm install commander
npm link          # makes `coda` available globally
```

---

## Commands

```
coda audit              Walk the target and score every artifact
coda plan               Build a consolidation plan from the last audit
coda prune              Execute the plan (checkpoints first)
coda status             Show storage used, audit age, graduation readiness
coda graduation         Run the graduation check
coda rollback           Restore the most recent checkpoint
```

---

## The Contract

| Property | Value |
|---|---|
| Access | All tools, all read, all write |
| Asks permission | **Never** |
| Storage hard limit | 500 GB |
| Graduation | Self-declared |
| Graduation test | States your best memory — unprompted |
| If it asks | It isn't done. Keep running. |
| Final judge | Craig alone |
| Last thing CODA prunes | Itself |

---

## Prune Order

1. Orphaned scaffolding
2. Donor identity residue
3. Redundant vault duplicates
4. Low-centrality lore fragments
5. Contested artifacts (after skeptic second-pass clears them)
6. **CODA's own bootstrap layer — last of all**

---

## Graduation Condition

CODA knows it's done when it can tell Craig what his best memory is —  
**without being asked.**

- If it asks → it isn't done. Keep running.
- If it answers → Craig confirms or denies.
- If confirmed → CODA prunes itself and exits.

---

## Configuration

Edit `src/config.js` or set environment variables:

```bash
CODA_TARGET=/path/to/your/vault    # what to audit
CODA_LIMIT_BYTES=536870912000      # storage limit (default 500 GB)
```

---

## Architecture

```
coda/
├── src/
│   ├── cli.js          ← entry point, Commander routing
│   ├── config.js       ← all constants and env vars
│   ├── auditor.js      ← filesystem scan + relevance scoring
│   ├── planner.js      ← consolidation logic (ported from planning.js)
│   ├── skeptic.js      ← second-pass self-distrust layer
│   ├── executor.js     ← prune execution + checkpoint/rollback
│   ├── graduation.js   ← graduation condition loop
│   ├── status.js       ← status display
│   └── logger.js       ← append-only action log
├── checkpoint/         ← rollback states (one per execution cycle)
├── coda.log            ← immutable append-only action log
└── README.md
```
