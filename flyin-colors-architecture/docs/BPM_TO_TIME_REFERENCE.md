# BPM to Time Conversion Reference

Quick reference for converting BPM to musical time durations + MIDI clock values.

---

## Common Trance BPMs

| BPM | Genre | 1 Bar (4 beats) | 16th Note | 16th in MIDI Ticks* |
|-----|-------|----------------|-----------|-------------------|
| 138 | Goa (slow) | 1.74 sec | 0.109 sec | 120 ticks |
| 140 | Goa (standard) | 1.71 sec | 0.107 sec | 120 ticks |
| 145 | Goa/Nitzhonot | 1.66 sec | 0.103 sec | 120 ticks |
| 148 | Nitzhonot (standard) | 1.62 sec | 0.101 sec | 120 ticks |
| 150 | Nitzhonot (fast) | 1.60 sec | 0.100 sec | 120 ticks |
| 155 | Nitzhonot (very fast) | 1.55 sec | 0.097 sec | 120 ticks |
| 160 | Psycore (entry) | 1.50 sec | 0.094 sec | 120 ticks |
| 180 | Psycore (fast) | 1.33 sec | 0.083 sec | 120 ticks |
| 200 | Psycore (extreme) | 1.20 sec | 0.075 sec | 120 ticks |

*MIDI ticks assume standard 480 PPQN (Pulses Per Quarter Note) resolution. Ableton Live uses 960 PPQN, so multiply by 2.

---

## Formulas

### Time Durations
```
Beat duration (seconds) = 60 / BPM
Bar duration (4 beats)  = (60 / BPM) * 4
16th note duration      = (60 / BPM) / 4
```

### MIDI Clock (Ticks)
```
Ticks per quarter note (PPQN) = 480 (standard) or 960 (Ableton)
Ticks per 16th note           = PPQN / 4

At 480 PPQN: 16th note = 120 ticks (regardless of BPM)
At 960 PPQN: 16th note = 240 ticks (regardless of BPM)
```

**Important:** MIDI ticks are tempo-independent. A 16th note is always 120 ticks at 480 PPQN, whether you're at 140 BPM or 180 BPM. The *time duration* changes, but the tick count doesn't.

---

## Automation Precision (MIDI Ticks)

When writing automation in Ableton via MCP server, use MIDI ticks for precision:

### Ableton Live (960 PPQN)

| Note Value | Ticks | Use Case |
|------------|-------|----------|
| Whole note (4 beats) | 3840 | Long pad sustains, breakdown chords |
| Half note (2 beats) | 1920 | Mid-length notes, bassline sustain |
| Quarter note (1 beat) | 960 | Kick placement, bassline roots |
| 8th note | 480 | Hi-hats, offbeat elements |
| 16th note | 240 | Rolling bass, arps, fast hi-hats |
| 32nd note | 120 | Rolls, fills, glitch effects |
| 64th note | 60 | Extreme precision, micro-timing |

### Example: Filter Sweep Automation

**Goal:** Sweep filter from 400Hz → 1200Hz over 8 bars at 148 BPM

**Math:**
- 8 bars at 148 BPM = 1.62 sec/bar * 8 = 12.96 seconds
- 8 bars in ticks (960 PPQN) = 3840 ticks/bar * 8 = 30,720 ticks

**MCP Command:**
```python
create_automation(
    track="Bass",
    parameter="Filter Cutoff",
    start_tick=0,
    end_tick=30720,
    start_value=400,
    end_value=1200,
    curve="exponential"
)
```

---

## Bar Count at Different BPMs

For standard track lengths (6-12 minutes):

| BPM | 6 min | 7 min | 8 min | 9 min | 10 min | 12 min |
|-----|-------|-------|-------|-------|--------|--------|
| 138 | 207 bars | 242 bars | 276 bars | 311 bars | 345 bars | 414 bars |
| 145 | 218 bars | 254 bars | 290 bars | 326 bars | 363 bars | 435 bars |
| 148 | 222 bars | 259 bars | 296 bars | 333 bars | 370 bars | 444 bars |
| 150 | 225 bars | 263 bars | 300 bars | 338 bars | 375 bars | 450 bars |

**Standard Flyin' Colors target:** 192 bars at 148 BPM = ~7:48 minutes

---

## Sync with External Hardware

If syncing Ableton with external gear via MIDI clock:

### MIDI Clock Messages
- **24 PPQN** (MIDI clock standard) — 24 clock pulses per quarter note
- Ableton sends MIDI clock at 24 PPQN regardless of internal 960 PPQN
- External gear receives 24 clock messages per beat

### Conversion
```
Ableton internal: 960 PPQN
MIDI clock out:   24 PPQN
Conversion:       960 / 24 = 40

Every 40 internal ticks = 1 MIDI clock message sent
```

**Why this matters:** If you're syncing Push 3 standalone mode or external synths, they'll lock to MIDI clock (24 PPQN), not Ableton's internal 960 PPQN.

---

## Quick Reference for Common Operations

### How many ticks for...

**At 960 PPQN (Ableton):**

| Duration | Ticks | Calculation |
|----------|-------|-------------|
| 1 beat | 960 | Base unit |
| 1 bar (4 beats) | 3840 | 960 * 4 |
| 2 bars | 7680 | 3840 * 2 |
| 4 bars | 15360 | 3840 * 4 |
| 8 bars | 30720 | 3840 * 8 |
| 16 bars | 61440 | 3840 * 16 |
| 32 bars | 122880 | 3840 * 32 |
| 64 bars | 245760 | 3840 * 64 |
| 192 bars (full track) | 737280 | 3840 * 192 |

### Triplets

| Note Value | Straight | Triplet | Ticks (Triplet @ 960 PPQN) |
|------------|----------|---------|---------------------------|
| Quarter note | 960 | 640 | 640 |
| 8th note | 480 | 320 | 320 |
| 16th note | 240 | 160 | 160 |

**Formula:** `Triplet ticks = (straight ticks / 3) * 2`

---

## Use Cases

### When to use TIME (seconds):
- Human-readable descriptions
- Audio editing (sample start/end points)
- Visualizing length of sections

### When to use BARS:
- Musical structure (intro, buildup, drop, breakdown)
- Arrangement decisions
- Handoff briefs between agents

### When to use MIDI TICKS:
- **MCP server automation commands** (most important)
- Precise MIDI note placement
- Automation curve points
- Quantization settings
- Sample-accurate timing

---

## Flyin' Colors Standards

**Default BPM:** 148 (Nitzhonot standard)
**Range:** 145-155 (Goa/Nitzhonot fusion)
**Standard track length:** 192 bars = 7:48 minutes at 148 BPM
**Ableton PPQN:** 960 (default, never change)

**When programming via MCP:**
- Always use ticks, not seconds
- 16th note = 240 ticks
- 1 bar = 3840 ticks
- Double-check: Does your automation land on musical divisions?

---

**Save this reference. You'll need it every session.**
