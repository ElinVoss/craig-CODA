# {{ENTITY_NAME}} — Entity Definition

**Entity ID**: {{ENTITY_ID}}
**Domain**: {{DOMAIN}}
**Frames available**: {{FRAME_LIST}}

---

## UNIVERSAL PROFILE
*(Information true across all frames — visible regardless of which frame is active)*

### Identity
- **Name**: {{ENTITY_NAME}}
- **Role**: {{ENTITY_ROLE}}
- **Domain**: {{ENTITY_DOMAIN}}

### Core Attributes
- {{ATTRIBUTE_1}}: {{VALUE_1}}
- {{ATTRIBUTE_2}}: {{VALUE_2}}
- {{ATTRIBUTE_N}}: {{VALUE_N}}

### Current State
*(Updated in 03_State_Tracking/ — do not modify here)*
- State as of output unit {{LAST_OUTPUT_N}}: {{CURRENT_STATE}}

---

## FRAMES

### Frame: {{FRAME_1_NAME}}
*(Accessible: {{FRAME_1_ACCESS_STAGES}})*

**What this frame reveals:**
{{FRAME_1_REVEALS}}

**Public motives:**
{{FRAME_1_MOTIVES}}

**Visible flaws:**
{{FRAME_1_FLAWS}}

**Relationships (in this frame):**
- {{RELATIONSHIP_1}}: {{RELATIONSHIP_1_DESCRIPTION}}

---

### Frame: {{FRAME_2_NAME}}
*(Accessible: {{FRAME_2_ACCESS_STAGES}})*

**What this frame reveals:**
{{FRAME_2_REVEALS}}

**Hidden motives:**
{{FRAME_2_MOTIVES}}

**True nature:**
{{FRAME_2_TRUE_NATURE}}

**Relationships (in this frame):**
- {{RELATIONSHIP_1}}: {{RELATIONSHIP_1_TRUE_DESCRIPTION}}

---

## PROGRESSION CONSTRAINTS
*(These accumulate and cannot be reset without cause)*

- {{PROGRESSION_CONSTRAINT_1}}
- {{PROGRESSION_CONSTRAINT_2}}

---

*SHA-pin this file in knowledge_index.json after any revision.*
