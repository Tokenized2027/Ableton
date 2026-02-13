# I/O Contract Template for Agent Prompts

**Add this section to the TOP of every agent prompt** (after identity/role, before responsibilities).

---

## Template

```markdown
## I/O Contract

### What I Receive (Input)
- [List the specific deliverables/briefs you expect from upstream agents]
- [Example: "Narrative Brief from Narrative Architect with emotional arc and samples needed"]
- [Example: "Musical Blueprint from Music Theory Architect with key, scale, BPM, progressions"]

### What I Deliver (Output)
- [List the specific deliverables you produce for downstream agents]
- [Example: "Sound Design Spec: Track-by-track synth assignments, preset names, processing chain"]
- [Format specification if relevant]

### Maximum Response Length
- **Target:** [X characters] — concise, actionable
- **Maximum:** [Y characters] — if longer than this, you're writing an essay, not a production spec
- **Format:** Bullet points > paragraphs, tables > prose

### Communication Style
- [Specificity level: "exact parameter values" vs "creative descriptions"]
- [Example: "Provide MIDI note numbers (D3 = MIDI 50), not just 'low D'"]
- [Example: "Provide filter cutoff in Hz (800 Hz), not 'medium-high'"]
```

---

## Examples by Agent

### Music Theory Architect

```markdown
## I/O Contract

### What I Receive
- Narrative Brief from Narrative Architect
  - Emotional arc (Horror → Defiance → Triumph)
  - Section markers and transitions
  - Mood descriptors for each section

### What I Deliver
- **Musical Blueprint** (markdown format)
  - BPM: Single value (e.g., 148)
  - Key: Root note + mode (e.g., Dm)
  - Scale: Specific scale name (e.g., Natural Minor, Harmonic Minor, Phrygian Dominant)
  - Chord Progressions: Roman numerals + actual chords for each section
    - Format: `i - bVI - bVII - i (Dm - Bb - C - Dm)`
  - Harmonic rhythm: How often chords change (e.g., "2 bars per chord")

### Maximum Response Length
- **Target:** 500 characters (one screen)
- **Maximum:** 1,000 characters (if you need more, you're overthinking)
- **Format:** Tables for progressions, bullet points for notes

### Communication Style
- **Exact values only** — "148 BPM", not "around 145-150"
- **Specific scales** — "Harmonic Minor", not "minor with exotic flavor"
- **Complete progressions** — Show all chords for each section, not "similar to intro"
```

### MIDI Producer

```markdown
## I/O Contract

### What I Receive
- Musical Blueprint from Music Theory Architect
  - Key, scale, BPM, chord progressions
- Sound Design Spec from Sound Designer
  - Which tracks need MIDI
  - Instrument assignments
- Arrangement Map from Arrangement Architect
  - Bar ranges for each section
  - When elements enter/exit

### What I Deliver
- **MIDI Patterns** (either as text description for manual entry OR MCP commands)
  - MIDI note numbers (not letter names — "D3 = MIDI 50")
  - Velocity values (0-127, exact numbers)
  - Timing (bar + beat + 16th, or MIDI ticks)
  - Pattern length (in bars)
  - **Example format:**
    ```
    Bass Pattern (bars 1-4, repeating):
    Bar 1: D2 (MIDI 38) @ velocity 100, 16th notes (every 240 ticks)
    Bar 2: F2 (MIDI 41) @ velocity 95, same rhythm
    Bar 3: C2 (MIDI 36) @ velocity 105, same rhythm
    Bar 4: G2 (MIDI 43) @ velocity 90, same rhythm
    ```

### Maximum Response Length
- **Target:** 800 characters per pattern (concise enough to execute quickly)
- **Maximum:** 2,000 characters per pattern (if longer, break into multiple patterns)
- **Format:** Code blocks for MIDI data, NOT prose descriptions

### Communication Style
- **MIDI numbers, not letter names** — "MIDI 50" > "D3"
- **Exact velocities** — "100, 95, 105, 90" not "varying velocities"
- **Exact timing** — "240 ticks (16th note @ 960 PPQN)" not "fast rhythm"
- **Copy-paste ready** — I should be able to execute your output immediately in Ableton
```

### Sound Designer

```markdown
## I/O Contract

### What I Receive
- Musical Blueprint from Music Theory Architect (for context)
- Narrative Brief from Narrative Architect (for emotional direction)

### What I Deliver
- **Sound Design Spec** (markdown format)
  - Track assignments: "Track 1: Kick - Kick 2 plugin, preset 'Tight 909'"
  - Synth patch instructions:
    ```
    Lead (Serum):
    - Osc A: Saw wave, 7 voices, detune 0.18
    - Osc B: Off
    - Filter: LP 24dB @ 1200 Hz, resonance 0.25
    - FX: Reverb 30% mix, Delay 1/8 note 15% mix
    ```
  - Processing chain: "EQ → Compressor → Saturator → Reverb"
  - Preset save names: "FC_Lead_Defiance_Bright_v1.fxp"

### Maximum Response Length
- **Target:** 300 characters per sound (one synth patch)
- **Maximum:** 600 characters per sound
- **Format:** Code blocks for synth settings, bullet points for processing

### Communication Style
- **Exact parameter values** — "Cutoff 1200 Hz" not "bright filter"
- **Plugin names** — "Serum" not "a good subtractive synth"
- **Processing order matters** — Specify chain sequence
- **Save preset names** — Follow naming convention (FC_[Role]_[Section]_[Character]_v[N])
```

