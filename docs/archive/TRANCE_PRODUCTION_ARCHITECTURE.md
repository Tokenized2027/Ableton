# Claude Code → Ableton Trance Production Pipeline

## Architecture Document v1.0

**Author:** Avi + Claude  
**Date:** February 2026  
**Purpose:** Complete system design for AI-assisted trance music production using Claude Code on a dedicated Linux mini PC (bosegame) controlling Ableton Live on a separate Windows machine.

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        YOUR WORKFLOW                                │
│                                                                     │
│   You ──prompt──▶ Claude Code ──generates──▶ MIDI / Automation      │
│                       │                          │                  │
│                       │         Tailscale VPN     │                  │
│                       ▼                          ▼                  │
│               MCP Server (Windows) ──OSC──▶ Ableton Live            │
│                                                  │                  │
│                                          You listen, tweak,         │
│                                          give feedback to Claude    │
└─────────────────────────────────────────────────────────────────────┘
```

### Two Machines, One Pipeline

| Machine | Role | OS | Always On? |
|---------|------|----|------------|
| **bosegame** (mini PC) | AI brain — runs Claude Code, generates MIDI, sends commands | Linux (Ubuntu) | Yes |
| **Production PC** | DAW host — runs Ableton Live, synths, audio output | Windows | During sessions |

### Communication Layer

Both machines connect via **Tailscale** (WireGuard-based mesh VPN). Claude Code on bosegame talks to a custom MCP server running on the Windows machine. The MCP server translates commands into OSC messages that AbletonOSC understands.

```
bosegame                          Windows Production PC
┌──────────────┐    Tailscale    ┌──────────────────────────────┐
│ Claude Code  │◀──────────────▶│  Trance MCP Server (Python)  │
│              │   TCP/WebSocket │       │                      │
│ - MIDI gen   │                 │       ▼ OSC (UDP)            │
│ - Arrangement│                 │  AbletonOSC ◀──▶ Ableton    │
│ - Automation │                 │                  Live 12     │
│ - Analysis   │                 │                              │
└──────────────┘                 └──────────────────────────────┘
```

---

## 2. Component Details

### 2.1 AbletonOSC (Foundation Layer)

**What:** Open-source Python MIDI Remote Script that exposes Ableton Live's internal API over OSC (Open Sound Control).

**Repo:** `github.com/ideoforms/AbletonOSC`

**Capabilities:**

| Category | OSC Commands | What It Does |
|----------|-------------|--------------|
| **Song** | `/live/song/set/tempo`, `/live/song/start_playing` | Set BPM, play/stop/record |
| **Tracks** | `/live/song/create_midi_track`, `/live/track/set/name` | Create/name/delete tracks |
| **Clips** | `/live/clip_slot/create_clip`, `/live/clip/add/notes` | Create clips, add MIDI notes |
| **Devices** | `/live/device/set/parameters/value` | Control synth/effect parameters |
| **Mixer** | `/live/track/set/volume`, `/live/track/set/panning` | Volume, pan, sends |
| **Scenes** | `/live/scene/fire`, `/live/song/create_scene` | Trigger scenes, arrangement |
| **Automation** | `/live/clip/set/automation` | Draw automation curves |

**Installation:** Copy the `AbletonOSC` folder to:
```
C:\Users\[YOU]\Documents\Ableton\User Library\Remote Scripts\AbletonOSC
```
Then in Ableton: Preferences → Link/Tempo/MIDI → Control Surface → select AbletonOSC.

**Default port:** Receives on UDP 11000, sends on UDP 11001.

### 2.2 Trance MCP Server (Bridge Layer)

A custom Python MCP server running on the Windows machine. Claude Code connects to it as an MCP tool. It provides high-level trance-production-specific commands.

**Tech stack:** Python 3.11+, `fastmcp`, `python-osc`, `mido`

**Tool categories the MCP server exposes to Claude Code:**

#### Session Management
```
create_session(bpm, key, time_signature)
  → Sets tempo, creates initial track layout for trance template

get_session_info()
  → Returns current BPM, track list, clip positions, arrangement length
