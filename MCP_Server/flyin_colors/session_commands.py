"""
Session Commands for Flyin' Colors

Command 3: set_section_markers
Creates Ableton locators from narrative arc.

Command 4: export_session_state
Exports session as JSON + markdown for continuation briefs.

Command 11: import_continuation_brief
Restores session context from continuation brief (reverse of export_session_state).
"""

import logging
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("FlyinColorsSession")

# Color mapping for locators
COLOR_MAP = {
    "red": 0,
    "orange": 1,
    "yellow": 2,
    "green": 3,
    "blue": 4,
    "purple": 5,
    "gray": 6
}

# Preset templates for section markers
PRESET_TEMPLATES = {
    "standard_three_act": {
        "description": "Horror→Defiance→Triumph with 3 drops",
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
    },
    "two_drop": {
        "description": "Shorter track, 2 drops",
        "markers": [
            {"bar": 1, "label": "INTRO - Descent", "color": "red", "phase": "horror"},
            {"bar": 17, "label": "BUILDUP 1 - Tension", "color": "red", "phase": "horror"},
            {"bar": 33, "label": "DROP 1 - Horror", "color": "red", "phase": "horror"},
            {"bar": 65, "label": "BREAKDOWN - Transition", "color": "yellow", "phase": "transition"},
            {"bar": 81, "label": "BUILDUP 2 - Defiance", "color": "orange", "phase": "defiance"},
            {"bar": 97, "label": "DROP 2 - Triumph", "color": "green", "phase": "triumph"},
            {"bar": 129, "label": "OUTRO - Resolve", "color": "blue", "phase": "triumph"}
        ]
    },
    "extended_breakdown": {
        "description": "Long emotional breakdown between drops",
        "markers": [
            {"bar": 1, "label": "INTRO - Dread", "color": "red", "phase": "horror"},
            {"bar": 17, "label": "BUILDUP 1 - Machine", "color": "red", "phase": "horror"},
            {"bar": 33, "label": "DROP 1 - Horror", "color": "red", "phase": "horror"},
            {"bar": 65, "label": "BREAKDOWN 1 - Silence", "color": "yellow", "phase": "transition"},
            {"bar": 81, "label": "BREAKDOWN 2 - Voice", "color": "yellow", "phase": "transition"},
            {"bar": 97, "label": "BREAKDOWN 3 - Rising", "color": "orange", "phase": "transition"},
            {"bar": 113, "label": "BUILDUP 2 - Defiance", "color": "orange", "phase": "defiance"},
            {"bar": 129, "label": "DROP 2 - Full Defiance", "color": "orange", "phase": "defiance"},
            {"bar": 161, "label": "BUILDUP 3 - Triumph", "color": "green", "phase": "triumph"},
            {"bar": 177, "label": "DROP 3 - Full Triumph", "color": "green", "phase": "triumph"},
            {"bar": 209, "label": "OUTRO - Afterglow", "color": "blue", "phase": "triumph"}
        ]
    },
    "fast_capture": {
        "description": "Minimal: just intro/main/outro",
        "markers": [
            {"bar": 1, "label": "INTRO", "color": "gray", "phase": None},
            {"bar": 33, "label": "MAIN", "color": "gray", "phase": None},
            {"bar": 129, "label": "OUTRO", "color": "gray", "phase": None}
        ]
    }
}


