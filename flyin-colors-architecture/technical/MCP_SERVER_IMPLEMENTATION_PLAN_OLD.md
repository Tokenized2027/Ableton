# MCP Server Implementation Plan — Flyin' Colors Automation Infrastructure

**Version:** 1.0
**Target Setup:** Single Windows PC (migrate to dual-machine later)
**Timeline:** Incremental build, 4 phases

---

## Architecture Overview

```
Claude Code (Windows) ←→ MCP Server (Python, Windows) ←→ AbletonOSC ←→ Ableton Live 12 Suite
                              ↓
                      Session State (JSON)
                              ↓
                    C:\trance-workspace\
```

---

## Phase 1: Foundation (Transport & Tracks)

**Goal:** Prove the connection works. Basic control of Ableton Live.

### Deliverables
1. AbletonOSC installed and configured
2. MCP server running locally
3. Transport control (play/stop/tempo)
4. Track creation/naming
5. Session state tracking (JSON)

### Implementation Steps

#### Step 1.1: Install AbletonOSC

**Terminal:**
```bash
cd C:\
git clone https://github.com/ideoforms/AbletonOSC.git
cp -r AbletonOSC/AbletonOSC "C:\Users\Avi\Documents\Ableton\User Library\Remote Scripts\"
```

**Ableton Setup:**
1. Open Ableton Live 12 Suite
2. Preferences → Link/Tempo/MIDI → Control Surface
3. Select "AbletonOSC" from dropdown
4. Input/Output: None (OSC uses network, not MIDI)
5. Close preferences

**Verify:**
Open Ableton's Log.txt (`C:\Users\Avi\AppData\Roaming\Ableton\Live 12\Preferences\Log.txt`)
Look for: `AbletonOSC: Listening on port 11000`

---

#### Step 1.2: Create MCP Server Scaffold

**Terminal:**
```bash
mkdir C:\trance-mcp
cd C:\trance-mcp
python -m venv venv
venv\Scripts\activate
pip install fastmcp python-osc mido numpy
```

**File: `C:\trance-mcp\server.py`**
```python
from fastmcp import FastMCP
from pythonosc import udp_client
import json, os, time

# OSC Client (sends commands to Ableton)
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 11000)

# MCP Server
mcp = FastMCP("Flyin Colors Trance Producer")

# ===== SESSION MANAGEMENT =====

@mcp.tool()
def create_session(bpm: int = 148, key: str = "Am") -> str:
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

# ===== TRANSPORT CONTROL =====

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

# ===== TRACK MANAGEMENT =====

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

# ===== STATE MANAGEMENT =====

STATE_FILE = r"C:\trance-workspace\state\session_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"session": {}, "tracks": [], "arrangement": {"sections": []}, "version_history": []}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

# ===== RUN SERVER =====

if __name__ == "__main__":
    # Create workspace folder
    os.makedirs(r"C:\trance-workspace\state", exist_ok=True)
    os.makedirs(r"C:\trance-workspace\midi", exist_ok=True)

    # Run MCP server (stdio mode for local Claude Code)
    mcp.run(transport="stdio")
```

---

#### Step 1.3: Configure Claude Code to Use MCP Server

**File: `C:\Users\Avi\.claude\mcp.json`** (or project-specific `.mcp.json`)
```json
{
  "mcpServers": {
    "flyin-colors-trance": {
      "command": "python",
      "args": ["C:\\trance-mcp\\server.py"],
      "env": {}
    }
  }
}
```

**Verify:**
```bash
claude mcp list
# Should show: flyin-colors-trance
```

---

#### Step 1.4: Test Phase 1

**In Claude Code conversation:**
```
User: "Use the flyin-colors-trance MCP server to create a session at 148 BPM in Am"

Claude: [Calls create_session(bpm=148, key="Am")]

User: "Create a track called 'Kick'"

Claude: [Calls create_track(name="Kick", track_type="midi")]

User: "Set tempo to 150 BPM"

Claude: [Calls set_tempo(bpm=150)]

User: "Play"

Claude: [Calls play()]
```

**Verify in Ableton:**
- Tempo should be 150 BPM
- Track named "Kick" should exist
- Playback should start

**Phase 1 Success Criteria:**
✅ MCP server connects to Claude Code
✅ Commands reach Ableton via OSC
✅ State is saved to JSON
✅ Transport control works

---

## Phase 2: MIDI Generation & Placement

**Goal:** Generate and place MIDI patterns in Ableton.

### New Deliverables
1. MIDI pattern generation (basslines, arps, drums)
2. MIDI note placement via OSC
3. Clip creation and management
4. Pattern library (reusable templates)

### Implementation

**Add to `server.py`:**

```python
# ===== MIDI PLACEMENT =====

@mcp.tool()
def place_midi(track_name: str, bar_start: int, bar_length: int, notes: str) -> str:
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
    scene_idx = (bar_start - 1) // 16  # Simplified scene mapping

    osc_client.send_message("/live/clip_slot/create_clip",
                            [track_idx, scene_idx, float(clip_length)])
    time.sleep(0.2)

    # Add notes
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

    return f"Placed {len(note_list)} notes on '{track_name}' at bar {bar_start}"

def find_track(state, name):
    name_lower = name.lower()
    for t in state["tracks"]:
        if t["name"].lower() == name_lower:
            return t
    return None

# ===== MIDI GENERATION =====

@mcp.tool()
def generate_rolling_bass(key: str, bar_start: int, bar_length: int) -> str:
    """Generate rolling Nitzhonot 16th-note bassline."""
    # Convert key to MIDI note (simple mapping)
    key_to_midi = {"A": 57, "C": 60, "D": 62, "E": 64, "F": 65, "G": 67}
    root_note = key_to_midi.get(key[0].upper(), 57)

    notes = []
    for bar in range(bar_length):
        for beat in range(4):
            for sixteenth in range(4):
                velocity = 100 if sixteenth == 0 else 85  # Accent on downbeats
                notes.append({
                    "pitch": root_note,
                    "velocity": velocity,
                    "start_beat": bar * 4 + beat + sixteenth * 0.25,
                    "duration_beats": 0.2  # Slight overlap for legato
                })

    return json.dumps(notes)

# Example high-level generator
@mcp.tool()
def create_bass_pattern(track_name: str, key: str, bar_start: int, bar_length: int) -> str:
    """Generate and place rolling bass pattern."""
    notes_json = generate_rolling_bass(key, 0, bar_length)  # Generate relative to 0
    return place_midi(track_name, bar_start, bar_length, notes_json)
```

