"""
Template Commands for Flyin' Colors

Command 1: create_flyin_colors_session
Creates a complete Ableton session template with standard Flyin' Colors
track layout, routing, and sends.
"""

import logging
from typing import Dict, Any
from .utils.constants import FLYIN_COLORS_TRACKS, FLYIN_COLORS_SENDS, SECTION_TYPES, GOA_STYLE_PRESETS

logger = logging.getLogger("FlyinColorsTemplates")


def create_flyin_colors_session(
    ableton_connection,
    bpm: int = 148,
    key: str = "Dm",
    track_name: str = "FC_Track_01",
    section_type: str = "full",
    style: str = None
) -> Dict[str, Any]:
    """
    Create a complete Flyin' Colors session template.

    Parameters:
    - ableton_connection: Active connection to Ableton
    - bpm: Tempo (default: 148)
    - key: Musical key (default: "Dm")
    - track_name: Project name (default: "FC_Track_01")
    - section_type: "full", "minimal", or "jam" (default: "full")
    - style: Goa trance style preset (optional). One of "dark_goa", "bright_goa",
             "standard_goa". When set, overrides section_type to the matching goa
             layout and attaches style metadata (filter ranges, scale recommendations,
             spectral targets) to the session response.

    Returns:
    - Dictionary with creation status and stats
    """

    # If a Goa style is specified, override section_type and resolve preset
    style_preset = None
    if style is not None:
        if style not in GOA_STYLE_PRESETS:
            raise ValueError(
                f"Invalid style: {style}. Must be one of: {list(GOA_STYLE_PRESETS.keys())}"
            )
        style_preset = GOA_STYLE_PRESETS[style]
        section_type = style  # dark_goa / bright_goa / standard_goa
        logger.info(
            f"Goa style '{style}' selected. Target centroid: {style_preset['target_centroid_hz']}Hz, "
            f"scale: {style_preset['recommended_scale']}, "
            f"bass filter: {style_preset['bass_filter_range']}"
        )

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

        # Attach Goa style metadata when a style preset was used
        if style_preset is not None:
            response["style"] = style
            response["style_metadata"] = {
                "target_centroid_hz": style_preset["target_centroid_hz"],
                "recommended_scale": style_preset["recommended_scale"],
                "bass_filter_range_hz": list(style_preset["bass_filter_range"]),
                "sub_energy_target_pct": style_preset["sub_energy_target_pct"],
                "frequency_distribution_pct": style_preset["frequency_distribution_pct"],
                "reference_tracks": style_preset["reference_tracks"],
                "recommended_bpm": style_preset["recommended_bpm"],
                "harmony_bars_per_chord": style_preset["harmony_bars_per_chord"],
                "description": style_preset["description"],
            }
            response["message"] += f" Style: {style} (centroid target: {style_preset['target_centroid_hz']}Hz)."

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


