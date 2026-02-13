# CONTINUATION BRIEF TEMPLATE

Use this at the start of every new conversation to resume production work. Copy, fill in, and paste into the new session.

---

## CONTINUATION BRIEF — [Track Name]

**Date:** [Date]
**Last Session:** [Date of previous session]
**Project:** [Shadow Creator / Production Studio / Quality Control]
**Agent Mode:** [Which agent(s) were active]

### Track Identity
- **Track name:** [Name]
- **Concept:** [1-sentence narrative summary]
- **BPM:** [e.g., 148]
- **Key / Scale:** [e.g., Am / Natural Minor, switching to Harmonic Minor at bar 97]
- **Emotional Arc:** [e.g., Horror (bars 1-64) → Defiance (65-128) → Triumph (129-192)]
- **Target Length:** [bars / minutes]

### Current State of Production

**Section Being Worked On:** [e.g., "Drop 1, bars 49-80"]

**Elements Placed:**
| Track | Has MIDI? | Sound Loaded? | Automation Done? | Status |
|-------|-----------|---------------|------------------|--------|
| Kick | ✅ | ✅ | ❌ | Pattern done, no sidechain automation yet |
| Bass | ✅ | ✅ | Partial | 16th pattern done, filter sweep bars 49-56 only |
| Lead | ❌ | ✅ (Serum preset) | ❌ | Timbre set, no melody written |
| Pad | ✅ | ✅ | ✅ | Complete for this section |
| Arp | ❌ | ❌ | ❌ | Not started |
| FX/Risers | ❌ | ❌ | ❌ | Not started |

**Chord Progression (current section):** [e.g., i - VI - III - VII, 2 bars each]

### Last Session Summary
- **What was accomplished:** [2-3 sentences]
- **Last creative decision:** [The most recent artistic choice and its rationale]
- **What was planned next:** [What was the intended next step when the session ended]

### Emotional Arc Position
```
[Horror]----[Defiance]----[Triumph]
              ^
         WE ARE HERE
         (Building into the first drop — transitioning from Horror to Defiance)
```

### Open Creative Questions
[Unresolved artistic decisions that need addressing this session]

1. [e.g., "Should the lead enter at bar 49 or build up to bar 57?"]
2. [e.g., "The bass feels too clean for the Horror section — add more distortion or keep it for contrast with Drop?"]
3. [e.g., "Hebrew sample placement: 'Am Yisrael Chai' at the Triumph climax or earlier in Defiance?"]

### Technical State
- **Ableton project location:** [exact file path]
- **Session state JSON version:** [version number from state file]
- **MCP server status:** [running / needs restart / not started]
- **Known issues:** [any bugs, sync problems, or workarounds in effect]

