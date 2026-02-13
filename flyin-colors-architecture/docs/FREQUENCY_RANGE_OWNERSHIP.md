# Frequency Range Ownership Chart — Flyin' Colors

**Purpose:** Define which instruments own which frequency ranges to prevent mud and masking.

**Key Principle:** Some overlap is INTENTIONAL for fullness. Some overlap is FORBIDDEN to maintain clarity.

---

## The Chart

| Frequency Range | Primary Owner | Secondary (Intentional Overlap) | NEVER Overlap With | Notes |
|----------------|---------------|--------------------------------|-------------------|-------|
| **20-40 Hz** | Sub Bass | Kick (transient only) | — | Sub-only zone. Kick can hit briefly but shouldn't sustain here. |
| **40-80 Hz** | Kick Fundamental | Sub Bass (sustain) | — | **SHARED INTENTIONALLY** — Kick transient + sub sustain = power |
| **80-150 Hz** | Rolling Bass | Kick (tail) | Pads, Leads | Bass melody lives here. Keep pads/leads OUT. |
| **150-300 Hz** | Rolling Bass (upper harmonics) | Pads (low end of chord) | Kick, Sub | **OVERLAP ZONE** — Bass + pad low notes can coexist if EQ'd correctly |
| **300-600 Hz** | Pads (chord body) | Rolling Bass (filter sweeps) | Kick | Midrange warmth. Bass can sweep through but shouldn't camp here. |
| **600-1200 Hz** | Lead (fundamental) | Pads (mid-range) | — | **OVERLAP ZONE** — Lead melody + pad harmony can share if not too dense |
| **1.2k-3k Hz** | Lead (presence) | Vocals/Samples (if present) | Pads | Vocal/lead intelligibility zone. Pads stay below or above. |
| **3k-6k Hz** | Hi-hats | Lead (harmonics), Cymbals | Kick, Bass, Pads | High-end energy. Drums + lead harmonics only. |
| **6k-12k Hz** | Cymbals, Ride | Hi-hats (harmonics) | Everything else | Shimmer zone. Only percussive elements. |
| **12k-20k Hz** | Air/Reverb Tails | — | — | Spatial zone. Reverb/delay tails, synth air. |

---

## Intentional Overlap Zones (GOOD)

These overlaps create fullness and power when done correctly:

### 1. **Kick + Sub Bass (40-80 Hz)**
- **Why:** Kick transient provides punch, sub provides sustained power
- **How to manage:**
  - Sidechain sub to kick (ducking -3 to -6 dB)
  - OR: High-pass sub at 30 Hz, low-pass kick tail at 60 Hz (they pass each other)
  - Result: Kick hits, sub fills the space between kicks

### 2. **Rolling Bass + Pads (150-300 Hz)**
- **Why:** Bass provides movement, pads provide harmonic context
- **How to manage:**
  - EQ pad: cut 150-250 Hz by -3 dB (make room for bass fundamental)
  - EQ bass: gentle boost 100-200 Hz (assert presence)
  - Result: Bass melody is clear, pads support without muddiness

### 3. **Lead + Pads (600-1200 Hz)**
- **Why:** Lead needs to sit "on top" of harmonic bed
- **How to manage:**
  - Pads: wide stereo, lower velocity, EQ dip at lead fundamental
  - Lead: mono or narrow stereo, brighter, forward in mix
  - Result: Lead is intelligible, pads provide depth

---

## Forbidden Overlaps (BAD)

These create mud, masking, and loss of clarity:

### 1. **Pads in 80-150 Hz (Bass Territory)**
- **Problem:** Pads with too much low-end mud the bassline
- **Fix:** High-pass pads at 150 Hz minimum (200 Hz if bass is very active)
- **Exception:** Breakdown sections with no bass — pads can go lower

### 2. **Kick + Pads Below 100 Hz**
- **Problem:** Pad low notes mask kick punch
- **Fix:** Sidechain pads to kick OR high-pass pads at 100 Hz
- **Test:** Solo kick + pads — can you feel the kick punch through?

### 3. **Multiple Elements Fighting 1-3 kHz (Presence Zone)**
- **Problem:** Lead, vocal samples, and snare all fight for intelligibility
- **Fix:** Pick ONE primary element per section:
  - Drop section: Lead owns 1-3 kHz
  - Breakdown with vocal: Vocal owns 1-3 kHz, lead dips here
  - Snare fill: Snare briefly takes 2 kHz, everything else ducks

---

## Flyin' Colors Specific Guidelines

### Horror Section (Mechanical, Dark)
- **Sub + Kick:** Aggressive overlap (40-80 Hz) — maximum weight
- **Bass:** Filtered low (cutoff 600-800 Hz) — dark, muffled
- **Pads:** Minimal (or absent) — sparse, cold atmosphere
- **Lead:** Delayed entrance OR only harmonics (no fundamental) — dissonant

**Result:** Heavy, oppressive, machine-like

### Defiance Section (Driving, Aggressive)
- **Bass:** Filter opens (cutoff 900-1200 Hz) — full range, aggressive
- **Lead:** Enters with presence (1-3 kHz boosted) — assertive, human
- **Pads:** Supportive but secondary (wide stereo, -3 dB in mix) — context
- **Hi-hats:** Active 16ths (3-6 kHz) — energy, movement

