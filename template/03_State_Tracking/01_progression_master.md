# {{PROJECT_NAME}} — Progression Master Ledger

**Status**: LIVE — updated after every output unit is generated.
**Purpose**: Single source of truth for all state changes across the entire project arc.
**Rule**: Any state recorded here is permanent. No retcons without explicit cause logged here.

---

## HOW TO USE

After generating each output unit:
1. Record all state changes in the relevant section below.
2. Run `tools/build_knowledge_index.py` to update SHA pins.
3. Commit with message: `STATE: Update progression after {{OUTPUT_UNIT}} N{{N}}`

---

## STATE DIMENSIONS

*(Define the dimensions of state your project tracks. Examples below.)*

### {{STATE_DIMENSION_1}}
*(e.g. "Character Arc", "System Capacity", "Crisis Level", "Relationship Status")*

| After Output N | State | Notes |
|---|---|---|
| N01 | {{INITIAL_STATE}} | Baseline established |
| N02 | {{STATE_N02}} | {{CHANGE_NOTES_N02}} |
| ... | | |

### {{STATE_DIMENSION_2}}

| After Output N | State | Notes |
|---|---|---|
| N01 | {{INITIAL_STATE_2}} | Baseline established |

### {{STATE_DIMENSION_N}}

| After Output N | State | Notes |
|---|---|---|
| N01 | {{INITIAL_STATE_N}} | Baseline established |

---

## IMMUTABLE EVENTS
*(Events that have occurred and can never be undone — the "spine")*

| Output N | Event | Impact |
|---|---|---|
| N01 | {{IMMUTABLE_EVENT_1}} | {{IMPACT_1}} |

---

## OPERATION SEQUENCE HISTORY
*(Used by ConstraintTracker to enforce no-repeat rules)*

| Output N | Operation Sequence |
|---|---|
| N01 | {{OP_SEQ_N01}} |
| N02 | {{OP_SEQ_N02}} |
