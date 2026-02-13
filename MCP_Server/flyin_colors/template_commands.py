"""
Template Commands for Flyin' Colors

Command 1: create_flyin_colors_session
Creates a complete Ableton session template with standard Flyin' Colors
track layout, routing, and sends.
"""

import logging
from typing import Dict, Any
from .utils.constants import FLYIN_COLORS_TRACKS, FLYIN_COLORS_SENDS, SECTION_TYPES

logger = logging.getLogger("FlyinColorsTemplates")


def create_flyin_colors_session(
    ableton_connection,
    bpm: int = 148,
    key: str = "Dm",
    track_name: str = "FC_Track_01",
    section_type: str = "full"
) -> Dict[str, Any]:
    """
    Create a complete Flyin' Colors session template.

    Parameters:
    - ableton_connection: Active connection to Ableton
    - bpm: Tempo (default: 148)
    - key: Musical key (default: "Dm")
    - track_name: Project name (default: "FC_Track_01")
    - section_type: "full", "minimal", or "jam" (default: "full")

    Returns:
    - Dictionary with creation status and stats
    """

    logger.info(f"Creating Flyin' Colors session: {track_name} @ {bpm} BPM in {key}")

    # Validate section type
    if section_type not in SECTION_TYPES:
        raise ValueError(f"Invalid section_type: {section_type}. Must be one of: {list(SECTION_TYPES.keys())}")

    # Validate BPM range
    if bpm < 100 or bpm > 200:
        logger.warning(f"BPM {bpm} is outside recommended range (140-155 for Flyin' Colors)")

    tracks_created = 0
    sends_created = 0
    errors = []

    try:
        # Step 1: Set tempo
        logger.info(f"Setting tempo to {bpm} BPM")
        tempo_result = ableton_connection.send_command("set_tempo", {"tempo": bpm})
        logger.info(f"Tempo set: {tempo_result}")

        # Step 2: Create tracks
        tracks_config = FLYIN_COLORS_TRACKS[section_type]
        logger.info(f"Creating {len(tracks_config)} tracks for section type: {section_type}")

        for idx, track_config in enumerate(tracks_config):
            try:
                track_type = track_config["type"]
                track_name_actual = track_config["name"]

                # Create track
                if track_type == "midi":
                    result = ableton_connection.send_command("create_midi_track", {"index": -1})
                elif track_type == "audio":
                    result = ableton_connection.send_command("create_audio_track", {"index": -1})
                else:
                    raise ValueError(f"Unknown track type: {track_type}")

                # Get the index of the created track
                track_index = result.get("track_index", idx)

                # Set track name
                name_result = ableton_connection.send_command("set_track_name", {
                    "track_index": track_index,
                    "name": track_name_actual
                })

                # Mute if specified (for Reference track)
                if track_config.get("muted", False):
                    # Note: This command may not exist in base ahujasid/ableton-mcp
                    # If it fails, we'll just log and continue
                    try:
                        ableton_connection.send_command("set_track_muted", {
                            "track_index": track_index,
                            "muted": True
                        })
                    except Exception as mute_error:
                        logger.warning(f"Could not mute track {track_name_actual}: {mute_error}")

                tracks_created += 1
                logger.info(f"Created track {tracks_created}/{len(tracks_config)}: {track_name_actual}")

            except Exception as track_error:
                error_msg = f"Error creating track {track_config['name']}: {track_error}"
                logger.error(error_msg)
                errors.append(error_msg)

        # Step 3: Create return tracks (sends)
        # Note: This functionality may not be implemented in base ahujasid/ableton-mcp
        # We'll attempt it, but won't fail the entire operation if it doesn't work
        logger.info(f"Creating {len(FLYIN_COLORS_SENDS)} return tracks")

        for send_config in FLYIN_COLORS_SENDS:
            try:
                # Attempt to create return track
                # This may require adding this command to the base MCP server
                result = ableton_connection.send_command("create_return_track", {
                    "name": send_config["name"]
                })
                sends_created += 1
                logger.info(f"Created return track: {send_config['name']}")
            except Exception as send_error:
                # If return track creation isn't supported, log but don't fail
                logger.warning(f"Could not create return track {send_config['name']}: {send_error}")
                logger.warning("Return tracks may need to be created manually or require base MCP update")

        # Step 4: Create initial locator at bar 1
        try:
            locator_label = f"{track_name} - {key} - {bpm}BPM"
            # This command may also not exist in base, but we'll try
            ableton_connection.send_command("create_locator", {
                "bar": 1,
                "label": locator_label
            })
            logger.info(f"Created locator: {locator_label}")
        except Exception as locator_error:
            logger.warning(f"Could not create locator: {locator_error}")

        # Prepare response
        response = {
            "status": "success",
            "tracks_created": tracks_created,
            "return_tracks_created": sends_created,
            "bpm": bpm,
            "key": key,
            "section_type": section_type,
            "message": f"Session {track_name} ready. {tracks_created} tracks + {sends_created} sends.",
            "warnings": []
        }

        if errors:
            response["warnings"] = errors
            response["message"] += f" ({len(errors)} errors occurred)"

        if sends_created == 0:
            response["warnings"].append("Return tracks not created - may require manual setup")

        logger.info(f"Session creation complete: {response['message']}")
        return response

    except Exception as e:
        error_msg = f"Fatal error creating Flyin' Colors session: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg,
            "tracks_created": tracks_created,
            "return_tracks_created": sends_created,
            "errors": errors
        }
