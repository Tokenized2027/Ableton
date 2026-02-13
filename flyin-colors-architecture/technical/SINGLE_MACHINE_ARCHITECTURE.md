# Single-Machine Architecture — Flyin' Colors (Current Setup)

**Platform:** Windows PC
**Components:** Ableton Live 12 Suite + Claude Code + MCP Server (all local)
**Future Migration:** Dual-machine setup when mini PC arrives

---

## System Overview

```
┌────────────────────────────────────────────────────────────┐
│                    Windows PC (Single Machine)              │
│                                                            │
│  Claude Code ←→ MCP Server ←→ AbletonOSC ←→ Ableton Live  │
│      │              │                             │        │
│      │              ↓                             │        │
│      │      Session State (JSON)                 │        │
│      │      C:\trance-workspace\                 │        │
│      │                                            │        │
│      └─────────────── You interact ──────────────┘        │
│                                                            │
│  Push 3 ←──USB──→ Ableton Live (hands-on control)         │
│                                                            │
│  RME Fireface UCX II ←──USB──→ Ableton (audio I/O)        │
│           │                                                │
│           ↓                                                │
│    Dynaudio Core 7 (monitoring)                            │
└────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Claude Code (Local)
- **Location:** Installed on Windows PC
- **Function:** AI agent coordination, MIDI generation logic, decision-making
- **Communication:** Calls MCP server via stdio (local process)

### 2. MCP Server (Python, Local)
- **Location:** `C:\trance-mcp\server.py`
- **Function:** Bridges Claude Code ↔ Ableton Live
- **Communication:** stdio (Claude Code) + OSC (Ableton Live)
- **Tools Provided:** Transport control, track creation, MIDI placement, automation

### 3. AbletonOSC (MIDI Remote Script)
- **Location:** `C:\Users\Avi\Documents\Ableton\User Library\Remote Scripts\AbletonOSC\`
- **Function:** Exposes Ableton Live's API via OSC protocol
- **Ports:** Receives on UDP 11000, sends on UDP 11001
- **Communication:** OSC messages from MCP server

### 4. Ableton Live 12 Suite
- **Function:** DAW, hosts all plugins and audio processing
- **Receives:** OSC commands from AbletonOSC
- **Outputs:** Audio to RME Fireface UCX II

### 5. Session State (JSON)
- **Location:** `C:\trance-workspace\state\session_state.json`
- **Function:** Tracks current project state (tracks, clips, arrangement)
- **Updated by:** MCP server after every operation
- **Read by:** Claude Code agents to understand current state

---

## File Structure

```
C:\
├── trance-mcp\
│   ├── server.py (MCP server)
│   ├── venv\ (Python virtual environment)
│   └── requirements.txt
│
├── trance-workspace\
│   ├── state\
│   │   └── session_state.json
│   ├── midi\
│   │   └── [generated MIDI files]
│   ├── audio\
│   │   └── [rendered bounces]
│   ├── masters\
│   │   └── [final masters]
│   └── exports\
│       └── [deliverable packages]
│
└── Users\Avi\
    ├── Desktop\
    │   └── Ableton Projects\
    │       └── Flyin Colors\
    │           └── [project folders]
    ├── Documents\
    │   └── Ableton\
    │       └── User Library\
    │           └── Remote Scripts\
    │               └── AbletonOSC\
    └── .claude\
        └── mcp.json (MCP server configuration)
```

---

## Data Flow

### Example: Creating a Rolling Bassline

```
1. Avi: "Create a rolling bass in Am from bar 33 for 16 bars"
   ↓
2. Claude Code (Shadow Creator):
   - Understands request
   - Activates MIDI Producer agent (or generates directly)
   ↓
3. MIDI Producer generates pattern:
   - Uses music theory (Am = MIDI 57)
   - Creates 16th-note pattern with velocity accents
   - Outputs JSON: [{"pitch": 57, "velocity": 100, "start_beat": 0, ...}, ...]
   ↓
4. Claude Code calls MCP tool:
   - create_bass_pattern("Bass", "Am", 33, 16)
   ↓
5. MCP Server (server.py):
   - Receives tool call
   - Sends OSC to AbletonOSC: /live/clip_slot/create_clip
   - Sends OSC to AbletonOSC: /live/clip/add/notes (for each note)
   - Updates session_state.json
   ↓
6. AbletonOSC:
   - Receives OSC messages
   - Calls Ableton Live's internal API
   ↓
7. Ableton Live:
   - Creates MIDI clip on "Bass" track
   - Adds notes to clip
   - Displays in arrangement view
   ↓
8. Avi sees the bassline in Ableton, can play it immediately
```

---

## Advantages of Single-Machine Setup

1. **No network latency** — Everything local, instant response
2. **Simpler setup** — No Tailscale, no IP configuration
3. **Easier debugging** — All logs on one machine
4. **Works offline** — No internet required

---

## Migration Path to Dual-Machine

When mini PC arrives:

### Changes Required

1. **MCP Server:** Change from `stdio` to `http` transport
   ```python
   # Current (single-machine):
   mcp.run(transport="stdio")

   # Future (dual-machine):
   mcp.run(transport="streamable-http", host="0.0.0.0", port=8765)
   ```

2. **Claude Code Config:** Point to network MCP server
   ```json
   // Current (single-machine):
   {
     "mcpServers": {
       "flyin-colors-trance": {
         "command": "python",
         "args": ["C:\\trance-mcp\\server.py"]
       }
     }
   }

   // Future (dual-machine):
   {
     "mcpServers": {
       "flyin-colors-trance": {
         "command": "npx",
         "args": ["@anthropic-ai/mcp-proxy", "http://[WINDOWS-TAILSCALE-IP]:8765"]
       }
     }
   }
   ```

3. **Tailscale:** Install on both machines, connect to same network

4. **File Sync:** Set up shared folder (Syncthing or Tailscale file sharing)

---

## Hardware Connections

### RME Fireface UCX II
- **Connection:** USB to Windows PC
- **Outputs:** Analog 1-2 → Dynaudio Core 7 (L/R)
- **Sample Rate:** 48 kHz (Ableton session rate)
- **Buffer Size:** 128-256 samples (balance latency vs. CPU)

### Ableton Push 3
- **Connection:** USB to Windows PC
- **Mode:** Controller mode (connected to Ableton)
- **Function:** MIDI input, parameter control, scene launching
- **Standalone:** Can disconnect and use independently for sketching

### Dynaudio Core 7
- **Connection:** XLR from RME Fireface (balanced)
- **Placement:** Optimized listening position
- **Volume:** Controlled via RME TotalMix or Ableton master

---

## Performance Considerations

### CPU Usage
- **Ableton Live:** 40-60% (with plugins loaded)
- **Claude Code:** Minimal (text processing)
- **MCP Server:** <5% (lightweight Python)
- **Total:** Should stay under 80% to avoid dropouts

### RAM
- **Ableton Live:** 4-8 GB (with large sample libraries)
- **System:** 16 GB minimum recommended, 32 GB ideal

### Storage
- **SSD required** for Ableton projects and sample libraries
- Fast read/write for real-time audio playback

---

## Key Principles

1. **Everything local** — Low latency, high reliability
2. **Simple to debug** — All components on one machine
3. **Migration-ready** — Code structured to easily move to dual-machine
4. **Hands-on hardware** — Push 3 keeps workflow tactile and musical
5. **Professional monitoring** — RME + Dynaudio ensure accurate listening

---

**This setup is operational immediately. Dual-machine migration is straightforward when mini PC arrives.**
