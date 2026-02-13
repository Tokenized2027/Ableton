# REJECTION BRIEF TEMPLATE

Use this template when a downstream agent identifies issues that require upstream rework. Copy this into the relevant conversation and fill in the fields.

---

## REJECTION BRIEF: [Rejecting Agent] → [Target Agent]

**Track:** [Name]
**Date:** [Date]
**From:** [Agent name and tier, e.g., "Sound Designer — Tier 3"]
**Back To:** [Agent that needs to redo work, e.g., "Music Theory Architect — Tier 1"]
**Severity:** [Minor tweak / Significant rework / Fundamental issue]

### What's Wrong

[Specific, actionable description. Use musical terms and reference exact bars, parameters, or decisions.]

Example: "The chord progression in bars 33-48 (i-VI-III-VII) creates a major-key feel during what's supposed to be the Horror section. The III chord especially undermines the tension — at 148 BPM with a rolling bass, this sounds triumphant, not horrifying."

### What I Need Instead

[Clear specification. Be specific enough that the target agent can produce exactly what you need.]

Example: "Bars 33-48 need a progression that sustains dissonance. Suggestions: i-bII-v-bVI (Phrygian-flavored) or i-iv-bVI-v (keeps it firmly minor). The bass pattern can stay as-is — the harmonic context just needs to be darker."

### What I've Already Tried

[If the rejecting agent attempted to fix it themselves before escalating.]

Example: "Tried substituting bIII for III — better but still not dark enough. The issue is systemic — the whole 16-bar section needs reharm, not just one chord swap."

### Cascade Impact Assessment

**Decision Criteria:**
- Mark **YES** if that agent must redo completed work
- Mark **MAYBE** if that agent should review whether the change affects them
- Mark **NO** if that agent's work is completely unaffected

| Agent | Affected? | What Changes |
|-------|-----------|-------------|
| Narrative Architect | No | Emotional arc unchanged |
| Music Theory Architect | **YES** | Needs new progression for bars 33-48 |
| Arrangement Architect | Maybe | If new chords change energy curve, arrangement may need adjustment |
| MIDI Producer | **YES** | Bass pattern may need new root notes, lead melody needs rewrite |
| Automation Engineer | Maybe | Filter automation tied to chord changes may need update |
| Sound Designer | No | Timbres don't change, just notes |

### Priority

- [ ] **Blocking** — Can't continue production until resolved
- [ ] **Important** — Can work around temporarily but needs fixing before mixdown
- [ ] **Nice-to-have** — Would improve the track but not critical

### Shadow Creator Note

[For the Shadow Creator to assess when reviewing rejection: Does this rejection suggest a pattern? Is this the same kind of issue that came up in a previous track? Should this trigger a style-fingerprint or knowledge base update?]

---

## Example: Filled Rejection Brief

**Track:** Iron Dome
**Date:** 2026-02-14
**From:** Sound Designer — Tier 2
**Back To:** Music Theory Architect — Tier 1
**Severity:** Significant rework

### What's Wrong

The chord progression in bars 33-48 (i-VI-III-VII → Dm-Bb-G-C) creates a major-key feel during what's supposed to be the Horror section. The III chord (G major) especially undermines the tension — at 148 BPM with a rolling mechanical bass, this sounds triumphant, not horrifying.

When I tried to design a lead sound over this progression, everything I made sounded "uplifting" because the G major chord is pulling the tonality toward brightness. The narrative brief says "Horror: mechanical dread, the moment before impact" but these chords say "we're winning already."

**Specific problem bars:**
- Bars 37-40: G major chord (the III) — this is the main culprit
- Bars 41-44: C major chord (the VII) — also bright, but less offensive than the G

### What I Need Instead

Bars 33-48 need a progression that sustains dissonance and darkness throughout the Horror section. The bass pattern can stay exactly as-is (rolling 16ths on root), but the harmonic context needs to be darker.

**Suggestions:**
1. **Option A (Phrygian-flavored):** i - bII - v - bVI (Dm - Eb - Am - Bb)
   - The bII (Eb) creates immediate tension (half-step above root)
   - Keeps things minor and dark throughout
   - No major chords until Defiance section (bar 65+)

2. **Option B (Stay in Natural Minor):** i - iv - bVI - v (Dm - Gm - Bb - Am)
   - All minor chords except bVI (Bb major is acceptable — it's stable but not bright)
   - More "sad" than "horrifying" but still works narratively
   - Easier to write lead melody over (more conventional minor)

**My recommendation:** Option A (Phrygian-flavored). The bII chord is unusual and dissonant, which matches the "mechanical/alien" vibe of the bass. It's more adventurous but serves the Horror narrative better.

### What I've Already Tried

Tried substituting bIII (F major) for III (G major) — better but still not dark enough. The issue is systemic — the whole 16-bar section needs reharmonization, not just one chord swap.

Also tried keeping the chords but using darker lead timbres (FM bell, detuned saw) — doesn't fix it. The problem is harmonic, not timbral.

### Cascade Impact Assessment

| Agent | Affected? | What Changes |
|-------|-----------|-------------|
| Narrative Architect | **NO** | Emotional arc unchanged (Horror section is still Horror) |
| Music Theory Architect | **YES** | Needs new progression for bars 33-48 (16 bars) |
| Arrangement Architect | **NO** | Section structure unchanged (still 16-bar Horror buildup) |
| MIDI Producer | **YES** | Bass pattern roots may need adjustment if we use bII chord (Eb instead of D in some bars). Lead melody needs complete rewrite. |
| Automation Engineer | **MAYBE** | Filter automation is tied to current chord changes. If chords change, automation curve may need update. |
| Sound Designer (me) | **YES** | Will redesign lead patch after new chords confirmed. Current patch was voiced for major chords. |

**Estimated rework time:**
- Music Theory: 30 min (write new progression, verify against narrative)
- MIDI Producer: 1-2 hours (adjust bass roots if needed, write new lead melody)
- Automation Engineer: 15 min (update filter automation curve)
- Sound Designer: 30 min (re-voice lead patch for new harmony)

**Total:** 2.5-3.5 hours of rework

### Priority

- [x] **Blocking** — Can't continue production until resolved
- [ ] **Important** — Can work around temporarily but needs fixing before mixdown
- [ ] **Nice-to-have** — Would improve the track but not critical

**Rationale for "Blocking":** I've already spent 2 hours trying to design a lead sound that works over these chords and it's impossible. The harmonic foundation is wrong. Need to fix this before I can proceed with any Tier 2/3 work in the Horror section.

### Shadow Creator Note

**Pattern identified:** This is the second time (first was "War of the Worlds" sketch) where initial chord choices were too bright for a Horror section.

**Root cause:** Music Theory Architect may be defaulting to "natural minor = i-VI-III-VII" as a standard progression without considering narrative context.

**Suggested fix for future:**
1. Update Music Theory Architect prompt to include narrative-aware chord selection guidelines
2. Add to knowledge base: "Horror sections should avoid major III and VII chords in minor keys — use Phrygian, Locrian, or modal interchange"
3. Add to style-fingerprint/ARRANGEMENT_PATTERNS.md: "Horror = no major chords except bVI (Bb in Dm), Defiance = introduce major VII, Triumph = full major chords + harmonic minor"

**Action:** After this fix, create `docs/style-fingerprint/HORROR_HARMONY_RULES.md` so this doesn't happen on track #3.