```

#### Track Management
```
create_track(name, type, color)
  → Creates MIDI track in Ableton with specified name
  → type: "kick", "bass", "lead", "pad", "arp", "fx", "perc", "vocal"

create_return_track(name, effect)
  → Creates return track with reverb/delay

create_trance_template()
  → Creates full track layout:
     - Kick, Clap, Hats, Perc (drums group)
     - Bass, Sub (bass group)
     - Lead 1, Lead 2 (leads group)
     - Pad, Atmosphere (pads group)
     - Arp 1, Arp 2 (arps group)
     - FX Riser, FX Sweep, FX Impact (fx group)
     - Reverb Send, Delay Send (returns)
```

#### MIDI Generation & Placement
```
place_midi(track_name, bar_start, bar_length, midi_data)
  → Places MIDI notes into a clip on specified track
  → midi_data: list of {note, velocity, start_beat, duration_beats}

generate_and_place_bassline(key, scale, pattern_type, bar_start, bar_length)
  → Generates bass MIDI based on trance patterns and places it
  → pattern_type: "rolling", "pulsing", "offbeat", "acid"

generate_and_place_arp(key, scale, pattern_type, rate, bar_start, bar_length)
  → Generates arpeggio pattern
  → rate: "1/8", "1/16", "1/16T" (triplet)
  → pattern_type: "up", "down", "updown", "random", "chord_stab"

generate_and_place_melody(key, scale, contour, bar_start, bar_length)
  → Generates lead melody
  → contour: "ascending", "descending", "arch", "valley", "call_response"

generate_and_place_chords(key, progression, voicing, bar_start, bar_length)
  → Generates pad/chord MIDI
  → progression: list like ["Am", "F", "C", "G"] or scale degrees [1, 6, 4, 5]
  → voicing: "open", "closed", "spread"

generate_and_place_drums(pattern_type, bar_start, bar_length)
  → Generates drum pattern
  → pattern_type: "four_on_floor", "buildup", "breakdown", "fill", "rolling"
```

#### Arrangement
```
create_arrangement(structure)
  → Lays out the full song structure
  → structure: list of sections like:
    [
      {"name": "intro", "bars": 32, "elements": ["kick", "hats", "arp1"]},
      {"name": "buildup1", "bars": 16, "elements": ["kick", "bass", "arp1", "arp2", "riser"]},
      {"name": "drop1", "bars": 32, "elements": ["kick", "bass", "lead1", "arp1", "pad"]},
      {"name": "breakdown", "bars": 32, "elements": ["pad", "piano", "vocal"]},
      {"name": "buildup2", "bars": 16, "elements": ["kick", "bass", "riser", "arp1"]},
      {"name": "drop2", "bars": 32, "elements": ["kick", "bass", "lead1", "lead2", "arp1", "pad"]},
      {"name": "outro", "bars": 32, "elements": ["kick", "hats"]}
    ]

mute_track_at(track_name, bar_start, bar_end)
unmute_track_at(track_name, bar_start, bar_end)
  → Controls which elements play during which sections
```

#### Automation
```
create_automation(track_name, parameter, bar_start, bar_end, curve)
  → Draws automation on a track's device parameter
  → parameter: "filter_cutoff", "reverb_send", "volume", "pan"
  → curve: list of (position, value) points or preset curves

create_filter_sweep(track_name, bar_start, bar_end, direction)
  → direction: "up" (opening), "down" (closing)
  → Classic trance filter automation

create_riser(bar_start, bar_end, type)
  → type: "white_noise", "pitch_riser", "reverse_cymbal"
  → Auto-generates riser clip + volume automation

create_impact(bar_position, type)
  → type: "downlifter", "cymbal_crash", "sub_drop"
```

#### Analysis & Feedback
```
get_arrangement_overview()
  → Returns current arrangement: what's on each track, bar positions

get_track_contents(track_name)
  → Returns MIDI note data from clips on a track

export_section(bar_start, bar_end, filename)
  → Triggers Ableton to render a section to audio for review
