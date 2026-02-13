# Ableton MCP Setup — Using ahujasid/ableton-mcp

**Decision:** Use existing [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp) instead of building from scratch.

**Why:** Ship music faster. Build custom features later if needed.

---

## What This Provides

**MCP Server:** Claude Desktop → Ableton Live integration

**Available Tools:**
- ✅ Track management (create, modify MIDI/audio tracks)
- ✅ Instrument/effect loading (browse and load from Ableton library)
- ✅ Clip operations (create MIDI clips, edit notes)
- ✅ Playback control (play/stop, fire clips)
- ✅ Session parameters (tempo, time signature)
- ✅ Session information (query tracks, clips, current state)

**What you can do:**
```
You: "Create a synth bass track with Serum"
Claude: [Creates track, loads Serum from browser]

You: "Add a 4-bar MIDI clip with a Dm rolling bass pattern"
Claude: [Creates clip, adds MIDI notes]

You: "Set tempo to 148 BPM"
Claude: [Updates session tempo]
```

---

## Requirements

- ✅ Ableton Live 10+ (you have Live 12 Suite)
- ✅ Python 3.8+ (check: `python --version`)
- ✅ UV package manager (install below)

---

## Installation (30 minutes)

### Step 1: Install UV Package Manager

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify:**
```bash
uv --version
```

### Step 2: Install Ableton Remote Script

**Download the remote script:**
```bash
cd ~/Downloads
git clone https://github.com/ahujasid/ableton-mcp.git
```

**Copy to Ableton:**
```bash
# Copy __init__.py to Ableton's MIDI Remote Scripts folder
cp ableton-mcp/__init__.py "C:\Users\Avi\Documents\Ableton\User Library\Remote Scripts\AbletonMCP\"
```

**Enable in Ableton:**
1. Open Ableton Live 12 Suite
2. Preferences → Link/Tempo/MIDI → Control Surface
3. Select "AbletonMCP" from dropdown
4. Input/Output: (leave blank)
5. Restart Ableton

**Verify:**
- Ableton should show "AbletonMCP" as active control surface
- Check Ableton's Log.txt for connection messages

### Step 3: Configure Claude Desktop

**Edit Claude Desktop config:**
```bash
# Location (Windows):
# C:\Users\Avi\AppData\Roaming\Claude\claude_desktop_config.json

# Add this:
{
  "mcpServers": {
    "AbletonMCP": {
      "command": "uvx",
      "args": ["ableton-mcp"]
    }
  }
}
```

**Restart Claude Desktop**

### Step 4: Test Connection

**In Claude Desktop, ask:**
```
What tracks are currently in my Ableton session?
```

If it responds with track info, it's working.

**Test creation:**
```
Create a MIDI track called "Bass" and load Serum
```

---

## Claude Code vs Claude Desktop

**Important:** This MCP server works with **Claude Desktop**, not Claude Code (CLI).

**Current workflow:**
```
Claude Projects (web) → Creative guidance, prompts
     ↓ (manual execution)
Ableton Live → You execute manually
```

**With ableton-mcp:**
```
Claude Desktop (app) → Creative guidance + automation
     ↓ (via MCP)
Ableton Live → Automated execution
```

**To use both:**
1. Use Claude Projects for planning/creative (Shadow Creator)
2. Use Claude Desktop for execution (ableton-mcp automation)
3. Use continuation briefs to transfer context between them

---

## Available Commands (Examples)

### Track Management
```
Create a MIDI track called "Lead" with Vital loaded
Create an audio track for vocal samples
Rename track 3 to "Arp"
```

### Instruments & Effects
```
Load Serum on the Bass track
Add FabFilter Pro-Q 3 to track 1
Load a drum rack on the Drums track
```

### MIDI Clips
```
Create a 4-bar MIDI clip on track 1
Add notes: D2 (MIDI 50) at beat 1, F2 (MIDI 53) at beat 2
Generate a Dm chord progression: Dm - Bb - C - Dm over 8 bars
```

### Playback Control
```
Set tempo to 148 BPM
Start playback
Stop playback
Fire clip 1 on track 2
```

### Session Queries
```
What's the current tempo?
List all tracks in the session
Show MIDI clips on track 1
What instruments are loaded?
```

---

## Limitations

