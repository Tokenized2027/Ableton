# PROMPT A/B TEST TEMPLATE

Use this to systematically test agent prompt improvements before rolling them out. Run both versions with identical input and compare.

---

## Prompt A/B Test: [Agent Name]

**Date:** [Date]
**Tester:** Avi
**Agent under test:** [e.g., MIDI Producer]

### Test Setup

**Task:** [Specific, repeatable task — the same for both versions]

Example tasks by agent:
- MIDI Producer: "Generate 8-bar rolling Nitzhonot bass in Am at 148 BPM following progression i-VI-III-VII"
- Sound Designer: "Design a lead synth patch for a Defiance section — aggressive but melodic, Serum-based"
- Arrangement Architect: "Create a 192-bar arrangement for a Horror→Defiance→Triumph track at 148 BPM"
- Shadow Creator: "Develop a track concept around the theme of surviving a rocket attack"

**Input brief (identical for both runs):**

```
[Paste the exact input you'll give both versions]
```

**Current prompt version:** v[X] — [brief description of current state]
**Modified prompt version:** v[X+1] — [brief description of what changed]

**What specifically changed in the prompt:**
1. [Change 1, e.g., "Added I/O contract section at top"]
2. [Change 2, e.g., "Replaced generic bass description with exact velocity sequence"]
3. [Change 3, e.g., "Added range-based parameters instead of fixed values"]

---

### Run A — Current Prompt (v[X])

**Output:**
```
[Paste the agent's complete output here]
```

**Evaluation:**

| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| **Musical accuracy** — Is it in key? Does rhythm work? Does it follow the progression? | | |
| **Specificity** — Are there actual values (MIDI notes, Hz, ms, dB) vs. vague descriptions? | | |
| **Actionability** — Can you execute this in Ableton immediately without interpretation? | | |
| **Creative quality** — Does it sound/feel like Flyin' Colors? Does it serve the narrative? | | |
| **Efficiency** — Did it get there directly or meander through unnecessary explanation? | | |
| **TOTAL** | /25 | |

**Best moment:** [What was the single best thing in this output?]

**Worst moment:** [What was the biggest gap or failure?]

---

### Run B — Modified Prompt (v[X+1])

**Output:**
```
[Paste the agent's complete output here]
```

**Evaluation:**

| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| **Musical accuracy** | | |
| **Specificity** | | |
| **Actionability** | | |
| **Creative quality** | | |
| **Efficiency** | | |
| **TOTAL** | /25 | |

**Best moment:** [What was the single best thing in this output?]

**Worst moment:** [What was the biggest gap or failure?]

---

### Comparison & Decision

**Winner:** [A / B / Tie]

**Score difference:** [A total] vs [B total] = [difference]

**What specifically improved:**
- [e.g., "The I/O contract made the output more structured — it delivered exactly the format I can use"]
- [e.g., "The exact velocity sequence example led to much more specific MIDI output"]

**What specifically degraded:**
- [e.g., "The prompt got longer and the agent spent more tokens on setup before producing output"]
- [e.g., "Range-based parameters made the agent indecisive — it asked which end of the range to use instead of just picking"]

**What was neutral (no impact):**
- [e.g., "The added BPM reference table didn't seem to affect output quality"]

### Changes to Keep

1. [Specific change that helped]
2. [Specific change that helped]

### Changes to Revert

1. [Specific change that didn't help or made things worse]

### Changes to Iterate On

1. [Change that showed promise but needs refinement — describe what to try next]

---

### Carry Forward

**Updated prompt version:** v[X+2] (incorporating winning changes, reverting losers)

**Next test planned:** [What's the next modification to A/B test?]

**Pattern noticed:** [Any broader insight about what makes prompts work better for this agent?]

---

## Testing Order (Recommended)

| Order | Agent | Why This Order |
|-------|-------|---------------|
| 1 | MIDI Producer | Most concrete output — MIDI notes are objectively evaluable |
| 2 | Sound Designer | Semi-concrete — synth parameter specs are verifiable |
| 3 | Arrangement Architect | Structural — section layouts can be evaluated against narrative |
| 4 | Automation Engineer | Technical — automation curves are measurable |
| 5 | Narrative Architect | Creative — harder to score but important |
| 6 | Shadow Creator | Most subjective — test last when you understand what "good" looks like |

## Scoring Guide

**1 — Fail:** Output is wrong, unusable, or completely misses the brief
**2 — Poor:** Partially relevant but major gaps, significant interpretation needed
**3 — Adequate:** Gets the job done but generic, could be any trance track
**4 — Good:** Specific to Flyin' Colors, actionable, serves the narrative
**5 — Excellent:** Exactly what you'd want, surprises you with creative quality, immediately usable