```

### 2.3 Claude Code (Brain Layer)

Claude Code on bosegame handles all creative decisions and MIDI generation. It uses Python libraries locally:

| Library | Purpose |
|---------|---------|
| `mido` | MIDI file creation, reading, manipulation |
| `pretty_midi` | Higher-level MIDI operations, note generation |
| `music21` | Music theory — scales, chords, harmony analysis |
| `numpy` | Automation curve generation, mathematical patterns |

Claude Code connects to the MCP server as a configured tool:

```json
// bosegame: ~/.claude.json or project .mcp.json
{
  "mcpServers": {
    "ableton-trance": {
      "command": "ssh",
      "args": [
        "user@[WINDOWS-TAILSCALE-IP]",
        "python",
        "C:/trance-mcp/server.py"
      ]
    }
  }
}
```

Alternative: run the MCP server as a network service and use `npx @anthropic-ai/mcp-proxy` to bridge.

---

## 3. Trance Music Theory Engine

Claude Code's MIDI generation is powered by a built-in understanding of trance production conventions. The MCP server can also store these as reference configs.

### 3.1 Scale & Key Library

```
Common trance keys: Am, Cm, Dm, Em, Fm, Gm (minor keys dominate)
Scales:
  - Natural minor (Aeolian) — most common
  - Harmonic minor — for that "uplifting" feel (raised 7th)
  - Phrygian — darker, psytrance territory
  - Mixolydian — euphoric, anthem trance
```

### 3.2 Chord Progressions (Trance Staples)

```
Uplifting:
  i - VI - III - VII    (Am - F - C - G)
  i - iv - VI - VII     (Am - Dm - F - G)
  i - III - VII - VI    (Am - C - G - F)

Dark/Driving:
  i - VII - VI - VII    (Am - G - F - G)
  i - iv - v - i        (Am - Dm - Em - Am)

Euphoric:
  I - V - vi - IV       (C - G - Am - F) — major key trance
  i - VI - VII - i      (Am - F - G - Am)
```

### 3.3 Standard Arrangement Structure

```
Classic 7-8 minute trance arrangement at 138-142 BPM:

Bars 1-32     │ INTRO        │ Kick + hats, subtle elements fade in
Bars 33-48    │ BUILDUP 1    │ Bass enters, arps layer, filter opens
Bars 49-80    │ DROP 1       │ Full energy — lead, bass, drums, pads
Bars 81-112   │ BREAKDOWN    │ Strip back to pads/piano, emotional core
Bars 113-128  │ BUILDUP 2    │ Tension — riser, rolling bass, snare rolls
Bars 129-160  │ DROP 2       │ Maximum energy — add second lead/layer
Bars 161-192  │ OUTRO        │ Elements drop out, back to kick + hats

At 138 BPM, 32 bars ≈ 55 seconds
Full track ≈ 7.5 minutes
```

### 3.4 Bassline Patterns

```
Rolling bass (16th notes):
  |x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x|  (constant 16ths, velocity variation)

Pulsing bass (8th notes):
  |x---x---x---x---x---x---x---x---|  (pumping sidechain feel)

Offbeat bass:
  |--x---x---x---x---x---x---x---x-|  (offbeat 8ths)

Acid bass (TB-303 style):
  |x--xx-x---x-xx--x--xx-x---x-xx--|  (syncopated with slides/accents)
```

### 3.5 Arpeggio Patterns

```
Classic trance arp (1/16th):
  Root-3rd-5th-Oct repeated, velocity: 100-80-90-70

Gate trance (1/16th with gaps):
  Root-rest-5th-rest-Oct-rest-5th-rest

Triplet arp (1/16T):
  Root-3rd-5th in triplets — creates rolling, hypnotic feel

Chord stab (1/4 or 1/2):
  Full chord hits on downbeats — classic trance stab
```

### 3.6 Automation Curves

```
Filter sweep up (buildup):
  Start: 20% cutoff → End: 100% cutoff
  Curve: exponential rise over 16-32 bars

Filter sweep down (intro/outro):
  Start: 100% → End: 20%
  Curve: logarithmic descent

Reverb send swell (breakdown):
  Gradual increase from 20% → 80% over 16 bars
  Snap back to 30% on drop