### Reference Context
[Which reference tracks or style-fingerprint files are relevant for this session's work]

- Primary reference for this section: [e.g., "Filteria - The Inner Light, bars 45-80 (drop energy)"]
- Style-fingerprint to load: [e.g., "BASS_IDENTITY.md — rolling bass range decisions"]

---

## Emergency: Context Overflow Recovery

**If you hit the context limit mid-session:**

1. **Stop immediately** — Don't try to continue in this conversation
2. **Start new conversation** in the same Claude Project
3. **Copy this continuation brief** + the last 3-5 messages from this conversation
4. **Paste into new conversation** with header: `⚠️ CONTEXT OVERFLOW RECOVERY`
5. **Continue from exact state** — all musical decisions preserved

**What to copy:**
- This full continuation brief (captures state)
- Your last question/instruction (what you were working on)
- My last 2-3 responses (context for current work)
- Any open creative decisions from this conversation

**Example recovery message:**
```
⚠️ CONTEXT OVERFLOW RECOVERY

We hit the context limit while working on Iron Dome. Resuming from exact state:

[Paste continuation brief here]

Last 3 messages:
[Your question about lead melody timing]
[My response with two options]
[Your decision to try Option B]

Continue: I chose Option B (lead enters at bar 57). Let's write the ascending phrase now.
```

**Prevent overflow:**
- Use continuation briefs every 20-30 messages
- Start new conversations between major sections (intro → buildup → drop)
- If a single section discussion goes past 50 messages, start fresh

---

## Example: Quick Continuation Brief (2-minute version)

**Track:** Iron Dome | **BPM:** 148 | **Key:** Dm | **Working on:** Drop 1, bars 49-80

**Last session:** Finished mechanical bass MIDI pattern (4-bar loop × 8), started lead sound design in Vital
**Next:** Write lead melody (ascending phrase, 8 bars, counter to bass), add rolling arp layer
**Open question:** Lead enters at bar 49 (with drop) or bar 57 (delayed entrance for tension)?

**Continuation:** Load `reference-analysis/filteria-birds.md` — using his lead phrasing style as template

---

## Example: Full Continuation Brief

**Date:** 2026-02-14
**Last Session:** 2026-02-13
**Project:** Shadow Creator
**Agent Mode:** Production mode (acting as Sound Designer + MIDI Producer)

### Track Identity
- **Track name:** Iron Dome
- **Concept:** The sound of the Iron Dome missile defense system activating during a rocket attack — mechanical precision vs. human terror, the machine that protects
- **BPM:** 148
- **Key / Scale:** Dm / Natural Minor (bars 1-96), switching to Harmonic Minor at bar 97 for Triumph section
- **Emotional Arc:** Horror (bars 1-64) → Defiance (65-128) → Triumph (129-192)
- **Target Length:** 192 bars (~7:48 minutes)

### Current State of Production

**Section Being Worked On:** Drop 1, bars 49-80 (Horror → Defiance transition)

**Elements Placed:**
| Track | Has MIDI? | Sound Loaded? | Automation Done? | Status |
|-------|-----------|---------------|------------------|--------|
| Kick | ✅ | ✅ (Kick 2) | ❌ | Four-on-floor pattern complete, no sidechain yet |
| Bass (Mechanical) | ✅ | ✅ (Serum preset) | Partial | 16th pattern done, filter sweep bars 49-56 only, needs bars 57-80 |
| Sub Bass | ✅ | ✅ (Sine wave) | ✅ | Root note sustain, complete for this section |
| Lead | ❌ | ✅ (Vital - supersaw patch) | ❌ | Timbre set (bright, aggressive), NO melody written yet |
| Arp | ❌ | ❌ | ❌ | Not started — will use Serum different instance |
| Pad | ✅ | ✅ (Kontakt strings) | ✅ | Dm chord sustain, complete |
| Hi-hats | ✅ | ✅ (samples) | ❌ | Tight 16th pattern, no velocity automation yet |
| FX/Risers | ❌ | ❌ | ❌ | Not started |

**Chord Progression (bars 49-80):** i - bVI - bVII - i (Dm - Bb - C - Dm), 8 bars each = 4 cycles

### Last Session Summary
- **What was accomplished:**
  - Created mechanical bass sound in Serum (FM technique, saved as preset)
  - Programmed 4-bar MIDI loop, extended to 32 bars
  - Added filter automation (bars 49-56 sweep from 400Hz → 800Hz)
  - Designed lead timbre in Vital (supersaw, 7 voices, detune 0.18)

- **Last creative decision:**
  Chose Dm natural minor for Horror section instead of Phrygian. Rationale: Phrygian felt too exotic/ethnic for mechanical theme. Natural minor is colder, more industrial. Saving Harmonic minor for Triumph (bars 129+) to create clear emotional shift.

- **What was planned next:**
  Write lead melody for bars 49-80. Should counter the bass (bass is mechanical/static, lead should be ascending/human/reaching). Reference Filteria's phrasing from "Birds" analysis.

### Emotional Arc Position
```
[Horror]----------[Defiance]----------[Triumph]
    ^
WE ARE HERE (bars 49-80)
(First drop — Horror energy, but starting to build resistance/defiance)
```

The bass represents the machine (Iron Dome). The lead we're about to write represents human hope/resistance. They should coexist but remain distinct — don't blend them too much. Mechanical vs. organic = the core tension.

### Open Creative Questions

1. **Lead entrance timing:** Enter at bar 49 (with the drop) or delay to bar 57 (second half)?
   - **Option A (bar 49):** Full energy immediately, lead + bass together from start
   - **Option B (bar 57):** Build tension — bass alone for 8 bars, then lead answers
   - **Leaning toward:** Option B — lets the mechanical bass establish itself first

2. **Lead melody contour:** Ascending (reaching/hopeful) or descending (heavy/weighed down)?
   - **Narrative lens:** Defiance = rising up despite the weight, so ascending makes sense
   - **Musical lens:** Bass is static/repetitive, lead should move to create contrast
   - **Decision:** Ascending phrase, starts on D4, peaks at A4 (perfect 5th), 8-bar phrase

3. **Arp layer:** Rolling 16ths (Nitzhonot style) or syncopated 8ths?
   - Haven't decided yet — will test both after lead melody is done

### Technical State
- **Ableton project location:** `C:\Users\Avi\Desktop\Ableton Projects\Iron Dome\Iron Dome v3.als`
- **Session state JSON version:** N/A (no MCP server yet, working manually)
- **MCP server status:** Not started (Phase 1 planned for next week)
- **Known issues:**
  - Filter automation jumps at bar 56 (not smooth) — need to redraw curve
  - Kick sample has slight click at transient — might need to fade or swap sample

### Reference Context

- **Primary reference:** `reference-analysis/filteria-birds.md` — specifically bars 45-80 analysis (his lead phrasing during drop section)
- **Style-fingerprint to load:** None created yet (first track using new system)
- **Memory/preferences:** First session, no established preferences yet beyond "mechanical bass works"