**Result:** Full spectrum energy, bass + lead battle for dominance

### Triumph Section (Soaring, Uplifting)
- **Bass:** Less aggressive (cutoff 800-1000 Hz, filter sweeps gentler)
- **Lead:** Dominant (1-4 kHz owns the space) — melodic, emotional
- **Pads:** Lush chords (300-1200 Hz) — harmonic richness
- **Strings/Classical:** Enter (500-3000 Hz) — emotional depth
- **Reverb:** Long tails (12-20 kHz) — space, air, release

**Result:** Lead + pads + strings share midrange intentionally — fullness without mud

---

## Mix Strategy by Frequency

| Range | EQ Move | Compression | Reverb | Stereo Width |
|-------|---------|-------------|--------|-------------|
| **Sub (20-60 Hz)** | Mono, tight low-end (high-pass at 30 Hz to remove rumble) | Light compression (2:1), slow attack | NONE (reverb causes mud) | MONO ONLY |
| **Bass (60-150 Hz)** | Boost fundamental, cut mud (150-250 Hz) | Medium compression (4:1), medium attack | Minimal (10% mix, short decay) | Mono or slight width |
| **Pads (150-600 Hz)** | Cut low-mid mud (200-300 Hz), boost warmth (400 Hz) | Light compression (2:1), slow attack | Medium (30-50% mix) | WIDE (100% stereo) |
| **Lead (600-3k Hz)** | Boost presence (1-2 kHz), cut harshness (3 kHz) | Medium compression (3:1), fast attack | Medium (20-40% mix) | Narrow (30-50% width) |
| **Hi-hats (3-8k Hz)** | High-pass at 500 Hz, boost air (8 kHz) | Light compression (2:1) | Short reverb (15% mix) | Wide (80-100%) |
| **Air (8k+ Hz)** | Gentle boost (10 kHz), high-pass at 15 kHz to remove digital noise | NONE | Long reverb (reverb lives here) | WIDE |

---

## Testing Overlap Issues

### Test 1: Solo Pairs
- Solo kick + sub → Do they work together or fight?
- Solo bass + pads → Is bass clear or muddy?
- Solo lead + pads → Does lead sit on top or get buried?

### Test 2: Spectrum Analyzer
- Visual: Are multiple elements stacking at the same frequency?
- If yes: Decide which OWNS that range, EQ the others

### Test 3: Mono Check
- Sum to mono → What disappears?
- If bass/kick disappear: Phase issues, fix with EQ or timing
- If lead disappears: Stereo width too wide, narrow it

### Test 4: Reference Track
- A/B your mix with Filteria/Pleiadians
- Where is THEIR bass sitting? (100-150 Hz usually)
- Where is THEIR lead sitting? (1-3 kHz usually)
- Match the general balance

---

## Common Mistakes

### Mistake 1: "Everything needs sub bass"
- **Wrong:** Pads, leads, arps all have content below 100 Hz
- **Right:** ONLY sub bass and kick go below 100 Hz. High-pass everything else.

### Mistake 2: "Wider is better"
- **Wrong:** Bass is 100% wide stereo
- **Right:** Bass and kick are MONO below 150 Hz. Stereo causes phase issues and weak low-end on club systems.

### Mistake 3: "Boost everything at 1 kHz for presence"
- **Wrong:** Kick, bass, pads, lead all boosted at 1 kHz
- **Right:** Pick ONE element to own 1 kHz per section. Everything else cuts or stays neutral.

### Mistake 4: "Reverb on everything for depth"
- **Wrong:** Reverb on sub, kick, bass
- **Right:** NO reverb below 150 Hz. Reverb on pads/leads/FX only.

---

## Quick Decision Matrix

**When two elements fight for the same frequency:**

| Situation | Who Wins | Who Adjusts | How |
|-----------|----------|-------------|-----|
| Kick vs Sub | Kick (transient) | Sub (sustain) | Sidechain sub to kick, -3 to -6 dB |
| Bass vs Pads | Bass | Pads | High-pass pads at 150 Hz, cut 200 Hz -3 dB |
| Lead vs Pads | Lead | Pads | EQ dip in pads at lead fundamental (1-2 kHz) |
| Lead vs Vocal Sample | Context-dependent | Non-priority element | Decide per section who is primary |
| Hi-hats vs Cymbals | Both (different ranges) | — | Hi-hats 3-6 kHz, cymbals 6-12 kHz |

---

## Flyin' Colors Frequency Signature

**What makes Flyin' Colors sound like Flyin' Colors:**

- **Powerful sub (30-60 Hz):** Nitzhonot-level weight
- **Aggressive bass (80-150 Hz):** Rolling 16ths, filter modulation
- **Clear midrange (1-3 kHz):** Lead and vocal samples intelligible
- **Bright highs (8-12 kHz):** Goa-style shimmer and air
- **Deep reverb (12-20 kHz):** Spatial depth, not mud

**Frequency balance target:**
- Sub/Bass: 35% of energy
- Mids (pads/leads): 40% of energy
- Highs (hats/cymbals/air): 25% of energy

**Check with:** Pink noise reference (equal energy per octave) — your mix should be slightly bass-heavy but not boomy.

---

**Use this chart every mix session. Print it. Tape it to your wall.**
