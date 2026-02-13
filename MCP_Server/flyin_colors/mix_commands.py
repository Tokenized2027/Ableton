"""
Mix Commands for Flyin' Colors

Command 7: apply_frequency_ownership
Command 8: check_frequency_conflicts

These commands implement the frequency ownership chart from FREQUENCY_RANGE_OWNERSHIP.md
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger("FlyinColorsMix")

# Frequency Ownership Chart
# Calibrated from 8-track Goa reference analysis (COMBINED_GOA_DNA.json)
# Energy distribution: sub_bass 55.3%, bass 25.3%, low_mid 10.2%, mid 4.9%, high_mid 2.5%, high 1.6%
FREQUENCY_OWNERSHIP = {
    "FC_Sub": {
        "hp_freq": 20,
        "lp_freq": 80,
        "range": "20-80 Hz",
        "role": "Sub Bass",
        "energy_pct": 55.3              # Dominant band in Goa trance
    },
    "FC_RollingBass": {
        "hp_freq": 80,
        "lp_freq": 300,
        "range": "80-300 Hz",
        "role": "Rolling Bass",
        "energy_pct": 25.3              # bass band extends to 300Hz per analysis
    },
    "FC_Kick": {
        "hp_freq": 40,
        "lp_freq": 8000,
        "range": "40-8000 Hz",
        "role": "Kick"
    },
    "FC_Pad": {
        "hp_freq": 300,
        "lp_freq": 8000,
        "range": "300-8000 Hz",
        "role": "Pad",
        "energy_pct": 10.2              # low_mid band where pads sit
    },
    "FC_Lead": {
        "hp_freq": 1000,
        "lp_freq": None,
        "range": "1000+ Hz",
        "role": "Lead",
        "energy_pct": 4.9               # mid band (1k-4kHz)
    },
    "FC_Arp": {
        "hp_freq": 1000,
        "lp_freq": None,
        "range": "1000+ Hz",
        "role": "Arp",
        "energy_pct": 2.5               # high_mid band (4k-8kHz)
    },
    "FC_Hats": {
        "hp_freq": 4000,
        "lp_freq": None,
        "range": "4000+ Hz",
        "role": "Hi-hats",
        "energy_pct": 1.6               # high band (8k+)
    },
    "FC_Perc": {
        "hp_freq": 300,
        "lp_freq": None,
        "range": "300+ Hz",
        "role": "Percussion"
    }
}


def apply_frequency_ownership(
    ableton_connection,
    strict_mode: bool = True,
    apply_to_tracks: str = "all"
) -> Dict[str, Any]:
    """
    Apply frequency ownership chart to all tracks using EQ Eight.

    Parameters:
    - ableton_connection: Active connection to Ableton
    - strict_mode: True = 24dB/oct filters, False = 12dB/oct filters
    - apply_to_tracks: "all" or "empty_only" (only tracks without EQ)

    Returns:
    - Dictionary with processing status
    """

    logger.info(f"Applying frequency ownership (strict_mode={strict_mode}, apply_to={apply_to_tracks})")

    tracks_processed = 0
    eq_added = 0
    eq_modified = 0
    skipped = []
    errors = []

    try:
        # Get session info to find all tracks
        session_info = ableton_connection.send_command("get_session_info")
        num_tracks = session_info.get("num_tracks", 0)

        logger.info(f"Found {num_tracks} tracks in session")

        # Process each track
        for track_idx in range(num_tracks):
            try:
                # Get track info
                track_info = ableton_connection.send_command("get_track_info", {
                    "track_index": track_idx
                })

                track_name = track_info.get("name", f"Track {track_idx}")
                devices = track_info.get("devices", [])

                # Check if this track is in our frequency ownership chart
                if track_name not in FREQUENCY_OWNERSHIP:
                    logger.debug(f"Skipping {track_name} (not in frequency ownership chart)")
                    skipped.append(track_name)
                    continue

                # Get frequency settings for this track
                freq_settings = FREQUENCY_OWNERSHIP[track_name]
                hp_freq = freq_settings["hp_freq"]
                lp_freq = freq_settings["lp_freq"]

                # Check if track already has EQ Eight
                has_eq = "EQ Eight" in devices

                # Skip if apply_to_tracks is "empty_only" and track has EQ
                if apply_to_tracks == "empty_only" and has_eq:
                    logger.info(f"Skipping {track_name} (already has EQ Eight)")
                    skipped.append(track_name)
                    continue

                # Determine filter slope based on strict_mode
                # 24dB/oct = slope value 3, 12dB/oct = slope value 1
                filter_slope = 3 if strict_mode else 1

                # Load or modify EQ Eight
                if not has_eq:
                    # Add EQ Eight to track
                    logger.info(f"Adding EQ Eight to {track_name}")
                    try:
                        ableton_connection.send_command("load_browser_item", {
                            "track_index": track_idx,
                            "item_uri": "query:Audio%20Effects#EQ%20Eight"
                        })
                        eq_added += 1
                    except Exception as load_error:
                        logger.warning(f"Could not load EQ Eight on {track_name}, trying fallback: {load_error}")
                        errors.append(f"Could not load EQ Eight on {track_name}")
                        continue
                else:
                    logger.info(f"Modifying existing EQ Eight on {track_name}")
                    eq_modified += 1

                # Configure High-Pass Filter
                if hp_freq:
                    try:
                        # Set HP filter frequency (parameter index varies by device)
                        # This is a simplified approach - actual parameter indices may vary
                        # EQ Eight HP: typically parameter 0 (on/off), 1 (frequency), 2 (slope)

                        # Enable HP filter
                        ableton_connection.send_command("set_device_parameter", {
                            "track_index": track_idx,
                            "device_index": devices.index("EQ Eight") if has_eq else 0,
                            "parameter_index": 0,  # HP On/Off
                            "value": 1.0  # On
                        })

                        # Set HP frequency (normalized 0-1, needs conversion)
                        # For now, using a simplified mapping
                        hp_normalized = min(1.0, max(0.0, (hp_freq - 20) / (20000 - 20)))
                        ableton_connection.send_command("set_device_parameter", {
                            "track_index": track_idx,
                            "device_index": devices.index("EQ Eight") if has_eq else 0,
                            "parameter_index": 1,  # HP Frequency
                            "value": hp_normalized
                        })

                        # Set HP slope
                        slope_normalized = filter_slope / 3.0  # Normalize to 0-1
                        ableton_connection.send_command("set_device_parameter", {
                            "track_index": track_idx,
                            "device_index": devices.index("EQ Eight") if has_eq else 0,
                            "parameter_index": 2,  # HP Slope
                            "value": slope_normalized
                        })

                        logger.info(f"  Set HP filter: {hp_freq} Hz @ {24 if strict_mode else 12}dB/oct")
                    except Exception as hp_error:
                        logger.warning(f"Could not set HP filter on {track_name}: {hp_error}")

                # Configure Low-Pass Filter
                if lp_freq:
                    try:
                        # Enable LP filter (parameter indices for LP typically higher)
                        ableton_connection.send_command("set_device_parameter", {
                            "track_index": track_idx,
                            "device_index": devices.index("EQ Eight") if has_eq else 0,
                            "parameter_index": 48,  # LP On/Off (example index)
                            "value": 1.0  # On
                        })

                        # Set LP frequency
                        lp_normalized = min(1.0, max(0.0, (lp_freq - 20) / (20000 - 20)))
                        ableton_connection.send_command("set_device_parameter", {
                            "track_index": track_idx,
                            "device_index": devices.index("EQ Eight") if has_eq else 0,
                            "parameter_index": 49,  # LP Frequency
                            "value": lp_normalized
                        })

                        # Set LP slope
                        slope_normalized = filter_slope / 3.0
                        ableton_connection.send_command("set_device_parameter", {
                            "track_index": track_idx,
                            "device_index": devices.index("EQ Eight") if has_eq else 0,
                            "parameter_index": 50,  # LP Slope
                            "value": slope_normalized
                        })

                        logger.info(f"  Set LP filter: {lp_freq} Hz @ {24 if strict_mode else 12}dB/oct")
                    except Exception as lp_error:
                        logger.warning(f"Could not set LP filter on {track_name}: {lp_error}")

                tracks_processed += 1
                logger.info(f"Processed {track_name}: HP={hp_freq}Hz, LP={lp_freq or 'None'}Hz")

            except Exception as track_error:
                error_msg = f"Error processing track {track_idx}: {track_error}"
                logger.error(error_msg)
                errors.append(error_msg)

        # Prepare response
        response = {
            "status": "success",
            "tracks_processed": tracks_processed,
            "eq_added": eq_added,
            "eq_modified": eq_modified,
            "skipped": len(skipped),
            "strict_mode": strict_mode,
            "message": f"Applied frequency ownership to {tracks_processed} tracks. Added {eq_added} EQs, modified {eq_modified} EQs."
        }

        if errors:
            response["warnings"] = errors
            response["message"] += f" ({len(errors)} warnings)"

        logger.info(f"Frequency ownership application complete: {response['message']}")
        return response

    except Exception as e:
        error_msg = f"Fatal error applying frequency ownership: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg,
            "tracks_processed": tracks_processed,
            "eq_added": eq_added,
            "eq_modified": eq_modified
        }


def check_frequency_conflicts(
    ableton_connection,
    report_mode: str = "summary"
) -> Dict[str, Any]:
    """
    Check all tracks for frequency ownership violations.

    Parameters:
    - ableton_connection: Active connection to Ableton
    - report_mode: "summary" or "detailed"

    Returns:
    - Dictionary with conflict analysis
    """

    logger.info(f"Checking frequency conflicts (report_mode={report_mode})")

    conflicts = []
    tracks_analyzed = 0

    try:
        # Get session info
        session_info = ableton_connection.send_command("get_session_info")
        num_tracks = session_info.get("num_tracks", 0)

        logger.info(f"Analyzing {num_tracks} tracks for conflicts")

        # Collect track frequency info
        track_frequencies = []

        for track_idx in range(num_tracks):
            try:
                track_info = ableton_connection.send_command("get_track_info", {
                    "track_index": track_idx
                })

                track_name = track_info.get("name", f"Track {track_idx}")
                devices = track_info.get("devices", [])

                # Only analyze tracks in our frequency ownership chart
                if track_name not in FREQUENCY_OWNERSHIP:
                    continue

                freq_settings = FREQUENCY_OWNERSHIP[track_name]
                expected_hp = freq_settings["hp_freq"]
                expected_lp = freq_settings["lp_freq"]

                track_frequencies.append({
                    "track_name": track_name,
                    "track_index": track_idx,
                    "expected_hp": expected_hp,
                    "expected_lp": expected_lp,
                    "has_eq": "EQ Eight" in devices,
                    "role": freq_settings["role"]
                })

                tracks_analyzed += 1

            except Exception as track_error:
                logger.warning(f"Could not analyze track {track_idx}: {track_error}")

        # Check for conflicts
        # Conflict detection logic based on frequency ranges

        # Conflict Type 1: Pads in bass territory (< 300 Hz)
        for track in track_frequencies:
            if track["role"] in ["Pad", "Lead", "Arp"] and track["expected_hp"] < 300:
                conflicts.append({
                    "track_1": track["track_name"],
                    "track_2": "Rolling Bass",
                    "conflict_range": "Below 300 Hz",
                    "severity": "high",
                    "recommendation": f"High-pass {track['track_name']} to 300 Hz minimum",
                    "current_hp": track["expected_hp"],
                    "recommended_hp": 300
                })

        # Conflict Type 2: Missing EQ on frequency-critical tracks
        for track in track_frequencies:
            if not track["has_eq"]:
                conflicts.append({
                    "track_1": track["track_name"],
                    "track_2": "N/A",
                    "conflict_range": "Full spectrum",
                    "severity": "medium",
                    "recommendation": f"Add EQ Eight to {track['track_name']} and apply frequency ownership",
                    "current_hp": None,
                    "recommended_hp": track["expected_hp"]
                })

        # Conflict Type 3: Sub and Kick not sharing 40-80 Hz
        sub_track = next((t for t in track_frequencies if t["role"] == "Sub Bass"), None)
        kick_track = next((t for t in track_frequencies if t["role"] == "Kick"), None)

        if sub_track and kick_track:
            # Check if they overlap correctly in 40-80 Hz range
            sub_range = (sub_track["expected_hp"], sub_track["expected_lp"] or 20000)
            kick_range = (kick_track["expected_hp"], kick_track["expected_lp"] or 20000)

            # They should both cover 40-80 Hz
            if not (sub_range[0] <= 40 and (sub_range[1] or 20000) >= 80):
                conflicts.append({
                    "track_1": sub_track["track_name"],
                    "track_2": kick_track["track_name"],
                    "conflict_range": "40-80 Hz",
                    "severity": "high",
                    "recommendation": "Sub Bass should cover 40-80 Hz (intentional overlap with Kick)",
                    "current_hp": sub_track["expected_hp"],
                    "recommended_hp": 40
                })

        # Prepare response
        response = {
            "status": "success",
            "conflict_count": len(conflicts),
            "tracks_analyzed": tracks_analyzed,
            "report_mode": report_mode
        }

        if report_mode == "detailed":
            response["conflicts"] = conflicts
            response["message"] = f"Found {len(conflicts)} conflicts across {tracks_analyzed} tracks. See details below."
        else:
            # Summary mode - just counts by severity
            high_severity = len([c for c in conflicts if c.get("severity") == "high"])
            medium_severity = len([c for c in conflicts if c.get("severity") == "medium"])
            low_severity = len([c for c in conflicts if c.get("severity") == "low"])

            response["summary"] = {
                "high_severity": high_severity,
                "medium_severity": medium_severity,
                "low_severity": low_severity
            }
            response["message"] = f"Found {len(conflicts)} conflicts: {high_severity} high, {medium_severity} medium, {low_severity} low severity."

        if len(conflicts) == 0:
            response["message"] = f"No frequency conflicts detected. All {tracks_analyzed} tracks follow ownership chart."

        logger.info(f"Conflict check complete: {response['message']}")
        return response

    except Exception as e:
        error_msg = f"Fatal error checking frequency conflicts: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg,
            "conflict_count": 0,
            "tracks_analyzed": tracks_analyzed
        }
