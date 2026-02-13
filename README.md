# Flyin' Colors MCP for Ableton Live

**Ableton Live automation via Claude Desktop** - Fork of [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp) with custom commands for Flyin' Colors music production workflow.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What This Is

Extends `ahujasid/ableton-mcp` with **12 custom commands** for Flyin' Colors production workflow (trauma-based Trance: Goa + Nitzhonot + Nu-Metal fusion).

### Implemented ✅

1. **`create_flyin_colors_session`** - Complete session template (11 tracks, 4 sends)
2. **`generate_rolling_bass`** - Signature rolling 16th bass MIDI patterns

### Planned (10 more)

3-12. Section markers, session export, arps, automation, mixing tools...

[Full spec](flyin-colors-architecture/technical/MCP_CUSTOM_COMMANDS.md) | [Testing Guide](TESTING_GUIDE.md) | [Architecture Docs](flyin-colors-architecture/)

---

## Quick Start (10 min setup)

1. **Install UV:** `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. **Copy remote script** to Ableton folder
3. **Enable AbletonMCP** in Ableton Preferences
4. **Configure Claude Desktop** (edit `claude_desktop_config.json`)
5. **Restart** Ableton + Claude Desktop
6. **Test:** "Create a Flyin' Colors session at 148 BPM"

[Full setup guide](INSTALL_MCP_NOW.md)

---

## Example Usage

**Create session:**
```
Create a Flyin' Colors session at 148 BPM in D minor called "FC_Test_01"
```
→ 11 tracks + 4 sends created in 10 seconds

**Generate bass:**
```
Generate a rolling bass on track 5, key Dm, 4 bars, progression i-bVI-bVII-i
```
→ 64-note pattern created in 5 seconds

---

## Time Savings

- **Before:** 30-40 min manual setup per session
- **After:** 15 seconds automated
- **Savings:** 35-40 min per session, 5-7 hours across 10 tracks

---

## Documentation

- [Quick Start Checklist](../QUICK_START_CHECKLIST.md) - 4-6 hour production setup
- [Testing Guide](TESTING_GUIDE.md) - Test all commands
- [Installation Guide](INSTALL_MCP_NOW.md) - Setup instructions
- [Architecture](flyin-colors-architecture/) - Complete production system
- [MCP Commands Spec](flyin-colors-architecture/technical/MCP_CUSTOM_COMMANDS.md) - All 12 commands

---

## Credits

- **Base MCP Server:** [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp) (MIT)
- **Flyin' Colors Extension:** Avi + Claude Sonnet 4.5

## License

MIT (same as upstream)
