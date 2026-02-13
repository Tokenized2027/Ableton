"""
Flyin' Colors Custom MCP Commands

Extensions to ahujasid/ableton-mcp for Flyin' Colors-specific workflow automation.

Commands:
1. create_flyin_colors_session - Full session template
2. generate_rolling_bass - Signature rolling bass MIDI
3. set_section_markers - Narrative structure markers
4. export_session_state - Continuation brief automation
... (12 total)

Repository: AviFlyin/ableton-mcp-flyin-colors
Based on: ahujasid/ableton-mcp (MIT License)
"""

__version__ = "0.1.0"
__author__ = "Avi + Claude"

from .template_commands import *

__all__ = ["create_flyin_colors_session"]
