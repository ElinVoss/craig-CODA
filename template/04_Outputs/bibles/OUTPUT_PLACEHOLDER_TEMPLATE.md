---
title: "{{OUTPUT_UNIT_TITLE}}"
sequence_n: {{N}}
phase: "{{PHASE}}"
frame_policy: "{{ACTIVE_FRAME}}"
previous_outputs:
  - "{{PREVIOUS_OUTPUT_1}}"
  - "{{PREVIOUS_OUTPUT_2}}"
  # craig injects this list automatically via context chain
---

# {{OUTPUT_UNIT_TITLE}} — {{OUTPUT_UNIT}} N{{N}}

## Context Chain
*(Auto-injected by craig session.py — do not edit manually)*
Previous {{OUTPUT_UNIT_PLURAL}}: {{CONTEXT_CHAIN_LIST}}

---

## {{PREMISE_SECTION_NAME}}
{{PREMISE_CONTENT}}

---

## {{CONSTRAINTS_SECTION_NAME}}
- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}

---

## {{ENTITIES_SECTION_NAME}}
*(Frame: {{ACTIVE_FRAME}} — per configs/frame_access_policy.yaml)*

{{ENTITIES_CONTENT}}

---

## {{DOMAIN_RULES_SECTION_NAME}}
{{DOMAIN_RULES_CONTENT}}

---

## {{CONTEXT_SECTION_NAME}}
{{CONTEXT_CONTENT}}

---

## {{STRUCTURE_SECTION_NAME}}

### Unit 1 — {{UNIT_1_LABEL}}
{{UNIT_1_CONTENT}}

### Unit 2 — {{UNIT_2_LABEL}}
{{UNIT_2_CONTENT}}

*(continue for all {{INTERNAL_UNIT_COUNT}} units)*

---

## {{OPERATION_SEQUENCE_SECTION_NAME}}

Operation sequence for this {{OUTPUT_UNIT}}:
1. {{OP_1}}
2. {{OP_2}}
3. {{OP_N}}

Constraint check: ✅ No consecutive repeats | ✅ No rotation pattern | ✅ No sequence repeat

---

## {{FORBIDDEN_CHECK_SECTION_NAME}}
- All forbidden terms from `01_Foundation/forbidden_terms.yaml`: ✅ None present
- Frame access policy respected: ✅
- {{ADDITIONAL_FORBIDDEN_CHECK}}: ✅

---

## Validation Checklist

- [ ] All foundation nodes queried via SHA-pinned paths
- [ ] Frame access policy applied (only {{ACTIVE_FRAME}} frame queried)
- [ ] Forbidden terms check passed
- [ ] No retcons — all state changes consistent with progression master
- [ ] Operation sequence constraint-valid
- [ ] Context chain injected ({{N-1}} previous {{OUTPUT_UNIT_PLURAL}} referenced)
- [ ] All required sections present
- [ ] {{PROJECT_SPECIFIC_VALIDATION_CHECK}}