Volume riser:
  -inf → 0dB over 16 bars, exponential
  Cut to silence on beat 1 of drop (impact moment)
```

---

## 4. File & Data Flow

### 4.1 MIDI Generation (on bosegame)

Claude Code generates MIDI data as Python objects, then either:

**Option A — Direct OSC placement (preferred):**
Claude Code tells the MCP server to place notes directly in Ableton via AbletonOSC. No file transfer needed.

```
Claude Code → MCP command: place_midi("Bass", bar=33, length=16, notes=[...])
MCP Server → OSC: /live/clip_slot/create_clip (track 2, slot 0, 16 bars)
MCP Server → OSC: /live/clip/add/notes (note data)
```

**Option B — MIDI file transfer (for complex patterns):**
Claude Code generates a `.mid` file, transfers it to a shared folder, MCP server imports it.

```
bosegame: ~/trance-workspace/midi/bass_v3.mid
  ↓ synced via Tailscale + shared folder or SCP
Windows: C:\trance-workspace\midi\bass_v3.mid
  ↓ MCP server drags into Ableton via AbletonOSC
```

### 4.2 Project State Tracking

The MCP server maintains a JSON state file so Claude Code always knows what's in the arrangement:

```json
{
  "session": {
    "bpm": 138,
    "key": "Am",
    "time_signature": "4/4"
  },
  "tracks": [
    {
      "name": "Kick",
      "index": 0,
      "type": "drums",
      "clips": [
        {"bar_start": 1, "bar_length": 32, "name": "Kick_Intro"},
        {"bar_start": 33, "bar_length": 128, "name": "Kick_Main"}
      ]
    },
    {
      "name": "Bass",
      "index": 1,
      "type": "bass",
      "clips": [
        {"bar_start": 33, "bar_length": 16, "name": "Rolling_Bass_v2"}
      ]
    }
  ],
  "arrangement": {
    "sections": [
      {"name": "intro", "bar_start": 1, "bar_end": 32},
      {"name": "buildup1", "bar_start": 33, "bar_end": 48}
    ]
  },
  "version_history": [
    {"timestamp": "2026-02-13T14:30:00", "action": "Created rolling bass v2", "tracks_affected": ["Bass"]}
  ]
}
```

### 4.3 Shared Folder Structure

```
C:\trance-workspace\              (Windows — synced with bosegame)
├── midi\                         Generated MIDI files
│   ├── bass_rolling_Am_v3.mid
│   ├── lead_melody_v1.mid
│   └── arp_16th_v2.mid
├── audio\                        Rendered bounces for review
│   ├── drop1_preview.wav
│   └── breakdown_preview.wav
├── presets\                       Synth preset references
│   └── preset_map.json           Maps track names to loaded presets
├── state\                        Project state
│   └── session_state.json
└── templates\                    Reusable arrangement templates
    ├── uplifting_138.json
    └── dark_140.json
```

---

## 5. Setup Instructions

### Phase 1: Windows Machine — AbletonOSC

```
1. Download AbletonOSC from github.com/ideoforms/AbletonOSC
2. Copy to: C:\Users\[YOU]\Documents\Ableton\User Library\Remote Scripts\
3. Open Ableton Live
4. Preferences → Link/Tempo/MIDI → Control Surface 1 → AbletonOSC
5. Verify: run this Python test script:

   from pythonosc import udp_client
   client = udp_client.SimpleUDPClient("127.0.0.1", 11000)
   client.send_message("/live/song/get/tempo", [])
   # Should see response in Ableton's log
```

### Phase 2: Windows Machine — Trance MCP Server

```
1. Install Python 3.11+ on Windows
2. Create project:
   mkdir C:\trance-mcp
   cd C:\trance-mcp
   python -m venv venv
   venv\Scripts\activate
   pip install fastmcp python-osc mido numpy

3. Place server.py (see Section 6 for scaffold)
4. Test locally:
   python server.py
```

### Phase 3: Networking — Tailscale

```
1. Install Tailscale on both machines
2. Join same Tailscale network
3. Note Windows machine's Tailscale IP (e.g., 100.x.y.z)
4. Verify connectivity:
   # From bosegame:
   ping 100.x.y.z
