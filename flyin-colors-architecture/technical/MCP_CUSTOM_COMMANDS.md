# Custom MCP Commands — Flyin' Colors Extensions

**Base:** Fork of `ahujasid/ableton-mcp` (MIT License)
**Purpose:** Flyin' Colors-specific commands layered on top of existing Ableton MCP
**Repository:** `AviFlyin/ableton-mcp-flyin-colors` (to be created)

---

## Implementation Priority

### Phase 1: Core Workflow (Week 1-2) — **BUILD THESE FIRST**
1. `create_flyin_colors_session` — Base template
2. `generate_rolling_bass` — Signature sound
3. `set_section_markers` — Narrative structure
4. `export_session_state` — Continuation workflow

**Time savings:** 30-45 min per session
**Dev time:** 16-24 hours

### Phase 2: Narrative + Mix (Week 3-4)
5. `generate_goa_arp` — Melodic sequences
6. `apply_narrative_arc` — Emotional automation
7. `apply_frequency_ownership` — Auto-EQ chart
8. `check_frequency_conflicts` — Mix validation

### Phase 3: Advanced Automation (Week 5-6)
9. `generate_buildup_riser` — Automated risers
10. `create_nitzhonot_bass_template` — Pre-routed bass pair
11. `import_continuation_brief` — Session restoration
12. `transition_between_sections` — Pre-built transitions

---

## Command 1: `create_flyin_colors_session` (Priority 1)

### What It Does
Creates a full Ableton session template with Flyin' Colors standard track layout, routing, and sends. Every new track starts from your blueprint.

### Input (Parameters)