def create_nitzhonot_bass_template(
    ableton_connection,
    key: str = "Dm",
    scale: str = "harmonic_minor",
    group_name: str = "Bass Group"
) -> Dict[str, Any]:
    """
    Create pre-routed rolling bass + sub bass track pair with sidechain.

    Creates a track group with:
    - Rolling Bass: Serum/Operator, EQ Eight (HP @ 80Hz, LP @ 200Hz), Compressor (sidechain to kick)
    - Sub Bass: Operator (sine wave), EQ Eight (HP @ 20Hz, LP @ 80Hz), Compressor (sidechain to kick)

    Parameters:
        ableton_connection: Active connection to Ableton
        key: Musical key (e.g., "Dm", "Am")
        scale: Scale type (default: "harmonic_minor")
        group_name: Track group name (default: "Bass Group")

    Returns:
        Dictionary with creation status and stats
    """

    logger.info(f"Creating Nitzhonot bass template: {key} {scale}, group: {group_name}")

    tracks_created = 0
    devices_loaded = 0
    sidechain_configured = False
    errors = []

    try:
        # Step 1: Create Rolling Bass track
        logger.info("Creating Rolling Bass track")
        try:
            rolling_bass_result = ableton_connection.send_command("create_midi_track", {"index": -1})
            rolling_bass_index = rolling_bass_result.get("track_index", -1)

            if rolling_bass_index >= 0:
                # Set track name
                ableton_connection.send_command("set_track_name", {
                    "track_index": rolling_bass_index,
                    "name": "FC_RollingBass"
                })
                tracks_created += 1
                logger.info(f"Created Rolling Bass track at index {rolling_bass_index}")

                # Try to load Serum (or fallback to Operator)
                try:
                    # Attempt to load Serum
                    # Note: URI format may vary depending on Ableton version and plugin installation
                    # This is a placeholder - actual URI would need to be discovered
                    ableton_connection.send_command("load_browser_item", {
                        "track_index": rolling_bass_index,
                        "item_uri": "query:Instruments#Serum"
                    })
                    devices_loaded += 1
                    logger.info("Loaded Serum on Rolling Bass")
                except Exception as serum_error:
                    logger.warning(f"Could not load Serum: {serum_error}")
                    # Fallback to Operator
                    try:
                        ableton_connection.send_command("load_browser_item", {
                            "track_index": rolling_bass_index,
                            "item_uri": "query:Instruments#Operator"
                        })
                        devices_loaded += 1
                        logger.info("Loaded Operator (Serum fallback) on Rolling Bass")
                    except Exception as operator_error:
                        logger.warning(f"Could not load Operator: {operator_error}")
                        errors.append("Could not load synth on Rolling Bass - add manually")

                # Try to add EQ Eight with HP @ 80Hz, LP @ 200Hz
                try:
                    ableton_connection.send_command("load_browser_item", {
                        "track_index": rolling_bass_index,
                        "item_uri": "query:Audio Effects#EQ Eight"
                    })
                    devices_loaded += 1
                    logger.info("Loaded EQ Eight on Rolling Bass")
                    # Note: Setting EQ parameters would require device parameter control
                    # This may need to be done manually or via additional MCP commands
                except Exception as eq_error:
                    logger.warning(f"Could not load EQ Eight: {eq_error}")
                    errors.append("Could not load EQ Eight on Rolling Bass - add manually")

                # Try to add Compressor with sidechain
                try:
                    ableton_connection.send_command("load_browser_item", {
                        "track_index": rolling_bass_index,
                        "item_uri": "query:Audio Effects#Compressor"
                    })
                    devices_loaded += 1
                    logger.info("Loaded Compressor on Rolling Bass")
                    # Note: Sidechain routing requires additional commands not in base MCP
                    errors.append("Sidechain routing must be configured manually")
                except Exception as comp_error:
                    logger.warning(f"Could not load Compressor: {comp_error}")
                    errors.append("Could not load Compressor on Rolling Bass - add manually")

        except Exception as rolling_error:
            error_msg = f"Error creating Rolling Bass track: {rolling_error}"
            logger.error(error_msg)
            errors.append(error_msg)

        # Step 2: Create Sub Bass track
        logger.info("Creating Sub Bass track")
        try:
            sub_bass_result = ableton_connection.send_command("create_midi_track", {"index": -1})
            sub_bass_index = sub_bass_result.get("track_index", -1)

            if sub_bass_index >= 0:
                # Set track name
                ableton_connection.send_command("set_track_name", {
                    "track_index": sub_bass_index,
                    "name": "FC_SubBass"
                })
                tracks_created += 1
                logger.info(f"Created Sub Bass track at index {sub_bass_index}")

                # Load Operator (sine wave for sub)
                try:
                    ableton_connection.send_command("load_browser_item", {
                        "track_index": sub_bass_index,
                        "item_uri": "query:Instruments#Operator"
                    })
                    devices_loaded += 1
                    logger.info("Loaded Operator on Sub Bass")
                    # Note: Configuring Operator for sine wave requires parameter control
                    errors.append("Configure Operator for sine wave manually")
                except Exception as operator_error:
                    logger.warning(f"Could not load Operator: {operator_error}")
                    errors.append("Could not load Operator on Sub Bass - add manually")

                # Try to add EQ Eight with HP @ 20Hz, LP @ 80Hz
                try:
                    ableton_connection.send_command("load_browser_item", {
                        "track_index": sub_bass_index,
                        "item_uri": "query:Audio Effects#EQ Eight"
                    })
                    devices_loaded += 1
                    logger.info("Loaded EQ Eight on Sub Bass")
                    # Note: Setting EQ parameters would require device parameter control
                except Exception as eq_error:
                    logger.warning(f"Could not load EQ Eight: {eq_error}")
                    errors.append("Could not load EQ Eight on Sub Bass - add manually")

                # Try to add Compressor with sidechain (faster attack)
                try:
                    ableton_connection.send_command("load_browser_item", {
                        "track_index": sub_bass_index,
                        "item_uri": "query:Audio Effects#Compressor"
                    })
                    devices_loaded += 1
                    logger.info("Loaded Compressor on Sub Bass")
                    errors.append("Sidechain routing and faster attack must be configured manually")
                except Exception as comp_error:
                    logger.warning(f"Could not load Compressor: {comp_error}")
                    errors.append("Could not load Compressor on Sub Bass - add manually")

        except Exception as sub_error:
            error_msg = f"Error creating Sub Bass track: {sub_error}"
            logger.error(error_msg)
            errors.append(error_msg)

        # Step 3: Try to create track group
        # Note: Track grouping may not be supported in base ahujasid/ableton-mcp
        # We'll attempt it, but won't fail if it doesn't work
        try:
            logger.info(f"Attempting to create track group: {group_name}")
            ableton_connection.send_command("create_track_group", {
                "name": group_name,
                "track_indices": [rolling_bass_index, sub_bass_index]
            })
            logger.info(f"Created track group: {group_name}")
        except Exception as group_error:
            logger.warning(f"Could not create track group: {group_error}")
            errors.append(f"Track grouping not supported - group tracks manually as '{group_name}'")

        # Prepare response
        response = {
            "status": "success",
            "group_created": tracks_created == 2,  # Both tracks created
            "tracks_in_group": tracks_created,
            "sidechain_configured": sidechain_configured,
            "devices_loaded": devices_loaded,
            "key": key,
            "scale": scale,
            "message": f"Nitzhonot bass template created: {tracks_created} tracks, {devices_loaded} devices loaded",
            "warnings": errors
        }

        if tracks_created < 2:
            response["status"] = "partial"
            response["message"] = f"Only {tracks_created}/2 tracks created - check errors"

        logger.info(f"Nitzhonot bass template creation complete: {response['message']}")
        return response

    except Exception as e:
        error_msg = f"Fatal error creating Nitzhonot bass template: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg,
            "group_created": False,
            "tracks_in_group": tracks_created,
            "sidechain_configured": False,
            "devices_loaded": devices_loaded,
            "errors": errors
        }