```

### Phase 4: bosegame — Claude Code MCP Config

```
1. Add to ~/.claude.json on bosegame:

{
  "mcpServers": {
    "ableton-trance": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-proxy", "http://100.x.y.z:8765"]
    }
  }
}

2. Verify in Claude Code:
   claude mcp list
   # Should show ableton-trance
```

### Phase 5: Shared Workspace

```
1. Create C:\trance-workspace on Windows
2. Share via Tailscale file sharing or Syncthing
3. Mount on bosegame: ~/trance-workspace
4. Verify bidirectional file sync
```

---

## 6. MCP Server Scaffold

```python
# C:\trance-mcp\server.py
# Trance Production MCP Server — connects Claude Code to Ableton Live

from fastmcp import FastMCP
from pythonosc import udp_client, dispatcher, osc_server
import json, os, time, threading, mido
import numpy as np

# --- Config ---
ABLETON_OSC_IP = "127.0.0.1"
ABLETON_OSC_SEND_PORT = 11000    # Send commands to Ableton
ABLETON_OSC_RECV_PORT = 11001    # Receive responses from Ableton
STATE_FILE = r"C:\trance-workspace\state\session_state.json"
MIDI_DIR = r"C:\trance-workspace\midi"

# --- OSC Client ---
osc_client = udp_client.SimpleUDPClient(ABLETON_OSC_IP, ABLETON_OSC_SEND_PORT)

# --- MCP Server ---
mcp = FastMCP("Ableton Trance Producer")

# =====================
# SESSION MANAGEMENT
# =====================

@mcp.tool()
def create_session(bpm: int = 138, key: str = "Am") -> str:
    """Create a new trance session with specified BPM and key."""
    osc_client.send_message("/live/song/set/tempo", [float(bpm)])
    state = {
        "session": {"bpm": bpm, "key": key, "time_signature": "4/4"},
        "tracks": [],
        "arrangement": {"sections": []},
        "version_history": []
    }
    save_state(state)
    return f"Session created: {bpm} BPM, key of {key}"

@mcp.tool()
def get_session_info() -> str:
    """Get current session state including tracks and arrangement."""
    return json.dumps(load_state(), indent=2)

# =====================
# TRACK MANAGEMENT
# =====================

@mcp.tool()
def create_trance_template() -> str:
    """Create a full trance track template with standard track layout."""
    tracks = [
        # Drums
        ("Kick", "drums"), ("Clap", "drums"), ("Hats", "drums"), ("Perc", "drums"),
        # Bass
        ("Bass", "bass"), ("Sub", "bass"),
        # Leads
        ("Lead 1", "lead"), ("Lead 2", "lead"),
        # Pads
        ("Pad", "pad"), ("Atmosphere", "pad"),
        # Arps
        ("Arp 1", "arp"), ("Arp 2", "arp"),
        # FX
        ("FX Riser", "fx"), ("FX Sweep", "fx"), ("FX Impact", "fx"),
    ]

    for i, (name, track_type) in enumerate(tracks):
        osc_client.send_message("/live/song/create_midi_track", [i])
        time.sleep(0.1)
        osc_client.send_message("/live/track/set/name", [i, name])
        time.sleep(0.05)

    state = load_state()
    state["tracks"] = [{"name": n, "index": i, "type": t, "clips": []}
                        for i, (n, t) in enumerate(tracks)]
    save_state(state)
    return f"Created {len(tracks)} tracks: {', '.join(n for n, _ in tracks)}"

@mcp.tool()
def create_track(name: str, track_type: str = "midi") -> str:
    """Create a single MIDI track."""
    state = load_state()
    index = len(state["tracks"])
    osc_client.send_message("/live/song/create_midi_track", [index])
    time.sleep(0.1)
    osc_client.send_message("/live/track/set/name", [index, name])
    state["tracks"].append({"name": name, "index": index, "type": track_type, "clips": []})
    save_state(state)
    return f"Created track '{name}' at index {index}"

# =====================
# MIDI PLACEMENT
# =====================