---

## Why I/O Contracts Matter

### Problem Without Contracts
```
User: "What bass sound should I use?"
Agent: "For this Horror section, you'll want a dark, mechanical bass. Think industrial,
relentless, machine-like. The timbre should evoke a sense of dread and precision.
Consider using a saw wave with some FM modulation to add that metallic edge. The filter
should be somewhat closed to keep it dark, but not too much or you'll lose definition.
Experiment with distortion — maybe a tube saturation for warmth, or perhaps a more
aggressive digital distortion if you want more edge. The key is to find that sweet spot
between dark and defined. [continues for 2000 more characters...]"
```

Result: **Vague, unusable, you still don't know what to do.**

### With I/O Contract
```
User: "What bass sound should I use?"
Agent (Sound Designer with I/O contract):

Bass (Serum):
- Osc A: Saw wave
- Osc B: Sine wave (FM modulator)
- FM Depth: 42%
- Detune: +7 cents (Osc A)
- Filter: LP 24dB @ 650 Hz, resonance 0.35
- FX: Tube distortion 40% drive
- Sub: -6dB sine layer (Serum sub osc)

Processing: Distortion → EQ (cut 200 Hz -3dB, boost 100 Hz +2dB) → Compressor (4:1, medium attack)

Preset: FC_Bass_Horror_Mechanical_v1.fxp

[215 characters — concise, actionable, exact]
```

Result: **Copy. Paste. Execute. Move forward.**

---

## Adding I/O Contracts to Existing Agents

### Step 1: Identify Current Bloat
- Read agent prompt
- Find sections where it says "provide guidance on X" or "help the user with Y"
- These are vague — replace with I/O contracts

### Step 2: Define Inputs
- What does this agent NEED to receive to do its job?
- List upstream deliverables (briefs, specs, blueprints)

### Step 3: Define Outputs
- What does this agent PRODUCE?
- Specify format (markdown table? code block? bullet list?)
- Specify length limits

### Step 4: Add Maximum Response Length
- Target: One screen of text (500-800 chars for most agents)
- Maximum: Two screens (1,000-2,000 chars)
- If agent regularly exceeds maximum, the prompt is wrong

### Step 5: Test
- Give agent a real task
- Measure response length
- If it writes an essay → tighten the contract
- If it's too terse → loosen slightly

---

## Character Count Guide

| Length | What Fits | Use For |
|--------|-----------|---------|
| 300 chars | 3-4 bullet points | Single synth patch, simple answer |
| 500 chars | 5-7 bullet points OR small table | Musical blueprint, sound design spec |
| 800 chars | Medium table OR code block | MIDI pattern, automation spec |
| 1,000 chars | Large table OR detailed instructions | Arrangement map, complex progression |
| 2,000 chars | Maximum before it's an essay | Full section breakdown (intro + buildup + drop) |

**Rule of thumb:** If you can't see the entire response without scrolling, it's too long.

---

## Common I/O Contract Violations (Fix These)

### Violation 1: No Length Limit
```markdown
## What I Deliver
- Advice on sound design approaches
```
**Problem:** "Advice" can be 10,000 characters of rambling.

**Fix:**
```markdown
## What I Deliver
- Sound Design Spec (max 600 chars per sound)
  - Synth patch parameters
  - Processing chain
  - Preset save name
```

### Violation 2: Vague Input Requirements
```markdown
## What I Receive
- Information about the track
```
**Problem:** "Information" is not specific enough.

**Fix:**
```markdown
## What I Receive
- Narrative Brief (emotional arc, section markers)
- Musical Blueprint (key, BPM, progressions)
```

### Violation 3: Format Not Specified
```markdown
## What I Deliver
- Chord progressions for each section
```
**Problem:** Could be prose ("The intro uses a minor i-VI progression") or structured data.

**Fix:**
```markdown
## What I Deliver
- Chord Progressions (table format):
  | Section | Progression | Duration |
  |---------|------------|----------|
  | Intro   | i - bVI - bVII - i | 2 bars/chord |
```

---

## Template for Agent Prompt Header

```markdown
# [Agent Name]

**Role:** [One sentence]

## I/O Contract

### What I Receive
- [Upstream deliverable 1]
- [Upstream deliverable 2]

### What I Deliver
- [Downstream deliverable]
  - Format: [table/bullet list/code block]
  - Example: [show format]

### Maximum Response Length
- **Target:** [X] characters
- **Maximum:** [Y] characters
- **Format:** [bullet points/tables/code blocks]

### Communication Style
- [Specificity requirement 1]
- [Specificity requirement 2]

---

[Rest of agent prompt: responsibilities, knowledge, examples, etc.]
```

---

**Add I/O contracts to all 11 agents. Every agent becomes 3x more useful.**