def set_section_markers(
    ableton_connection,
    markers: Optional[List[Dict[str, Any]]] = None,
    preset: Optional[str] = None,
    total_bars: Optional[int] = None,
    drop_count: Optional[int] = None,
    clear_existing: bool = False
) -> Dict[str, Any]:
    """
    Create Ableton locators from narrative arc.

    Parameters:
        ableton_connection: Active connection to Ableton
        markers: Array of marker objects with bar, label, color, phase
        preset: Preset template name (overrides markers if provided)
        total_bars: Total track length (used with presets)
        drop_count: Number of drops (used with presets)
        clear_existing: Remove all existing locators first

    Returns:
        Dictionary with creation results and phase breakdown
    """

    logger.info("Setting section markers")

    # If preset is specified, use preset markers
    if preset:
        if preset not in PRESET_TEMPLATES:
            raise ValueError(
                f"Unknown preset: {preset}. Must be one of: {list(PRESET_TEMPLATES.keys())}"
            )

        template = PRESET_TEMPLATES[preset]
        markers = template["markers"].copy()
        logger.info(f"Using preset template: {preset} - {template['description']}")

        # Scale markers to total_bars if specified
        if total_bars:
            # Find max bar in template
            template_max_bar = max(m["bar"] for m in markers)
            scale_factor = total_bars / template_max_bar

            for marker in markers:
                marker["bar"] = int(marker["bar"] * scale_factor)

            logger.info(f"Scaled markers to {total_bars} bars (scale factor: {scale_factor:.2f})")

    if not markers:
        raise ValueError("Either 'markers' array or 'preset' must be provided")

    # Validate markers
    for marker in markers:
        if "bar" not in marker or "label" not in marker:
            raise ValueError("Each marker must have 'bar' and 'label' fields")
        if len(marker["label"]) > 50:
            raise ValueError(f"Label too long (max 50 chars): {marker['label']}")

    try:
        # Step 1: Clear existing locators if requested
        if clear_existing:
            logger.info("Clearing existing locators")
            try:
                ableton_connection.send_command("clear_locators")
                logger.info("Existing locators cleared")
            except Exception as e:
                # If clear_locators doesn't exist, log warning but continue
                logger.warning(f"Could not clear existing locators: {e}")

        # Step 2: Create each locator
        markers_created = 0
        for marker in markers:
            bar = marker["bar"]
            label = marker["label"]
            color = marker.get("color", "gray")

            # Validate color
            if color not in COLOR_MAP:
                logger.warning(f"Unknown color '{color}', using gray")
                color = "gray"

            try:
                ableton_connection.send_command("create_locator", {
                    "bar": bar,
                    "label": label
                })
                markers_created += 1
                logger.info(f"Created locator {markers_created}/{len(markers)}: Bar {bar} - {label}")
            except Exception as marker_error:
                logger.error(f"Failed to create locator at bar {bar}: {marker_error}")

        # Step 3: Calculate phase breakdown
        phases = {}
        current_phase = None
        phase_start = None

        for marker in sorted(markers, key=lambda m: m["bar"]):
            phase = marker.get("phase")
            if phase and phase != current_phase:
                # End previous phase
                if current_phase:
                    phases[current_phase] = {
                        "start": phase_start,
                        "end": marker["bar"] - 1,
                        "bars": marker["bar"] - phase_start
                    }

                # Start new phase
                current_phase = phase
                phase_start = marker["bar"]

        # Close last phase
        if current_phase and phase_start:
            last_bar = markers[-1]["bar"]
            phases[current_phase] = {
                "start": phase_start,
                "end": last_bar,
                "bars": last_bar - phase_start + 1
            }

        # Calculate total bars from highest marker
        total_bars_calculated = max(m["bar"] for m in markers)

        result = {
            "status": "success",
            "markers_created": markers_created,
            "cleared_existing": clear_existing,
            "total_bars": total_bars_calculated,
            "phases": phases
        }

        logger.info(f"Section markers set: {markers_created} markers, {len(phases)} phases")
        return result

    except Exception as e:
        error_msg = f"Error setting section markers: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg
        }