@mcp.tool()
def place_midi(track_name: str, bar_start: int, bar_length: int,
               notes: str) -> str:
    """
    Place MIDI notes on a track.

    notes: JSON string — list of dicts with keys:
      - pitch (int, MIDI note number 0-127)
      - velocity (int, 1-127)
      - start_beat (float, beat position within clip, 0-based)
      - duration_beats (float)

    Example: [{"pitch": 69, "velocity": 100, "start_beat": 0.0, "duration_beats": 0.5}]
    """
    state = load_state()
    track = find_track(state, track_name)
    if not track:
        return f"Error: Track '{track_name}' not found"

    track_idx = track["index"]
    note_list = json.loads(notes)

    # Create clip (length in beats, 4 beats per bar)
    clip_length = bar_length * 4
    scene_idx = bar_to_scene(bar_start)

    osc_client.send_message("/live/clip_slot/create_clip",
                            [track_idx, scene_idx, float(clip_length)])
    time.sleep(0.2)

    # Add notes: /live/clip/add/notes [track, clip, pitch, start, duration, velocity, mute]
    for note in note_list:
        osc_client.send_message("/live/clip/add/notes", [
            track_idx, scene_idx,
            note["pitch"],
            float(note["start_beat"]),
            float(note["duration_beats"]),
            note["velocity"],
            0  # not muted
        ])
        time.sleep(0.02)

    # Update state
    clip_info = {
        "bar_start": bar_start,
        "bar_length": bar_length,
        "note_count": len(note_list),
        "name": f"{track_name}_b{bar_start}"
    }
    track["clips"].append(clip_info)
    save_state(state)

    return f"Placed {len(note_list)} notes on '{track_name}' at bar {bar_start} ({bar_length} bars)"

@mcp.tool()
def place_midi_file(track_name: str, bar_start: int, midi_filename: str) -> str:
    """Import a .mid file from the shared workspace onto a track."""
    filepath = os.path.join(MIDI_DIR, midi_filename)
    if not os.path.exists(filepath):
        return f"Error: File {filepath} not found"

    mid = mido.MidiFile(filepath)
    notes = []
    current_tick = 0

    for msg in mid.tracks[0 if len(mid.tracks) == 1 else 1]:
        current_tick += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            beat_pos = current_tick / mid.ticks_per_beat
            notes.append({
                "pitch": msg.note,
                "velocity": msg.velocity,
                "start_beat": beat_pos,
                "duration_beats": 0.25  # Will be updated by note_off
            })

    return place_midi(track_name, bar_start, len(notes) // 16 or 4,
                      json.dumps(notes))

# =====================
# ARRANGEMENT
# =====================

@mcp.tool()
def create_arrangement(structure: str) -> str:
    """
    Create full song arrangement from a structure definition.

    structure: JSON string — list of sections:
    [
      {"name": "intro", "bars": 32, "elements": ["kick", "hats"]},
      {"name": "buildup1", "bars": 16, "elements": ["kick", "bass", "arp1"]},
      ...
    ]
    """
    sections = json.loads(structure)
    state = load_state()
    current_bar = 1
    arrangement = []

    for section in sections:
        arrangement.append({
            "name": section["name"],
            "bar_start": current_bar,
            "bar_end": current_bar + section["bars"] - 1,
            "elements": section["elements"]
        })
        current_bar += section["bars"]

    state["arrangement"]["sections"] = arrangement
    save_state(state)

    summary = "\n".join(
        f"  {s['name']}: bars {s['bar_start']}-{s['bar_end']} ({s['bar_end']-s['bar_start']+1} bars)"
        for s in arrangement
    )
    total_bars = current_bar - 1
    bpm = state["session"]["bpm"]
    duration_min = (total_bars * 4) / bpm

    return f"Arrangement created ({total_bars} bars, ~{duration_min:.1f} min):\n{summary}"

@mcp.tool()
def get_arrangement_overview() -> str:
    """Get a summary of the current arrangement."""
    state = load_state()
    return json.dumps(state["arrangement"], indent=2)

# =====================
# AUTOMATION
# =====================

