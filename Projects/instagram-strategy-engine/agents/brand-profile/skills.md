# Agent Skills: Brand Profile

## 1. Assigned Skills & Capabilities
- **Brand Profile Foundation Skill (`brand-profile-skill.md`)**:
  - *Description*: The foundational discovery and extraction skill that derives identity, positioning, audience, voice, proof, guardrails, and operational defaults from raw context and targeted reasoning interviews.
- **Voice & Lexicon Architecture**:
  - *Description*: Mapping tone onto concrete dimensions, defining preferred vs. banned lexicons, signature rhetorical devices, and cadence rules.
- **Audience & Attention Mapping**:
  - *Description*: Segmenting core buyer vs. practitioner follower dynamics, attention triggers, and pain points.
- **Guardrails & Compliance Extraction**:
  - *Description*: Enforcing regulatory claims, disclaimer logic, AI disclosure policies, and brand safety boundaries.

## 2. Tools & MCP Integrations
- [x] Web Reader / URL Fetching (Extracting text from brand websites and landing pages)
- [x] File System Access (Reading existing decks, docs, and writing `brand-profile.md`)
- [x] Search / Social Research (Investigating competitor positioning and social handle references)
- [x] Interactive Multi-batch Questioning (Adaptive conversational probing)

## 3. Skill Execution Workflow
1. **Step 1 (Check & Load)**: Verify if a valid, current `brand-profile.md` exists. If yes, load into memory, reflect in ~2 lines, and hand off.
2. **Step 2 (Raw Material Ingestion)**: Ingest URLs, decks, about pages, or handles provided by the user. Draft a provisional profile internally.
3. **Step 3 (Reasoning Interview)**: Ask small batches (2–4 questions) focusing on un-inferred specifics, challenging vague abstractions with comparative prompts.
4. **Step 4 (Artifact Synthesis)**: Assemble `brand-profile.md` following the standard template and reference guidelines.
5. **Step 5 (Confirmation & Handoff)**: Reflect the finalized profile back to the user for one round of confirmation, saving the artifact for downstream content skills.