**Test Phase 2:**
```
User: "Create a track called 'Bass'"
User: "Generate a rolling bass pattern in Am from bar 33 for 16 bars"

Claude: [Calls create_track("Bass") then create_bass_pattern("Bass", "Am", 33, 16)]

User: "Play from bar 33"
```

**Phase 2 Success Criteria:**
✅ MIDI patterns generated algorithmically
✅ Notes placed in Ableton clips
✅ Patterns play correctly in Ableton

---

## Phase 3: Arrangement Automation

**Goal:** Automate full track structure creation.

### New Deliverables
1. Arrangement structure definition
2. Element muting/unmuting by section
3. Trance template creation (full track layout)
4. Section-based workflow

### Implementation

**Add to `server.py`:**

```python
@mcp.tool()
def create_trance_template() -> str:
    """Create full Flyin' Colors track template."""
    tracks = [
        ("Kick", "drums"), ("Clap", "drums"), ("Hats", "drums"), ("Perc", "drums"),
        ("Bass", "bass"), ("Sub", "bass"),
        ("Lead 1", "lead"), ("Lead 2", "lead"),
        ("Pad", "pad"), ("Atmosphere", "pad"),
        ("Arp 1", "arp"), ("Arp 2", "arp"),
        ("FX Riser", "fx"), ("FX Impact", "fx"),
    ]

    for i, (name, track_type) in enumerate(tracks):
        create_track(name, track_type)
        time.sleep(0.1)

    return f"Created {len(tracks)} tracks"

@mcp.tool()
def create_arrangement(structure: str) -> str:
    """
    Create full song arrangement.

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

    total_bars = current_bar - 1
    bpm = state["session"]["bpm"]
    duration_min = (total_bars * 4) / bpm

    return f"Arrangement created ({total_bars} bars, ~{duration_min:.1f} min)"
```

---

## Phase 4: Automation & Push 3 Integration

**Goal:** Parameter automation and Push 3 control.

### New Deliverables
1. Filter sweeps, volume risers
2. Automation curve creation
3. Push 3 parameter mapping
4. Push 3 standalone mode integration

### Implementation

**Add to `server.py`:**

```python
import numpy as np

@mcp.tool()
def create_filter_sweep(track_name: str, bar_start: int, bar_end: int, direction: str = "up") -> str:
    """
    Create filter cutoff automation sweep.
    direction: 'up' (opening) or 'down' (closing)
    """
    state = load_state()
    track = find_track(state, track_name)
    if not track:
        return f"Error: Track '{track_name}' not found"

    num_points = (bar_end - bar_start) * 4  # One point per beat
    if direction == "up":
        values = [float(np.power(i / num_points, 2)) for i in range(num_points + 1)]
    else:
        values = [float(1.0 - np.power(i / num_points, 0.5)) for i in range(num_points + 1)]

    track_idx = track["index"]
    for i, val in enumerate(values):
        beat_pos = (bar_start - 1) * 4 + i
        osc_client.send_message("/live/device/set/parameters/value", [
            track_idx, 0,  # First device on track
            1,  # Parameter index (filter cutoff, device-specific)
            float(val)
        ])
        time.sleep(0.01)

    return f"Filter sweep {direction} on '{track_name}': bars {bar_start}-{bar_end}"
```

**Phase 4 Note:** Push 3 integration requires additional research into Push 3's MIDI/OSC capabilities or Ableton's Push scripting API.

---

## Migration to Dual-Machine Setup (Future)

When mini PC ("bosegame") arrives:

1. **Install Tailscale** on both machines
2. **Move MCP server** to network mode:
   ```python
   mcp.run(transport="streamable-http", host="0.0.0.0", port=8765)
   ```
3. **Update Claude Code config** on bosegame:
   ```json
   {
     "mcpServers": {
       "flyin-colors-trance": {
         "command": "npx",
         "args": ["@anthropic-ai/mcp-proxy", "http://[WINDOWS-TAILSCALE-IP]:8765"]
       }
     }
   }
   ```
4. **Test connectivity** via Tailscale VPN

---

## Testing Checklist

**Phase 1:**
- [ ] AbletonOSC installed
- [ ] MCP server runs
- [ ] Transport control works (play/stop/tempo)
- [ ] Track creation works
- [ ] State saved to JSON

**Phase 2:**
- [ ] MIDI patterns generated
- [ ] Notes placed in Ableton
- [ ] Clips play correctly
- [ ] Pattern variations work

**Phase 3:**
- [ ] Template creation works
- [ ] Arrangement structure defined
- [ ] Section-based workflow functional

**Phase 4:**
- [ ] Filter sweeps automated
- [ ] Volume risers automated
- [ ] Push 3 parameters controlled

---

**Implementation starts when System Architect agent is activated by Shadow Creator.**