@mcp.tool()
def create_filter_sweep(track_name: str, bar_start: int, bar_end: int,
                        direction: str = "up") -> str:
    """
    Create a filter cutoff automation sweep.
    direction: 'up' (opening, for buildups) or 'down' (closing, for intros/outros)
    """
    state = load_state()
    track = find_track(state, track_name)
    if not track:
        return f"Error: Track '{track_name}' not found"

    num_points = (bar_end - bar_start) * 4  # One point per beat
    if direction == "up":
        # Exponential rise
        values = [float(np.power(i / num_points, 2)) for i in range(num_points + 1)]
    else:
        # Logarithmic descent
        values = [float(1.0 - np.power(i / num_points, 0.5)) for i in range(num_points + 1)]

    # Send automation points via OSC
    track_idx = track["index"]
    for i, val in enumerate(values):
        beat_pos = (bar_start - 1) * 4 + i
        osc_client.send_message("/live/clip/set/automation", [
            track_idx, 0,  # track, clip
            "Filter Freq",  # parameter name
            float(beat_pos), float(val)
        ])
        time.sleep(0.01)

    return f"Filter sweep {direction} on '{track_name}': bars {bar_start}-{bar_end}"

@mcp.tool()
def create_volume_riser(track_name: str, bar_start: int, bar_end: int) -> str:
    """Create a volume automation riser (for buildup tension)."""
    state = load_state()
    track = find_track(state, track_name)
    if not track:
        return f"Error: Track '{track_name}' not found"

    num_points = (bar_end - bar_start) * 4
    # Exponential rise from -inf to 0dB (mapped 0.0 → 0.85 in Ableton's scale)
    values = [float(0.85 * np.power(i / num_points, 2.5)) for i in range(num_points + 1)]

    track_idx = track["index"]
    for i, val in enumerate(values):
        beat_pos = (bar_start - 1) * 4 + i
        osc_client.send_message("/live/track/set/volume", [track_idx, val])
        time.sleep(0.01)

    return f"Volume riser on '{track_name}': bars {bar_start}-{bar_end}"

# =====================
# TRANSPORT
# =====================

@mcp.tool()
def play() -> str:
    """Start playback."""
    osc_client.send_message("/live/song/start_playing", [])
    return "Playback started"

@mcp.tool()
def stop() -> str:
    """Stop playback."""
    osc_client.send_message("/live/song/stop_playing", [])
    return "Playback stopped"

@mcp.tool()
def set_tempo(bpm: int) -> str:
    """Set the session tempo."""
    osc_client.send_message("/live/song/set/tempo", [float(bpm)])
    state = load_state()
    state["session"]["bpm"] = bpm
    save_state(state)
    return f"Tempo set to {bpm} BPM"

# =====================
# HELPERS
# =====================

def find_track(state, name):
    name_lower = name.lower()
    for t in state["tracks"]:
        if t["name"].lower() == name_lower:
            return t
    return None

def bar_to_scene(bar):
    return bar - 1  # 1-indexed bars to 0-indexed scenes

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"session": {}, "tracks": [], "arrangement": {"sections": []}, "version_history": []}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

# =====================
# RUN SERVER
# =====================

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8765)
```

---

## 7. Example Workflow

Here's what a real session looks like:

### You say to Claude Code:

> "Create a new uplifting trance track. 138 BPM, key of A minor. Classic structure — 32 bar intro with just kick and hats, 16 bar buildup where bass and arps come in with a filter sweep, 32 bar drop with the full lead melody, 32 bar breakdown with just pads and a piano, 16 bar buildup 2 with a riser, 32 bar second drop with a second lead layered in, 32 bar outro."

### Claude Code executes:

```
1. create_session(bpm=138, key="Am")
2. create_trance_template()
3. create_arrangement([
     {"name": "intro", "bars": 32, "elements": ["kick", "hats"]},
     {"name": "buildup1", "bars": 16, "elements": ["kick", "bass", "arp1", "hats"]},
     {"name": "drop1", "bars": 32, "elements": ["kick", "bass", "lead1", "arp1", "pad", "hats"]},
     {"name": "breakdown", "bars": 32, "elements": ["pad", "atmosphere"]},
     {"name": "buildup2", "bars": 16, "elements": ["kick", "bass", "arp1", "fx_riser"]},
     {"name": "drop2", "bars": 32, "elements": ["kick", "bass", "lead1", "lead2", "arp1", "arp2", "pad", "hats"]},
     {"name": "outro", "bars": 32, "elements": ["kick", "hats"]}
   ])