```json
{
  "command": "create_flyin_colors_session",
  "params": {
    "bpm": 148,
    "key": "Dm",
    "track_name": "FC_HorrorToTriumph_01",
    "section_type": "full"
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `bpm` | int | Yes | — | Range: 140-155 (Flyin' Colors range) |
| `key` | string | Yes | — | Format: "Dm", "Am", "Em" etc. |
| `track_name` | string | Yes | — | Used for project naming + metadata |
| `section_type` | string | No | "full" | "full" = all tracks, "minimal" = kick+bass+lead only, "jam" = bass+drums only |

### Output (What Gets Created in Ableton)

**Tracks (in order):**

| # | Track Name | Type | Group | Notes |
|---|-----------|------|-------|-------|
| 1 | `FC_Kick` | MIDI | Drums | — |
| 2 | `FC_Hats` | MIDI | Drums | — |
| 3 | `FC_Perc` | MIDI | Drums | — |
| 4 | `FC_Sub` | MIDI | Bass | — |
| 5 | `FC_RollingBass` | MIDI | Bass | — |
| 6 | `FC_Lead` | MIDI | Melodic | — |
| 7 | `FC_Pad` | MIDI | Melodic | — |
| 8 | `FC_Arp` | MIDI | Melodic | — |
| 9 | `FC_FX` | Audio | FX | For risers, impacts, samples |
| 10 | `FC_Vocal` | Audio | FX | For Hebrew samples, vocal textures |
| 11 | `FC_Reference` | Audio | — | Muted. For reference track A/B |

**Return Tracks:**

| # | Send Name | Default Effect | Notes |
|---|----------|----------------|-------|
| A | `FC_Reverb_Short` | Reverb (0.8s decay) | For percussion, rhythmic elements |
| B | `FC_Reverb_Long` | Reverb (3.5s decay) | For pads, atmospheric elements |
| C | `FC_Delay` | Ping-Pong Delay (1/8 note) | For leads, arps |
| D | `FC_Distortion` | Saturator (medium drive) | For Horror sections, aggressive textures |

**Also sets:**
- Session BPM to `bpm` parameter
- Locator at bar 1: `[track_name] - [key] - [bpm]BPM`

### Response (Returned to Claude)

```json
{
  "status": "success",
  "tracks_created": 11,
  "return_tracks_created": 4,
  "bpm": 148,
  "message": "Session FC_HorrorToTriumph_01 ready. 11 tracks + 4 sends."
}
```

### Error Cases

| Error | Cause | Response |
|-------|-------|----------|
| `bpm_out_of_range` | BPM < 100 or > 200 | Warning + creates anyway |
| `session_not_empty` | Existing tracks present | Ask user: overwrite or append? |
| `ableton_not_connected` | Socket timeout | Standard connection error |

---

## Command 2: `generate_rolling_bass` (Priority 2)

### What It Does
Generates a MIDI clip with a rolling 16th-note bass pattern and places it on the specified track. Core Flyin' Colors sound.

### Input (Parameters)

```json
{
  "command": "generate_rolling_bass",
  "params": {
    "track_index": 4,
    "clip_slot": 0,
    "key": "D",
    "octave": 2,
    "scale": "natural_minor",
    "bars": 4,
    "pattern_type": "rolling_16th",
    "velocity_pattern": [100, 85, 95, 80],
    "chord_progression": ["i", "bVI", "bVII", "i"],
    "bars_per_chord": 1,
    "filter_hint": "closed"
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `track_index` | int | Yes | — | Which track to place clip on |
| `clip_slot` | int | No | 0 | Scene/clip slot index |
| `key` | string | Yes | — | Root note: "C", "D", "E" etc. |
| `octave` | int | No | 2 | MIDI octave (2 = bass range) |
| `scale` | string | No | "natural_minor" | "natural_minor", "harmonic_minor", "phrygian_dominant", "chromatic" |
| `bars` | int | No | 4 | Clip length in bars |
| `pattern_type` | string | No | "rolling_16th" | "rolling_16th", "pulsing_8th", "syncopated", "gallop" |
| `velocity_pattern` | int[] | No | [100, 85, 95, 80] | Repeating velocity cycle. Length 1-8. |
| `chord_progression` | string[] | No | ["i"] | Roman numerals. Length must match bars / bars_per_chord |
| `bars_per_chord` | int | No | 1 | How many bars before chord changes |
| `filter_hint` | string | No | "medium" | "closed" (600Hz), "medium" (900Hz), "open" (1200Hz) — metadata tag only |

### Output (What Gets Created in Ableton)

A MIDI clip containing:

**Example for D natural minor, 4 bars, i-bVI-bVII-i:**

```
Bar 1 (Dm): 16 x D2 (MIDI 38) at 16th intervals
  Velocities: 100, 85, 95, 80, 100, 85, 95, 80, 100, 85, 95, 80, 100, 85, 95, 80

Bar 2 (Bb): 16 x Bb1 (MIDI 34) at 16th intervals
  Velocities: [same pattern]

Bar 3 (C): 16 x C2 (MIDI 36) at 16th intervals
  Velocities: [same pattern]

Bar 4 (Dm): 16 x D2 (MIDI 38) at 16th intervals
  Velocities: [same pattern]
```

**Clip properties:**
- Name: `FC_Bass_[key]m_[bpm]_[pattern_type]`
- Length: `bars` bars
- Loop: ON
- Color: Orange (bass identity color)

### Response

```json
{
  "status": "success",
  "clip_name": "FC_Bass_Dm_148_rolling_16th",
  "track_index": 4,
  "clip_slot": 0,
  "notes_placed": 64,
  "bars": 4,
  "root_notes_used": ["D2", "Bb1", "C2", "D2"],
  "midi_note_numbers": [38, 34, 36, 38]
}
```

### Pattern Type Definitions

| Pattern | Rhythm | Character | Use For |
|---------|--------|-----------|---------|
| `rolling_16th` | Every 16th note, single root | Mechanical, relentless | Horror, main drops |
| `pulsing_8th` | Every 8th note, root + octave alternating | Pumping, Nitzhonot-style | Defiance energy |
| `syncopated` | 16ths with accent on off-beats | Groovy, human | Transitions, breakdowns |
| `gallop` | 16th-16th-8th repeating | Aggressive, nu-metal-influenced | Horror→Defiance transitions |

### Scale Degree → Note Mapping (Built Into Command)

For key of D:

| Degree | Natural Minor | Harmonic Minor | Phrygian Dominant |
|--------|--------------|----------------|-------------------|
| i | D | D | D |
| bII | — | — | Eb |
| ii° | E | E | — |
| bIII | F | F | F# |
| III | — | — | — |
| iv | G | G | G |
| V | — | A (major!) | A |
| v | A | — | — |
| bVI | Bb | Bb | Bb |
| bVII | C | — | C |
| vii° | — | C# | — |

---

## Command 3: `set_section_markers` (Priority 3)

### What It Does
Creates Ableton locators (arrangement markers) from your narrative arc map. Bridges narrative workflow to Ableton timeline.

### Input (Parameters)

```json
{
  "command": "set_section_markers",
  "params": {
    "clear_existing": true,
    "markers": [
      {"bar": 1, "label": "INTRO - Silence/Dread", "color": "red", "phase": "horror"},
      {"bar": 17, "label": "BUILDUP 1 - Machine Awakens", "color": "red", "phase": "horror"},
      {"bar": 33, "label": "DROP 1 - Full Horror", "color": "red", "phase": "horror"},
      {"bar": 65, "label": "BREAKDOWN - Human Voice Emerges", "color": "yellow", "phase": "transition"},
      {"bar": 81, "label": "BUILDUP 2 - Defiance Rising", "color": "orange", "phase": "defiance"},
      {"bar": 97, "label": "DROP 2 - Full Defiance", "color": "orange", "phase": "defiance"},
      {"bar": 129, "label": "BREAKDOWN 2 - Reflection", "color": "yellow", "phase": "transition"},
      {"bar": 145, "label": "BUILDUP 3 - Triumph Incoming", "color": "green", "phase": "triumph"},
      {"bar": 161, "label": "DROP 3 - Full Triumph", "color": "green", "phase": "triumph"},
      {"bar": 193, "label": "OUTRO - Release/Afterglow", "color": "blue", "phase": "triumph"}
    ]
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `clear_existing` | bool | No | false | Remove all existing locators first |
| `markers` | object[] | Yes | — | Array of marker objects |
| `markers[].bar` | int | Yes | — | Bar number (1-indexed) |
| `markers[].label` | string | Yes | — | Locator text. Max 50 chars. |
| `markers[].color` | string | No | "gray" | "red", "orange", "yellow", "green", "blue", "gray" |
| `markers[].phase` | string | No | — | Metadata: "horror", "defiance", "triumph", "transition" |

### Output (What Gets Created in Ableton)

Locators (cue points) in arrangement view at specified bar positions.

### Response

```json
{
  "status": "success",
  "markers_created": 10,
  "cleared_existing": true,
  "total_bars": 208,
  "phases": {
    "horror": {"start": 1, "end": 64, "bars": 64},
    "defiance": {"start": 81, "end": 128, "bars": 48},
    "triumph": {"start": 145, "end": 208, "bars": 64}
  }
}
```

### Preset Templates (Shortcut)

Instead of defining every marker, use a preset:

```json
{
  "command": "set_section_markers",
  "params": {
    "preset": "standard_three_act",
    "total_bars": 208,
    "drop_count": 3
  }
}
```

| Preset | Description | Sections |
|--------|-------------|----------|
| `standard_three_act` | Horror→Defiance→Triumph with 3 drops | 10 markers |
| `two_drop` | Shorter track, 2 drops | 7 markers |
| `extended_breakdown` | Long emotional breakdown between drops | 12 markers |
| `fast_capture` | Minimal: just intro/main/outro | 3 markers |

---

## Command 4: `export_session_state` (Priority 4)

### What It Does
Reads current Ableton session and exports as JSON + markdown that maps to CONTINUATION_BRIEF_TEMPLATE.

### Input (Parameters)

```json
{
  "command": "export_session_state",
  "params": {
    "output_format": "both",
    "output_path": "C:\\Users\\Avi\\Desktop\\GoAI\\session-states\\",
    "include_midi_summary": true,
    "include_automation_summary": true
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `output_format` | string | No | "both" | "json", "markdown", "both" |
| `output_path` | string | No | Current directory | Where to save files |
| `include_midi_summary` | bool | No | true | Summarize MIDI clip contents |
| `include_automation_summary` | bool | No | true | List automated parameters |

### Output (Two Files Generated)

**File 1: `session_state_[timestamp].json`**

```json
{
  "version": "1.0",
  "exported_at": "2026-02-14T22:30:00+02:00",
  "session": {
    "bpm": 148,
    "time_signature": "4/4",
    "total_tracks": 11,
    "total_scenes": 8,
    "song_length_bars": 208
  },
  "tracks": [
    {
      "index": 0,
      "name": "FC_Kick",
      "type": "midi",
      "volume_db": -3.2,
      "devices": ["Drum Rack"],
      "clips": [
        {
          "slot": 0,
          "name": "FC_Kick_Main",
          "length_bars": 4,
          "note_count": 16
        }
      ]
    }
  ]
}
```

**File 2: `session_state_[timestamp].md`**

Auto-generated markdown for CONTINUATION_BRIEF_TEMPLATE:

```markdown
# SESSION STATE — Auto-exported
**Exported:** 2026-02-14 22:30 IST
**BPM:** 148 | **Tracks:** 11 | **Length:** 208 bars

## Elements Placed
| Track | Has MIDI? | Devices? | Automation? | Status |
|-------|-----------|----------|-------------|--------|
| FC_Kick | ✅ (16 notes) | ✅ Drum Rack | ❌ | Looping |
| FC_RollingBass | ✅ (64 notes) | ✅ Serum | ✅ Filter | Looping |
...

## Completion Estimate
- Tracks with content: 2/11 (18%)
- Tracks with automation: 1/11 (9%)
```

### Response

```json
{
  "status": "success",
  "json_path": "C:\\...\\session_state_20260214_2230.json",
  "markdown_path": "C:\\...\\session_state_20260214_2230.md",
  "summary": {
    "tracks_with_content": 2,
    "completion_pct": 18
  }
}
```

---

## Command 5: `generate_goa_arp` (Priority 5)

### What It Does
Generates arpeggiated MIDI pattern in Filteria/Pleiadians style.

### Input (Parameters)

```json
{
  "command": "generate_goa_arp",
  "params": {
    "track_index": 7,
    "clip_slot": 0,
    "key": "D",
    "octave_start": 3,
    "octave_range": 2,
    "scale": "natural_minor",
    "bars": 4,
    "rate": "16th",
    "direction": "up_down",
    "chord_tones": ["1", "3", "5", "7"],
    "velocity_range": [70, 110],
    "velocity_shape": "saw_up",
    "note_length_pct": 75
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `track_index` | int | Yes | — | Target track |
| `clip_slot` | int | No | 0 | Scene/clip slot |
| `key` | string | Yes | — | Root note |
| `octave_start` | int | No | 3 | Starting octave |
| `octave_range` | int | No | 2 | Octaves to span (1-3) |
| `scale` | string | No | "natural_minor" | Scale type |
| `bars` | int | No | 4 | Clip length |
| `rate` | string | No | "16th" | "8th", "16th", "32nd", "16th_triplet" |
| `direction` | string | No | "up" | "up", "down", "up_down", "random_seed" |
| `chord_tones` | string[] | No | ["1","3","5"] | Scale degrees: "1"=root, "3"=third, etc. |
| `velocity_range` | int[2] | No | [70, 110] | [min, max] velocity |
| `velocity_shape` | string | No | "saw_up" | "saw_up", "saw_down", "flat", "random" |
| `note_length_pct` | int | No | 80 | Note length %. 100=legato, 50=staccato |

### Direction Patterns

| Direction | Pattern (for 1-3-5) | Character |
|-----------|---------------------|-----------|
| `up` | 1-3-5-1'-3'-5' | Classic Goa, uplifting |
| `down` | 5'-3'-1'-5-3-1 | Descending, melancholic |
| `up_down` | 1-3-5-1'-5-3-1 | Filteria-style flowing |
| `random_seed` | Seeded random | Psychedelic |

### Response

```json
{
  "status": "success",
  "clip_name": "FC_Arp_Dm_16th_up_down",
  "notes_placed": 128,
  "octave_range": "D3-D5",
  "unique_pitches": 8
}
```

---

## Command 6: `apply_narrative_arc` (Priority 6)

### What It Does
Adjusts track parameters to match emotional phase. Narrative arc becomes automation.

### Input (Parameters)

```json
{
  "command": "apply_narrative_arc",
  "params": {
    "phase": "horror",
    "bar_start": 1,
    "bar_end": 64,
    "intensity": 0.8
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `phase` | string | Yes | — | "horror", "defiance", "triumph", "transition" |
| `bar_start` | int | Yes | — | First bar |
| `bar_end` | int | Yes | — | Last bar |
| `intensity` | float | No | 0.7 | 0.0=subtle, 1.0=extreme |

### Phase Definitions (What Gets Changed)

**Horror:**

| Parameter | Target | Reason |
|-----------|--------|--------|
| Bass filter cutoff | 600-800 Hz | Dark, constrained |
| Reverb send (long) | Low (0.1) | Dry, claustrophobic |
| Distortion send | High (0.5-0.7) | Aggressive texture |
| Pad volume | -6 dB | Sparse, cold |
| Lead | Muted | Absent hope |

**Defiance:**

| Parameter | Target | Reason |
|-----------|--------|--------|
| Bass filter cutoff | 900-1200 Hz | Full range, aggressive |
| Reverb send (long) | Medium (0.25) | Building space |
| Distortion send | Medium (0.3) | Controlled aggression |
| Pad volume | -3 dB | Supportive |
| Lead volume | 0 dB | Assertive |

**Triumph:**

| Parameter | Target | Reason |
|-----------|--------|--------|
| Bass filter cutoff | 800-1000 Hz | Gentler |
| Reverb send (long) | High (0.5) | Lush, spacious |
| Distortion send | Low (0.1) | Clean, clear |
| Pad volume | 0 dB | Rich harmonic bed |
| Lead volume | +1 dB | Soaring melody |

### Response

```json
{
  "status": "success",
  "phase": "horror",
  "bars_affected": "1-64",
  "parameters_set": 8,
  "automation_points_created": 16
}
```

---

## Command 7: `apply_frequency_ownership` (Priority 7)

### What It Does
Applies FREQUENCY_RANGE_OWNERSHIP.md EQ chart to all tracks automatically.

### Input (Parameters)

```json
{
  "command": "apply_frequency_ownership",
  "params": {
    "strict_mode": true,
    "apply_to_tracks": "all"
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `strict_mode` | bool | No | true | true=hard cuts (24dB/oct), false=gentle (12dB/oct) |
| `apply_to_tracks` | string | No | "all" | "all", "empty_only" (only tracks without EQ) |

### Frequency Ownership Chart (Applied)

| Track Role | High-Pass | Low-Pass | Reason |
|------------|-----------|----------|--------|
| Sub Bass | 20 Hz | 80 Hz | Sine wave only |
| Rolling Bass | 80 Hz | 200 Hz | Core bass energy |
| Kick | 40 Hz | 8 kHz | Overlaps with sub (intentional) |
| Pad | 300 Hz | 8 kHz | Carved out of bass |
| Lead | 800 Hz | — | High-mid focus |
| Arp | 1 kHz | — | Top-end energy |

### Response

```json
{
  "status": "success",
  "tracks_processed": 11,
  "eq_added": 3,
  "eq_modified": 8,
  "strict_mode": true
}
```

---

## Command 8: `check_frequency_conflicts` (Priority 8)

### What It Does
Analyzes all track EQs and flags violations of frequency ownership chart.

### Input (Parameters)

```json
{
  "command": "check_frequency_conflicts",
  "params": {
    "report_mode": "detailed"
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `report_mode` | string | No | "summary" | "summary" or "detailed" |

### Response

```json
{
  "status": "success",
  "conflicts": [
    {
      "track_1": "Pad",
      "track_2": "Rolling Bass",
      "conflict_range": "80-200 Hz",
      "severity": "high",
      "recommendation": "High-pass Pad to 300 Hz minimum"
    }
  ],
  "conflict_count": 1
}
```

---

## Command 9: `generate_buildup_riser` (Priority 9)

### What It Does
Generates automated pitch rise + filter sweep for buildups.

### Input (Parameters)

```json
{
  "command": "generate_buildup_riser",
  "params": {
    "track_index": 9,
    "start_bar": 17,
    "length_bars": 16,
    "pitch_rise_semitones": 24,
    "filter_sweep": true,
    "intensity": 0.8
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `track_index` | int | Yes | — | Target track (usually FX) |
| `start_bar` | int | Yes | — | Where riser begins |
| `length_bars` | int | No | 16 | Riser length |
| `pitch_rise_semitones` | int | No | 24 | Pitch rise amount (24=2 octaves) |
| `filter_sweep` | bool | No | true | Add filter cutoff automation |
| `intensity` | float | No | 0.7 | 0.0=subtle, 1.0=extreme |

### Creates

- MIDI clip with single held note (C2)
- Pitch bend automation (0 → pitch_rise_semitones)
- Filter cutoff automation (200Hz → 8kHz) if enabled
- Volume automation (fade in, exponential curve)

### Response

```json
{
  "status": "success",
  "clip_created": true,
  "automation_envelopes": 3,
  "pitch_rise": 24,
  "bars": "17-32"
}
```

---

## Command 10: `create_nitzhonot_bass_template` (Priority 10)

### What It Does
Creates pre-routed rolling bass + sub bass track pair with sidechain.

### Input (Parameters)

```json
{
  "command": "create_nitzhonot_bass_template",
  "params": {
    "key": "Dm",
    "scale": "harmonic_minor",
    "group_name": "Bass Group"
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `key` | string | Yes | — | E.g., "Dm", "Am" |
| `scale` | string | No | "harmonic_minor" | Scale type |
| `group_name` | string | No | "Bass Group" | Track group name |

### Creates

```
Bass Group (track group)
├── Rolling Bass
│   ├── Serum (loaded)
│   ├── EQ Eight (HP @ 80Hz, LP @ 200Hz)
│   └── Compressor (sidechain to kick)
└── Sub Bass
    ├── Operator (sine wave)
    ├── EQ Eight (HP @ 20Hz, LP @ 80Hz)
    └── Compressor (sidechain to kick, faster attack)
```

### Response

```json
{
  "status": "success",
  "group_created": true,
  "tracks_in_group": 2,
  "sidechain_configured": true
}
```

---

## Command 11: `import_continuation_brief` (Priority 11)

### What It Does
Restores session context from continuation brief (reverse of export_session_state).

### Input (Parameters)

```json
{
  "command": "import_continuation_brief",
  "params": {
    "brief_path": "C:\\Users\\Avi\\Desktop\\GoAI\\session-states\\session_state_20260214.json",
    "restore_mode": "markers_only"
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `brief_path` | string | Yes | — | Path to JSON brief |
| `restore_mode` | string | No | "markers_only" | "markers_only" or "full" |

### Restore Modes

- **markers_only:** Set tempo, create locators, set key
- **full:** Also create tracks, load instruments, set send levels

### Response

```json
{
  "status": "success",
  "tempo_set": 148,
  "markers_created": 10,
  "tracks_created": 0,
  "restore_mode": "markers_only"
}
```

---

## Command 12: `transition_between_sections` (Priority 12)

### What It Does
Inserts pre-built transition patterns between sections.

### Input (Parameters)

```json
{
  "command": "transition_between_sections",
  "params": {
    "bar_position": 64,
    "type": "filter_sweep",
    "duration_bars": 2
  }
}
```

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `bar_position` | int | Yes | — | Where transition occurs |
| `type` | string | Yes | — | "filter_sweep", "impact_hit", "reverse_cymbal", "silence_drop" |
| `duration_bars` | int | No | 2 | Transition length |

### Transition Types

| Type | Effect |
|------|--------|
| `filter_sweep` | Master filter cutoff: 8kHz → 200Hz descending |
| `impact_hit` | Places impact sample + reverb automation |
| `reverse_cymbal` | Places reverse cymbal leading into bar_position |
| `silence_drop` | Volume to -inf 1 beat before, snap back at bar_position |

### Response

```json
{
  "status": "success",
  "type": "filter_sweep",
  "bar_position": 64,
  "automation_created": true
}
```

---

## Implementation Notes

### Fork Strategy

1. Fork `ahujasid/ableton-mcp` → `AviFlyin/ableton-mcp-flyin-colors`
2. Keep all existing commands untouched
3. Add `src/flyin_colors/` module for custom commands
4. Register in existing command handler

### Directory Structure

```
ableton-mcp-flyin-colors/
├── src/
│   ├── ableton_mcp/          # Original (keep updated)
│   └── flyin_colors/          # Custom extensions
│       ├── __init__.py
│       ├── template_commands.py    # Commands 1, 10
│       ├── midi_generation.py      # Commands 2, 5, 9
│       ├── narrative_commands.py   # Commands 3, 6, 12
│       ├── session_commands.py     # Commands 4, 11
│       ├── mix_commands.py         # Commands 7, 8
│       └── utils/
│           ├── scale_mappings.py
│           └── frequency_ownership.py
├── config/
│   ├── frequency_ownership.json
│   └── scale_definitions.json
└── tests/
    └── flyin_colors/
```

### Dependencies on Base Commands

| Custom Command | Uses Base Commands |
|---------------|-------------------|
| `create_flyin_colors_session` | `create_midi_track`, `set_tempo` |
| `generate_rolling_bass` | `create_clip`, `add_notes_to_clip` |
| `set_section_markers` | `create_cue_point` (may need to add) |
| `export_session_state` | `get_session_info`, `get_track_info` |

### Missing from ahujasid (May Need to Add)

| Missing | Needed By | Workaround |
|---------|-----------|------------|
| `create_cue_point` | set_section_markers | Use AbletonOSC directly |
| `get_device_parameters` | export_session_state | Query via OSC |
| `create_return_track` | create_flyin_colors_session | PR #26 adds this |

---

## Testing Strategy

### Smoke Test (After Each Command)

1. `create_flyin_colors_session` → Verify 11 tracks + 4 sends
2. `generate_rolling_bass` → Verify note count + pitches
3. `set_section_markers` → Verify locators in arrangement
4. `export_session_state` → Verify JSON matches session

### Integration Test (After All Commands)

```
1. create_flyin_colors_session (Dm, 148)
2. set_section_markers (standard_three_act, 208 bars)
3. generate_rolling_bass (Dm, rolling_16th, i-bVI-bVII-i)
4. generate_goa_arp (Dm, 16th, up_down)
5. apply_narrative_arc (horror, bars 1-64)
6. export_session_state
7. Verify markdown matches actual Ableton
8. Play back: sounds like Flyin' Colors?
```

---

## Development Timeline

**Week 1-2:** Commands 1-4 (core workflow)
**Week 3-4:** Commands 5-8 (narrative + mix)
**Week 5-6:** Commands 9-12 (advanced)

**Total:** 6-8 weeks for all 12 commands

---

**Next Step:** Fork repo, implement Command 1 as proof of concept.