def export_session_state(
    ableton_connection,
    output_format: str = "both",
    output_path: Optional[str] = None,
    include_midi_summary: bool = True,
    include_automation_summary: bool = True
) -> Dict[str, Any]:
    """
    Export session as JSON + markdown for continuation briefs.

    Parameters:
        ableton_connection: Active connection to Ableton
        output_format: "json", "markdown", or "both"
        output_path: Where to save files (defaults to current directory)
        include_midi_summary: Summarize MIDI clip contents
        include_automation_summary: List automated parameters

    Returns:
        Dictionary with file paths and summary stats
    """

    logger.info(f"Exporting session state (format: {output_format})")

    if output_format not in ["json", "markdown", "both"]:
        raise ValueError(f"Invalid output_format: {output_format}. Must be 'json', 'markdown', or 'both'")

    # Default output path to current directory
    if not output_path:
        output_path = os.getcwd()

    # Ensure output path exists
    os.makedirs(output_path, exist_ok=True)

    try:
        # Step 1: Get session info
        logger.info("Fetching session info from Ableton")
        session_info = ableton_connection.send_command("get_session_info")

        # Extract basic session data
        bpm = session_info.get("tempo", 0)
        time_signature = session_info.get("time_signature", "4/4")
        total_tracks = len(session_info.get("tracks", []))
        total_scenes = session_info.get("num_scenes", 0)

        # Calculate song length in bars (estimate from session info)
        song_length_bars = 0
        if "song_length" in session_info:
            # If song_length is in beats, convert to bars
            song_length_bars = int(session_info["song_length"] / 4)
        else:
            # Estimate from locators or default
            song_length_bars = 208  # Default Flyin' Colors length

        # Step 2: Build track data
        logger.info("Building track data")
        tracks_data = []
        tracks_with_content = 0
        tracks_with_automation = 0

        for track_info in session_info.get("tracks", []):
            track_index = track_info.get("index", 0)
            track_name = track_info.get("name", "Unknown")
            track_type = track_info.get("type", "unknown")

            # Get more detailed track info if available
            try:
                detailed_track = ableton_connection.send_command("get_track_info", {
                    "track_index": track_index
                })
            except:
                detailed_track = track_info

            # Get clips (if available)
            clips_data = []
            has_midi = False
            note_count_total = 0

            for clip in detailed_track.get("clips", []):
                if clip and clip.get("name"):
                    clip_length_bars = int(clip.get("length", 0) / 4)
                    note_count = clip.get("note_count", 0)

                    clips_data.append({
                        "slot": clip.get("index", 0),
                        "name": clip.get("name", ""),
                        "length_bars": clip_length_bars,
                        "note_count": note_count
                    })

                    if note_count > 0:
                        has_midi = True
                        note_count_total += note_count

            # Get devices
            devices = detailed_track.get("devices", [])

            # Check for automation (placeholder - may need additional command)
            has_automation = False

            # Build track entry
            track_entry = {
                "index": track_index,
                "name": track_name,
                "type": track_type,
                "volume_db": detailed_track.get("volume", 0),
                "devices": [d.get("name", "") for d in devices] if isinstance(devices, list) else devices,
                "clips": clips_data
            }

            if include_automation_summary:
                track_entry["has_automation"] = has_automation

            tracks_data.append(track_entry)

            # Count tracks with content
            if clips_data or devices:
                tracks_with_content += 1
            if has_automation:
                tracks_with_automation += 1

        # Step 3: Build JSON output
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S%z")
        timestamp_filename = timestamp.strftime("%Y%m%d_%H%M")

        json_data = {
            "version": "1.0",
            "exported_at": timestamp_str,
            "session": {
                "bpm": bpm,
                "time_signature": time_signature,
                "total_tracks": total_tracks,
                "total_scenes": total_scenes,
                "song_length_bars": song_length_bars
            },
            "tracks": tracks_data
        }

        # Calculate completion percentage
        completion_pct = 0
        if total_tracks > 0:
            completion_pct = int((tracks_with_content / total_tracks) * 100)

        # Step 4: Write files
        json_path = None
        markdown_path = None

        if output_format in ["json", "both"]:
            json_filename = f"session_state_{timestamp_filename}.json"
            json_path = os.path.join(output_path, json_filename)

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            logger.info(f"JSON exported to: {json_path}")

        if output_format in ["markdown", "both"]:
            markdown_filename = f"session_state_{timestamp_filename}.md"
            markdown_path = os.path.join(output_path, markdown_filename)

            # Build markdown content
            md_lines = [
                "# SESSION STATE — Auto-exported",
                f"**Exported:** {timestamp.strftime('%Y-%m-%d %H:%M')}",
                f"**BPM:** {bpm} | **Tracks:** {total_tracks} | **Length:** {song_length_bars} bars",
                "",
                "## Elements Placed",
                "| Track | Has MIDI? | Devices? | Automation? | Status |",
                "|-------|-----------|----------|-------------|--------|"
            ]

            for track in tracks_data:
                track_name = track["name"]

                # Check if has MIDI
                clips = track.get("clips", [])
                midi_notes = sum(c.get("note_count", 0) for c in clips)
                has_midi_str = f"✅ ({midi_notes} notes)" if midi_notes > 0 else "❌"

                # Check if has devices
                devices = track.get("devices", [])
                has_devices_str = f"✅ {', '.join(devices)}" if devices else "❌"

                # Check automation
                has_automation = track.get("has_automation", False)
                automation_str = "✅" if has_automation else "❌"

                # Status
                status = "Looping" if clips else "Empty"

                md_lines.append(
                    f"| {track_name} | {has_midi_str} | {has_devices_str} | {automation_str} | {status} |"
                )

            md_lines.extend([
                "",
                "## Completion Estimate",
                f"- Tracks with content: {tracks_with_content}/{total_tracks} ({completion_pct}%)",
                f"- Tracks with automation: {tracks_with_automation}/{total_tracks} ({int((tracks_with_automation/total_tracks)*100) if total_tracks > 0 else 0}%)"
            ])

            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(md_lines))

            logger.info(f"Markdown exported to: {markdown_path}")

        result = {
            "status": "success",
            "json_path": json_path,
            "markdown_path": markdown_path,
            "summary": {
                "tracks_with_content": tracks_with_content,
                "completion_pct": completion_pct
            }
        }

        logger.info(f"Session state exported: {completion_pct}% complete")
        return result

    except Exception as e:
        error_msg = f"Error exporting session state: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg
        }