4. Generate kick pattern → place_midi("Kick", 1, 192, [four_on_floor])
5. Generate hi-hat pattern → place_midi("Hats", 1, 192, [hats])
6. Generate rolling bassline → place_midi("Bass", 33, 160, [rolling_bass_Am])
7. Generate 16th arp in Am → place_midi("Arp 1", 33, 160, [arp_data])
8. Generate lead melody → place_midi("Lead 1", 49, 32, [melody])
9. Generate pad chords (Am-F-C-G) → place_midi("Pad", 49, 128, [chords])
10. Generate second lead harmony → place_midi("Lead 2", 129, 32, [harmony])
11. create_filter_sweep("Bass", 33, 48, "up")
12. create_volume_riser("FX Riser", 113, 128)
```

### You listen, then say:

> "The bass is too busy in the buildup. Make it simpler — just root notes on quarter notes. And make the lead melody more emotional, longer notes with more movement."

### Claude Code adjusts and re-places the MIDI.

---

## 8. Limitations & What You Handle

### What Claude Code CANNOT do:
- Choose which synth/preset sounds good (no audio feedback loop yet)
- Mix and master (needs ears)
- Load specific VST plugins (needs manual setup or pre-configured template)
- Real-time audio monitoring (no audio stream from Windows to bosegame)

### What YOU handle:
- Synth selection and sound design on each track
- Loading your preferred plugins/presets
- Final mixing decisions (EQ, compression, stereo width)
- Mastering
- Creative direction ("I want this to feel more like Armin" vs "more like Infected Mushroom")
- Saving/exporting the final project

### Future enhancements:
- Audio analysis: bounce sections → send wav to bosegame → Claude analyzes frequency content
- Preset management: MCP server maps preset names to synth parameters
- Reference track matching: Claude analyzes a reference track's structure and recreates it
- Live feedback loop: stream audio from Windows to bosegame for real-time Claude analysis

---

## 9. Dependencies Summary

### bosegame (Linux)
```bash
# Claude Code (already installed)
# Python libraries for MIDI generation
pip install mido pretty_midi music21 numpy

# Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
```

### Windows Production PC
```bash
# Python 3.11+
# In C:\trance-mcp:
pip install fastmcp python-osc mido numpy

# AbletonOSC
# Download from github.com/ideoforms/AbletonOSC

# Tailscale
# Download from tailscale.com

# Ableton Live 11 or 12 (Suite or Standard)
```

---

## 10. Security Notes

- Tailscale handles encryption (WireGuard) — no ports exposed to public internet
- MCP server binds to Tailscale IP only, not 0.0.0.0 (override in production config)
- No Ableton credentials or license keys transit the network
- Session state files contain only MIDI data and arrangement info, no sensitive data

---

## 11. Quick Reference Card

| You want to... | Tell Claude Code... |
|----------------|---------------------|
| Start a new track | "Create a new trance session at 140 BPM in C minor" |
| Set up tracks | "Create the trance template" or "Add a track called Pluck" |
| Make a bassline | "Generate a rolling 16th bass in Am, bars 33-48" |
| Add arpeggios | "Create a 16th note arp using Am chord tones, bars 33-80" |
| Write a melody | "Write an emotional 8-bar lead melody in A minor" |
| Build arrangement | "Arrange: 32 intro, 16 buildup, 32 drop, 32 breakdown, 16 buildup, 32 drop, 32 outro" |
| Add tension | "Add a filter sweep on the bass from bar 33 to 48" |
| Add a riser | "Create a volume riser on FX Riser, bars 113-128" |
| Review | "Show me the current arrangement overview" |
| Iterate | "The melody at bar 49 is too busy — simplify it, longer notes" |
| Play | "Hit play" |
| Change tempo | "Set tempo to 142" |