**What ableton-mcp does NOT do (yet):**
- ❌ Advanced automation curves (you'll write manually)
- ❌ Complex arrangement editing (use Ableton's arrange view)
- ❌ Mixing (EQ, compression parameters — manual for now)
- ❌ Mastering (use dedicated tools)
- ❌ Audio clip editing (sample manipulation)

**These are fine.** The 80/20 rule: automate MIDI creation, keep creative control on sound design/mix.

---

## Integration with Flyin' Colors Workflow

### Scenario 1: Starting a New Track

**Claude Projects (Shadow Creator):**
```
You: "I want to create a track about the Iron Dome"

Shadow Creator:
- Defines narrative (Horror → Defiance → Triumph)
- Provides musical blueprint (148 BPM, Dm, Harmonic Minor, progressions)
- Suggests sound design (mechanical bass, aggressive lead)
```

**Claude Desktop (ableton-mcp):**
```
You: "Create session:
- Tempo: 148 BPM
- Tracks: Kick, Sub, Bass (Serum), Lead (Vital), Pad (Kontakt), Arp (Massive)
- 4-bar MIDI clip on Bass: Dm rolling 16ths"

Claude Desktop: [Executes via MCP]
```

**You (Ableton manually):**
- Tweak Serum patch for mechanical bass sound
- Adjust filter automation
- Mix and master

### Scenario 2: Fast-Capture to Production

**Push 3:** [Jam a bass riff]

**Claude Projects (Shadow Creator fast-capture):**
```
You: "Fast capture. I jammed a dark rolling bass in Dm"
Shadow Creator: Extracts DNA, suggests development path
```

**Claude Desktop (ableton-mcp):**
```
You: "Recreate this pattern in Ableton:
- Track: Bass (Serum)
- Pattern: [describes from fast-capture brief]"

Claude Desktop: [Creates MIDI clip with pattern]
```

**You:** Tweak and refine in Ableton

---

## When to Use vs Manual Production

### Use ableton-mcp for:
- ✅ Creating tracks and loading instruments quickly
- ✅ Generating MIDI patterns from descriptions
- ✅ Setting up session structure (BPM, tracks, basic clips)
- ✅ Rapid prototyping (test 3 different bass patterns in 2 minutes)
- ✅ Tedious tasks (creating 16 tracks with naming conventions)

### Do manually for:
- ❌ Sound design (tweaking synth parameters, finding the perfect patch)
- ❌ Mixing (EQ cuts, compression, sidechain — requires ears)
- ❌ Mastering (final polish — requires reference monitoring)
- ❌ Creative exploration (jamming on Push 3, discovering happy accidents)
- ❌ Complex automation (filter sweeps with specific curves)

---

## Troubleshooting

### "MCP server not found" in Claude Desktop
```bash
# Check UV is installed
uv --version

# Try manual install
uvx ableton-mcp

# Check Claude Desktop config path is correct
cat "C:\Users\Avi\AppData\Roaming\Claude\claude_desktop_config.json"
```

### "Can't connect to Ableton" errors
```bash
# 1. Restart Ableton Live
# 2. Check Preferences → Control Surface → AbletonMCP is selected
# 3. Check Log.txt for errors:
cat "C:\Users\Avi\AppData\Roaming\Ableton\Live 12\Preferences\Log.txt" | grep -i error
```

### Remote script not showing in Ableton
```bash
# Verify file is in correct location:
ls "C:\Users\Avi\Documents\Ableton\User Library\Remote Scripts\AbletonMCP\__init__.py"

# If missing, re-copy:
cp ~/Downloads/ableton-mcp/__init__.py "C:\Users\Avi\Documents\Ableton\User Library\Remote Scripts\AbletonMCP\"
```

### Commands work but changes don't appear
- Make sure Ableton is in focus
- Try clicking in Ableton's session view
- Restart both Ableton and Claude Desktop

---

## Upgrade Path

**Phase 1 (Now):** Use ahujasid/ableton-mcp as-is
- Track creation, MIDI clips, basic automation
- Covers 80% of tedious work

**Phase 2 (After 2-3 tracks):** Fork and customize
- Add Flyin' Colors-specific tools (Nitzhonot bass generator, Goa arp builder)
- Integrate continuation brief format
- Add support for style-fingerprint constraints

**Phase 3 (Long-term):** Contribute upstream
- Submit improvements to ahujasid/ableton-mcp
- Help other producers benefit from your workflow

---

## Quick Reference

**Install:** `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` → `uvx ableton-mcp`

**Configure:** Add to `claude_desktop_config.json`:
```json
{"mcpServers": {"AbletonMCP": {"command": "uvx", "args": ["ableton-mcp"]}}}
```

**Test:** "Create a MIDI track called Test with Serum loaded"

**Docs:** https://github.com/ahujasid/ableton-mcp

---

**Next:** Install UV, set up remote script, configure Claude Desktop, test with simple track creation.
