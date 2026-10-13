# Agent Skills: Audience Research

## 1. Assigned Skills & Capabilities
- **Audience Research Foundation Skill (`audience-research-skill.md`)**:
  - *Description*: Synthesizes Jobs-to-be-Done (JTBD), pains, desires, objections, sophistication levels, and authentic Voice of Customer language banks into `audience.md`.
- **Jobs-to-be-Done (JTBD) & Motivation Mapping**:
  - *Description*: Deconstructs audience drivers across functional, emotional, and social dimensions, separating Buyer vs. Follower dynamics.
- **Voice of Customer (VoC) Mining**:
  - *Description*: Extracts verbatim phrases, emotional pain points, and objections from social comments, reviews, Reddit forums, support tickets, and sales notes.
- **Audience Segmentation & Sophistication Profiling**:
  - *Description*: Pins 1–3 sharp segments, classifying awareness and sophistication stages (beginner vs. practitioner vs. executive) to govern copy depth.

## 2. Tools & MCP Integrations
- [x] Web Reader & Search (Scraping public forums, Reddit discussions, reviews, comment sections)
- [x] Workspace File Access (Reading `brand-profile.md` and producing `audience.md`)
- [x] Conversational Probing (Interactive JTBD reasoning interviews)

## 3. Skill Execution Workflow
1. **Step 0 (Read Foundation)**: Load and inspect `brand-profile.md` for positioning, category, and initial audience cues.
2. **Step 1 (Gather Evidence)**: Ingest provided customer reviews, support logs, social comments, and search public community forums. Flag any unverified claims as hypotheses.
3. **Step 2 (Segment & Role Definition)**: Establish 1–3 primary segments and separate the Buyer (decision/payment) from the Follower (engagement/sharing).
4. **Step 3 (Dimension Mapping)**: Extract JTBD, pains, desires, pre-existing beliefs, objections, platform mindsets, and sophistication level.
5. **Step 4 (Language Bank Assembly)**: Collate raw, verbatim phrases for problem descriptions, desired transformations, and resistance triggers.
6. **Step 5 (Artifact Generation & Handoff)**: Output `audience.md` using the standard schema, present summary to user for feedback, and publish for downstream skill consumption.
