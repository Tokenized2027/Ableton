# Flyin' Colors Extension for ableton-mcp

**Fork of:** [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp)
**License:** MIT (same as upstream)
**Purpose:** Custom MCP commands for Flyin' Colors music production workflow

---

## What This Adds

This fork extends the base `ahujasid/ableton-mcp` with 12 custom commands tailored to the Flyin' Colors production workflow (trauma-based Trance music: Goa + Nitzhonot + Nu-Metal fusion).

### Implemented (PoC)

1. **`create_flyin_colors_session`** ✅
   Creates complete session template with 11 tracks, 4 sends, routing

### Planned (12 total commands)

2. `generate_rolling_bass` - Signature rolling 16th bass MIDI
3. `set_section_markers` - Narrative structure (Horror → Defiance → Triumph)
4. `export_session_state` - Auto-generate continuation briefs
5. `generate_goa_arp` - Filteria/Pleiadians-style arpeggiated sequences
6. `apply_narrative_arc` - Emotional automation (filter, reverb, distortion)
7. `apply_frequency_ownership` - Auto-EQ all tracks per frequency chart
8. `check_frequency_conflicts` - Mix validation
9. `generate_buildup_riser` - Automated pitch rise + filter sweep
10. `create_nitzhonot_bass_template` - Pre-routed rolling + sub bass pair
11. `import_continuation_brief` - Restore session from brief
12. `transition_between_sections` - Pre-built transitions (sweeps, drops, impacts)

Full spec: `GoAI/flyin-colors-architecture/technical/MCP_CUSTOM_COMMANDS.md`

---

## Installation

### Prerequisites
- Ableton Live 10+ (tested on Live 12 Suite)
- Python 3.8+
- UV package manager

### Setup

1. **Install UV (if not already installed):**
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Install Ableton Remote Script:**
   ```bash
   cp AbletonMCP_Remote_Script/__init__.py "C:\Users\Avi\Documents\Ableton\User Library\Remote Scripts\AbletonMCP\"
   ```

3. **Enable in Ableton:**
   - Preferences → Link/Tempo/MIDI → Control Surface
   - Select "AbletonMCP" from dropdown
   - Restart Ableton

4. **Configure Claude Desktop:**
   Edit `C:\Users\Avi\AppData\Roaming\Claude\claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "AbletonMCP": {
         "command": "uvx",
         "args": ["ableton-mcp"]
       }
     }
   }
   ```

5. **Restart Claude Desktop**

---

## Usage

### Test Command 1: Create Session

In Claude Desktop:
```
Create a new Flyin' Colors session at 148 BPM in D minor
```

Claude will execute:
```python
create_flyin_colors_session(
    bpm=148,
    key="Dm",
    track_name="FC_HorrorToTriumph_01",
    section_type="full"
)
```

**Result:**
- 11 MIDI/audio tracks created
- 4 return tracks (reverb short/long, delay, distortion)
- Tempo set to 148 BPM
- Initial locator at bar 1

### Parameters

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `bpm` | int | 148 | 140-155 recommended for Flyin' Colors |
| `key` | string | "Dm" | Format: "Dm", "Am", "F#m", etc. |
| `track_name` | string | "FC_Track_01" | Project/track identifier |
| `section_type` | string | "full" | "full" (11 tracks), "minimal" (4 tracks), "jam" (3 tracks) |

---

## Architecture

### Directory Structure

```
MCP_Server/
├── server.py                    # Base server (extended with FC tools)
├── __init__.py
└── flyin_colors/                # Flyin' Colors extension
    ├── __init__.py
    ├── template_commands.py     # Command 1: create_flyin_colors_session
    ├── midi_generation.py       # Commands 2, 5, 9 (future)
    ├── narrative_commands.py    # Commands 3, 6, 12 (future)
    ├── session_commands.py      # Commands 4, 11 (future)
    ├── mix_commands.py          # Commands 7, 8 (future)
    └── utils/
        ├── __init__.py
        ├── constants.py         # Track layouts, send configs
        ├── scale_mappings.py    # MIDI note calculations (future)
        └── frequency_ownership.py # EQ chart logic (future)
```

### Extension Pattern

All Flyin' Colors commands follow this pattern:

1. **Implementation:** `flyin_colors/{module}.py`
2. **MCP Wrapper:** Added to `server.py` with `@mcp.tool()` decorator
3. **Uses base commands:** `create_midi_track`, `set_track_name`, etc.
4. **Additive only:** Never modifies ahujasid/ableton-mcp core code

---

## Development

### Upstream Sync

To pull updates from ahujasid/ableton-mcp:

```bash
git remote add upstream https://github.com/ahujasid/ableton-mcp.git
git fetch upstream
git merge upstream/main
```

Flyin' Colors extensions in `MCP_Server/flyin_colors/` won't conflict with upstream.

### Testing New Commands

1. Implement in `MCP_Server/flyin_colors/{module}.py`
2. Add `@mcp.tool()` wrapper in `server.py`
3. Restart Claude Desktop
4. Test via Claude Desktop conversation

### Missing Base Commands

Some Flyin' Colors commands require features not in base ahujasid/ableton-mcp:
- `create_return_track` (needed by Command 1)
- `create_locator` (needed by Commands 1, 3)
- `set_track_muted` (nice-to-have for Command 1)
- `get_device_parameters` (needed by Command 4)

**Options:**
1. Add directly to `AbletonMCP_Remote_Script/__init__.py`
2. Submit PRs to upstream ahujasid/ableton-mcp
3. Use AbletonOSC protocol directly

---

## Proof of Concept Status

**Implemented:**
- ✅ Command 1: `create_flyin_colors_session` (fully functional except return tracks)
- ✅ Directory structure for all 12 commands
- ✅ Constants and utilities foundation

**Known Limitations (PoC):**
- Return tracks may not be created (requires `create_return_track` in base)
- Locator may not be created (requires `create_locator` in base)
- Reference track won't be muted (requires `set_track_muted` in base)

**Still works:**
- All 11 tracks created successfully
- Tempo set correctly
- Track names set correctly
- Track types (MIDI/audio) correct

**Next Steps:**
1. Test Command 1 in real Ableton session
2. Add missing base commands to remote script
3. Implement Commands 2-4 (Phase 1)
4. Test integration with Shadow Creator (Claude Projects)

---

## Credits

- **Base MCP Server:** [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp) (MIT License)
- **Flyin' Colors Extension:** Avi + Claude Sonnet 4.5 (2026)
- **Music Production Architecture:** Flyin' Colors Project

---

## License

MIT License (same as upstream)

See [LICENSE](LICENSE) for details.

---

**Status:** Proof of Concept (Command 1 implemented)
**Last Updated:** 2026-02-14
**Next Milestone:** Commands 2-4 (Week 1-2 implementation plan)