def import_continuation_brief(
    ableton_connection,
    brief_path: str,
    restore_mode: str = "markers_only"
) -> Dict[str, Any]:
    """
    Restore session context from continuation brief JSON.

    Parameters:
        ableton_connection: Active connection to Ableton
        brief_path: Path to JSON brief file
        restore_mode: "markers_only" (tempo, locators, key) or "full" (also tracks, instruments, sends)

    Returns:
        Dictionary with restoration results
    """

    logger.info(f"Importing continuation brief from: {brief_path}")
    logger.info(f"Restore mode: {restore_mode}")

    # Validate restore mode
    if restore_mode not in ["markers_only", "full"]:
        raise ValueError(f"Invalid restore_mode: {restore_mode}. Must be 'markers_only' or 'full'")

    # Validate file exists
    brief_file = Path(brief_path)
    if not brief_file.exists():
        raise FileNotFoundError(f"Continuation brief not found: {brief_path}")

    # Load JSON
    try:
        with open(brief_file, 'r', encoding='utf-8') as f:
            brief_data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in continuation brief: {str(e)}")
    except Exception as e:
        raise Exception(f"Error reading continuation brief: {str(e)}")

    logger.info(f"Loaded continuation brief, version: {brief_data.get('version', 'unknown')}")

    # Track restoration stats
    tempo_set = None
    markers_created = 0
    tracks_created = 0
    errors = []

    try:
        # Step 1: Set tempo (both modes)
        session_data = brief_data.get("session", {})
        bpm = session_data.get("bpm")

        if bpm:
            try:
                logger.info(f"Setting tempo to {bpm} BPM")
                ableton_connection.send_command("set_tempo", {"tempo": float(bpm)})
                tempo_set = bpm
            except Exception as e:
                error_msg = f"Error setting tempo: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)

        # Step 2: Create markers/locators (both modes)
        # Note: This assumes a create_locator command exists or will be added
        locators = brief_data.get("locators", [])
        if locators:
            logger.info(f"Creating {len(locators)} locators")
            for locator in locators:
                try:
                    bar = locator.get("bar")
                    label = locator.get("label", "")

                    # Attempt to create locator
                    # This may require adding create_locator to base MCP
                    ableton_connection.send_command("create_locator", {
                        "bar": bar,
                        "label": label
                    })
                    markers_created += 1
                    logger.info(f"Created locator at bar {bar}: {label}")
                except Exception as e:
                    error_msg = f"Could not create locator at bar {locator.get('bar')}: {str(e)}"
                    logger.warning(error_msg)
                    errors.append(error_msg)

        # Step 3: Set key signature (both modes)
        # Note: May require adding set_key command
        key = session_data.get("key")
        if key:
            try:
                logger.info(f"Setting key to {key}")
                # This may not be implemented yet
                ableton_connection.send_command("set_key", {"key": key})
            except Exception as e:
                logger.warning(f"Could not set key signature: {str(e)}")
                errors.append(f"Key signature not set: {str(e)}")

        # Step 4: Full restoration (only in "full" mode)
        if restore_mode == "full":
            logger.info("Full restoration mode: creating tracks and loading instruments")

            tracks = brief_data.get("tracks", [])
            for track_data in tracks:
                try:
                    track_name = track_data.get("name", "Unknown")
                    track_type = track_data.get("type", "midi")

                    # Create track
                    if track_type == "midi":
                        result = ableton_connection.send_command("create_midi_track", {"index": -1})
                    elif track_type == "audio":
                        result = ableton_connection.send_command("create_audio_track", {"index": -1})
                    else:
                        logger.warning(f"Unknown track type: {track_type}")
                        continue

                    track_index = result.get("track_index", tracks_created)

                    # Set track name
                    ableton_connection.send_command("set_track_name", {
                        "track_index": track_index,
                        "name": track_name
                    })

                    # Set volume if present
                    volume_db = track_data.get("volume_db")
                    if volume_db is not None:
                        try:
                            ableton_connection.send_command("set_track_volume", {
                                "track_index": track_index,
                                "volume_db": float(volume_db)
                            })
                        except Exception as e:
                            logger.warning(f"Could not set volume for {track_name}: {str(e)}")

                    # Load devices/instruments (if URIs are stored)
                    devices = track_data.get("devices", [])
                    for device in devices:
                        # This would require device URIs to be stored in export
                        if isinstance(device, dict) and "uri" in device:
                            try:
                                ableton_connection.send_command("load_browser_item", {
                                    "track_index": track_index,
                                    "item_uri": device["uri"]
                                })
                            except Exception as e:
                                logger.warning(f"Could not load device {device.get('name', 'unknown')}: {str(e)}")

                    tracks_created += 1
                    logger.info(f"Restored track {tracks_created}: {track_name}")

                except Exception as e:
                    error_msg = f"Error restoring track {track_data.get('name', 'unknown')}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)

            # Restore return tracks/sends (if data available)
            return_tracks = brief_data.get("return_tracks", [])
            for return_track in return_tracks:
                try:
                    name = return_track.get("name", "Return")
                    ableton_connection.send_command("create_return_track", {"name": name})
                    logger.info(f"Created return track: {name}")
                except Exception as e:
                    logger.warning(f"Could not create return track: {str(e)}")

        # Prepare response
        response = {
            "status": "success",
            "restore_mode": restore_mode,
            "tempo_set": tempo_set,
            "markers_created": markers_created,
            "tracks_created": tracks_created,
            "brief_path": str(brief_file.absolute())
        }

        if errors:
            response["warnings"] = errors
            response["message"] = f"Restoration complete with {len(errors)} warnings"
        else:
            response["message"] = f"Successfully restored session from continuation brief"

        logger.info(f"Import complete: {response['message']}")
        return response

    except Exception as e:
        error_msg = f"Fatal error importing continuation brief: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg,
            "tempo_set": tempo_set,
            "markers_created": markers_created,
            "tracks_created": tracks_created,
            "errors": errors
        }
