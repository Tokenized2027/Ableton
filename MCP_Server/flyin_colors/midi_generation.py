"""
MIDI Generation Commands for Flyin' Colors

Command 2: generate_rolling_bass
Generates rolling 16th-note bass patterns - the signature Flyin' Colors sound.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger("FlyinColorsMIDI")

# Scale definitions (MIDI note offsets from root)
SCALES = {
    "natural_minor": [0, 2, 3, 5, 7, 8, 10],           # W-H-W-W-H-W-W
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],          # W-H-W-W-H-WH-H
    "phrygian_dominant": [0, 1, 4, 5, 7, 8, 10],       # H-WH-H-W-H-W-W
    "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
}

# Roman numeral to scale degree mapping
# Returns list of possible notes for each degree across all octaves
ROMAN_NUMERALS = {
    # Natural Minor
    "i": [0],      # Root
    "ii°": [2],    # 2nd (diminished)
    "bIII": [3],   # Flat 3rd
    "iv": [5],     # 4th
    "v": [7],      # 5th
    "bVI": [8],    # Flat 6th
    "bVII": [10],  # Flat 7th

    # Harmonic Minor additions
    "V": [7],      # Major 5th
    "vii°": [11],  # Raised 7th (diminished)

    # Phrygian Dominant
    "bII": [1],    # Flat 2nd
    "III": [4],    # Major 3rd
}

def note_name_to_midi(note_name, octave=2):
    """Convert note name (C, D, E, etc.) to MIDI note number"""
    note_map = {
        "C": 0, "C#": 1, "Db": 1,
        "D": 2, "D#": 3, "Eb": 3,
        "E": 4,
        "F": 5, "F#": 6, "Gb": 6,
        "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10,
        "B": 11
    }

    # Extract note and accidental
    if len(note_name) == 2:
        note = note_name[0].upper()
        accidental = note_name[1]
        full_note = note + accidental
    else:
        full_note = note_name.upper()

    return note_map.get(full_note, 0) + (octave + 1) * 12


def get_chord_root_note(key, chord_degree, scale_type, octave):
    """
    Get the MIDI note number for a chord root given the key and roman numeral degree.

    Args:
        key: Root note name (e.g., "D", "Am")
        chord_degree: Roman numeral (e.g., "i", "bVI", "bVII")
        scale_type: Scale name
        octave: Target octave

    Returns:
        MIDI note number
    """
    # Parse key (handle things like "Dm" -> "D")
    if len(key) > 1 and key[1] not in ['#', 'b']:
        key = key[0]  # Strip minor designation if present

    # Get root MIDI note
    root = note_name_to_midi(key, octave)

    # Get scale pattern
    scale_pattern = SCALES.get(scale_type, SCALES["natural_minor"])

    # Get offset from roman numeral
    offsets = ROMAN_NUMERALS.get(chord_degree, [0])
    offset = offsets[0]  # Take first option

    # Calculate final note
    return root + offset


def generate_rolling_bass(
    ableton_connection,
    track_index: int,
    clip_slot: int = 0,
    key: str = "D",
    octave: int = 2,
    scale: str = "natural_minor",
    bars: int = 4,
    pattern_type: str = "rolling_16th",
    velocity_pattern: List[int] = None,
    chord_progression: List[str] = None,
    bars_per_chord: int = 1,
    filter_hint: str = "medium"
) -> Dict[str, Any]:
    """
    Generate a rolling bass MIDI clip - the signature Flyin' Colors sound.

    Parameters:
        ableton_connection: Active connection to Ableton
        track_index: Which track to place clip on
        clip_slot: Scene/clip slot index
        key: Root note ("C", "D", "E", etc.)
        octave: MIDI octave (2 = bass range, D2 = MIDI 38)
        scale: Scale type
        bars: Clip length in bars
        pattern_type: Rhythm pattern
        velocity_pattern: Repeating velocity cycle (default: [100, 85, 95, 80])
        chord_progression: Roman numerals (default: ["i"])
        bars_per_chord: Bars before chord changes
        filter_hint: Metadata for filter position ("closed", "medium", "open")

    Returns:
        Dictionary with generation results
    """

    logger.info(f"Generating rolling bass: {key} {scale}, {bars} bars, pattern: {pattern_type}")

    # Defaults
    if velocity_pattern is None:
        velocity_pattern = [100, 85, 95, 80]
    if chord_progression is None:
        chord_progression = ["i"]

    # Validate scale
    if scale not in SCALES:
        raise ValueError(f"Unknown scale: {scale}. Must be one of: {list(SCALES.keys())}")

    try:
        # Step 1: Create the clip
        clip_length = float(bars * 4)  # 4 beats per bar
        logger.info(f"Creating {clip_length}-beat clip at track {track_index}, slot {clip_slot}")

        ableton_connection.send_command("create_clip", {
            "track_index": track_index,
            "clip_index": clip_slot,
            "length": clip_length
        })

        # Step 2: Generate notes based on pattern type
        notes = []
        ticks_per_16th = 240  # Ableton uses 960 PPQN, so 16th note = 240 ticks

        if pattern_type == "rolling_16th":
            # Every 16th note, single root note
            num_16ths = bars * 16  # 16 sixteenth notes per bar

            for i in range(num_16ths):
                # Determine which chord we're on
                chord_index = (i // (bars_per_chord * 16)) % len(chord_progression)
                chord_degree = chord_progression[chord_index]

                # Get the MIDI note for this chord's root
                midi_note = get_chord_root_note(key, chord_degree, scale, octave)

                # Get velocity from pattern
                velocity = velocity_pattern[i % len(velocity_pattern)]

                # Calculate timing
                start_tick = i * ticks_per_16th
                duration_ticks = ticks_per_16th  # Full 16th note duration

                notes.append({
                    "pitch": midi_note,
                    "start_time": start_tick,
                    "duration": duration_ticks,
                    "velocity": velocity,
                    "mute": False
                })

        elif pattern_type == "pulsing_8th":
            # Every 8th note, alternating root and octave
            num_8ths = bars * 8

            for i in range(num_8ths):
                chord_index = (i // (bars_per_chord * 8)) % len(chord_progression)
                chord_degree = chord_progression[chord_index]

                base_note = get_chord_root_note(key, chord_degree, scale, octave)

                # Alternate between root and octave
                if i % 2 == 0:
                    midi_note = base_note  # Root
                else:
                    midi_note = base_note + 12  # Octave up

                velocity = velocity_pattern[i % len(velocity_pattern)]
                start_tick = i * (ticks_per_16th * 2)  # 8th note = 2 16ths
                duration_ticks = ticks_per_16th * 2

                notes.append({
                    "pitch": midi_note,
                    "start_time": start_tick,
                    "duration": duration_ticks,
                    "velocity": velocity,
                    "mute": False
                })

        elif pattern_type == "syncopated":
            # 16ths with accent on off-beats
            num_16ths = bars * 16

            for i in range(num_16ths):
                # Skip every 4th beat (downbeats)
                if i % 4 == 0:
                    continue

                chord_index = (i // (bars_per_chord * 16)) % len(chord_progression)
                chord_degree = chord_progression[chord_index]
                midi_note = get_chord_root_note(key, chord_degree, scale, octave)

                # Accent off-beats
                if i % 2 == 1:
                    velocity = min(127, velocity_pattern[i % len(velocity_pattern)] + 10)
                else:
                    velocity = velocity_pattern[i % len(velocity_pattern)]

                start_tick = i * ticks_per_16th
                duration_ticks = ticks_per_16th

                notes.append({
                    "pitch": midi_note,
                    "start_time": start_tick,
                    "duration": duration_ticks,
                    "velocity": velocity,
                    "mute": False
                })

        elif pattern_type == "gallop":
            # 16th-16th-8th repeating (nu-metal style)
            num_beats = bars * 4

            for beat in range(num_beats):
                chord_index = (beat // (bars_per_chord * 4)) % len(chord_progression)
                chord_degree = chord_progression[chord_index]
                midi_note = get_chord_root_note(key, chord_degree, scale, octave)

                beat_start = beat * 4 * ticks_per_16th  # 4 16ths per beat

                # First 16th
                notes.append({
                    "pitch": midi_note,
                    "start_time": beat_start,
                    "duration": ticks_per_16th,
                    "velocity": velocity_pattern[0],
                    "mute": False
                })

                # Second 16th
                notes.append({
                    "pitch": midi_note,
                    "start_time": beat_start + ticks_per_16th,
                    "duration": ticks_per_16th,
                    "velocity": velocity_pattern[1] if len(velocity_pattern) > 1 else velocity_pattern[0],
                    "mute": False
                })

                # 8th note (two 16ths)
                notes.append({
                    "pitch": midi_note,
                    "start_time": beat_start + (2 * ticks_per_16th),
                    "duration": ticks_per_16th * 2,
                    "velocity": velocity_pattern[2] if len(velocity_pattern) > 2 else velocity_pattern[0],
                    "mute": False
                })

        else:
            raise ValueError(f"Unknown pattern_type: {pattern_type}")

        # Step 3: Add notes to clip
        logger.info(f"Adding {len(notes)} notes to clip")
        ableton_connection.send_command("add_notes_to_clip", {
            "track_index": track_index,
            "clip_index": clip_slot,
            "notes": notes
        })

        # Step 4: Name the clip
        clip_name = f"FC_Bass_{key}m_{pattern_type}"
        ableton_connection.send_command("set_clip_name", {
            "track_index": track_index,
            "clip_index": clip_slot,
            "name": clip_name
        })

        # Collect unique pitches used
        unique_pitches = sorted(set(note["pitch"] for note in notes))

        result = {
            "status": "success",
            "clip_name": clip_name,
            "track_index": track_index,
            "clip_slot": clip_slot,
            "notes_placed": len(notes),
            "bars": bars,
            "unique_pitches": unique_pitches,
            "pattern_type": pattern_type,
            "filter_hint": filter_hint
        }

        logger.info(f"Rolling bass generated: {len(notes)} notes, {len(unique_pitches)} unique pitches")
        return result

    except Exception as e:
        error_msg = f"Error generating rolling bass: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg
        }


def generate_goa_arp(
    ableton_connection,
    track_index: int,
    clip_slot: int = 0,
    key: str = "D",
    octave_start: int = 3,
    octave_range: int = 2,
    scale: str = "natural_minor",
    bars: int = 4,
    rate: str = "16th",
    direction: str = "up",
    chord_tones: List[str] = None,
    velocity_range: List[int] = None,
    velocity_shape: str = "saw_up",
    note_length_pct: int = 80
) -> Dict[str, Any]:
    """
    Generate arpeggiated MIDI pattern in Filteria/Pleiadians style.

    Parameters:
        ableton_connection: Active connection to Ableton
        track_index: Which track to place clip on
        clip_slot: Scene/clip slot index
        key: Root note ("C", "D", "E", etc.)
        octave_start: Starting octave
        octave_range: Octaves to span (1-3)
        scale: Scale type
        bars: Clip length in bars
        rate: Note rate ("8th", "16th", "32nd", "16th_triplet")
        direction: Arp direction ("up", "down", "up_down", "random_seed")
        chord_tones: Scale degrees (e.g., ["1", "3", "5", "7"])
        velocity_range: [min, max] velocity
        velocity_shape: Velocity pattern ("saw_up", "saw_down", "flat", "random")
        note_length_pct: Note length as percentage (100=legato, 50=staccato)

    Returns:
        Dictionary with generation results
    """
    import random

    logger.info(f"Generating Goa arp: {key} {scale}, {bars} bars, rate: {rate}, direction: {direction}")

    # Defaults
    if chord_tones is None:
        chord_tones = ["1", "3", "5"]
    if velocity_range is None:
        velocity_range = [70, 110]

    # Validate scale
    if scale not in SCALES:
        raise ValueError(f"Unknown scale: {scale}. Must be one of: {list(SCALES.keys())}")

    # Map rate to ticks
    ticks_per_16th = 240  # Ableton uses 960 PPQN
    rate_to_ticks = {
        "8th": ticks_per_16th * 2,
        "16th": ticks_per_16th,
        "32nd": ticks_per_16th // 2,
        "16th_triplet": int(ticks_per_16th * 2 / 3)
    }

    if rate not in rate_to_ticks:
        raise ValueError(f"Unknown rate: {rate}. Must be one of: {list(rate_to_ticks.keys())}")

    note_ticks = rate_to_ticks[rate]

    try:
        # Step 1: Create the clip
        clip_length = float(bars * 4)
        logger.info(f"Creating {clip_length}-beat clip at track {track_index}, slot {clip_slot}")

        ableton_connection.send_command("create_clip", {
            "track_index": track_index,
            "clip_index": clip_slot,
            "length": clip_length
        })

        # Step 2: Build scale notes across octave range
        root = note_name_to_midi(key, octave_start)
        scale_pattern = SCALES[scale]

        # Convert chord_tones (scale degrees) to indices
        tone_indices = []
        for tone in chord_tones:
            degree = int(tone) - 1  # "1" = index 0 (root)
            if 0 <= degree < len(scale_pattern):
                tone_indices.append(degree)

        # Build pitch pool across octaves
        pitch_pool = []
        for octave_offset in range(octave_range):
            for tone_idx in tone_indices:
                pitch = root + scale_pattern[tone_idx] + (octave_offset * 12)
                pitch_pool.append(pitch)

        pitch_pool.sort()

        # Step 3: Generate arp sequence based on direction
        if direction == "up":
            arp_sequence = pitch_pool
        elif direction == "down":
            arp_sequence = list(reversed(pitch_pool))
        elif direction == "up_down":
            # Up then down (excluding duplicate at peak)
            arp_sequence = pitch_pool + list(reversed(pitch_pool[:-1]))
        elif direction == "random_seed":
            # Seeded random for consistent psychedelic pattern
            random.seed(42)
            arp_sequence = pitch_pool.copy()
            random.shuffle(arp_sequence)
        else:
            raise ValueError(f"Unknown direction: {direction}")

        # Step 4: Calculate total notes and generate MIDI
        total_ticks = int(clip_length * 960)  # bars * 4 beats * 960 ticks
        num_notes = total_ticks // note_ticks
        notes = []

        for i in range(num_notes):
            pitch = arp_sequence[i % len(arp_sequence)]

            # Calculate velocity based on shape
            if velocity_shape == "saw_up":
                t = (i % len(arp_sequence)) / len(arp_sequence)
                velocity = int(velocity_range[0] + t * (velocity_range[1] - velocity_range[0]))
            elif velocity_shape == "saw_down":
                t = (i % len(arp_sequence)) / len(arp_sequence)
                velocity = int(velocity_range[1] - t * (velocity_range[1] - velocity_range[0]))
            elif velocity_shape == "flat":
                velocity = velocity_range[0]
            elif velocity_shape == "random":
                velocity = random.randint(velocity_range[0], velocity_range[1])
            else:
                velocity = velocity_range[0]

            # Calculate note duration based on note_length_pct
            duration_ticks = int(note_ticks * note_length_pct / 100)

            notes.append({
                "pitch": pitch,
                "start_time": i * note_ticks,
                "duration": duration_ticks,
                "velocity": velocity,
                "mute": False
            })

        # Step 5: Add notes to clip
        logger.info(f"Adding {len(notes)} notes to clip")
        ableton_connection.send_command("add_notes_to_clip", {
            "track_index": track_index,
            "clip_index": clip_slot,
            "notes": notes
        })

        # Step 6: Name the clip
        clip_name = f"FC_Arp_{key}{scale[0].upper()}_{rate}_{direction}"
        ableton_connection.send_command("set_clip_name", {
            "track_index": track_index,
            "clip_index": clip_slot,
            "name": clip_name
        })

        # Collect unique pitches
        unique_pitches = sorted(set(note["pitch"] for note in notes))
        octave_range_str = f"{key}{octave_start}-{key}{octave_start + octave_range - 1}"

        result = {
            "status": "success",
            "clip_name": clip_name,
            "notes_placed": len(notes),
            "octave_range": octave_range_str,
            "unique_pitches": len(unique_pitches)
        }

        logger.info(f"Goa arp generated: {len(notes)} notes, {len(unique_pitches)} unique pitches")
        return result

    except Exception as e:
        error_msg = f"Error generating Goa arp: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg
        }


def generate_buildup_riser(
    ableton_connection,
    track_index: int,
    start_bar: int,
    length_bars: int = 16,
    pitch_rise_semitones: int = 24,
    filter_sweep: bool = True,
    intensity: float = 0.7
) -> Dict[str, Any]:
    """
    Generate automated pitch rise + filter sweep for buildups.

    Parameters:
        ableton_connection: Active connection to Ableton
        track_index: Target track (usually FX track)
        start_bar: Where riser begins
        length_bars: Riser length in bars (default: 16)
        pitch_rise_semitones: Pitch rise amount in semitones (24 = 2 octaves) (default: 24)
        filter_sweep: Add filter cutoff automation (default: True)
        intensity: 0.0 = subtle, 1.0 = extreme (default: 0.7)

    Returns:
        Dictionary with generation results
    """

    logger.info(f"Generating buildup riser: {length_bars} bars at bar {start_bar}, pitch rise {pitch_rise_semitones}st")

    # Validate parameters
    if intensity < 0.0 or intensity > 1.0:
        raise ValueError(f"Intensity must be between 0.0 and 1.0, got {intensity}")

    if pitch_rise_semitones < 0 or pitch_rise_semitones > 48:
        raise ValueError(f"Pitch rise must be between 0 and 48 semitones, got {pitch_rise_semitones}")

    try:
        # Step 1: Create the clip
        clip_length = float(length_bars * 4)  # 4 beats per bar
        logger.info(f"Creating {clip_length}-beat riser clip at track {track_index}, bar {start_bar}")

        # Convert bar to clip slot (assuming clip slot = bar - 1, or use 0 if starting fresh)
        clip_slot = 0  # Place in first slot, user can fire at specific time

        ableton_connection.send_command("create_clip", {
            "track_index": track_index,
            "clip_index": clip_slot,
            "length": clip_length
        })

        # Step 2: Add a single sustained note (C2, MIDI note 36)
        # Duration spans the entire clip
        sustained_note_pitch = 36  # C2
        ticks_per_beat = 960  # Ableton PPQN
        total_ticks = int(clip_length * ticks_per_beat)

        note = {
            "pitch": sustained_note_pitch,
            "start_time": 0,
            "duration": total_ticks,
            "velocity": 100,
            "mute": False
        }

        ableton_connection.send_command("add_notes_to_clip", {
            "track_index": track_index,
            "clip_index": clip_slot,
            "notes": [note]
        })

        # Step 3: Add pitch bend automation (0 → pitch_rise_semitones)
        # Pitch bend automation in Ableton uses values from -8192 to 8191
        # We'll create a linear rise from 0 to max bend value
        # Assuming pitch bend range is set to ±2 semitones by default,
        # we need to calculate the bend value for the desired semitones
        # For 24 semitones (2 octaves) with ±2 semitone range, we need 12x the range
        # This is a simplification - in reality, pitch bend range should be configured on the synth

        # For now, we'll create envelope automation points
        # Start at 0, end at maximum bend scaled by pitch_rise_semitones
        automation_envelopes_created = 0

        # Note: The base ahujasid/ableton-mcp may not support automation envelopes yet
        # We'll attempt it, but it may require adding this command to the base MCP server
        try:
            # Pitch bend envelope (0 to 8191 for upward bend)
            pitch_bend_max = int(8191 * min(1.0, pitch_rise_semitones / 24.0))

            ableton_connection.send_command("add_clip_envelope", {
                "track_index": track_index,
                "clip_index": clip_slot,
                "parameter": "pitch_bend",
                "points": [
                    {"time": 0.0, "value": 0},
                    {"time": clip_length, "value": pitch_bend_max}
                ]
            })
            automation_envelopes_created += 1
            logger.info(f"Created pitch bend automation: 0 → {pitch_bend_max}")
        except Exception as envelope_error:
            logger.warning(f"Could not create pitch bend envelope: {envelope_error}")
            logger.warning("Pitch bend automation may need to be added manually")

        # Step 4: Add filter cutoff automation (200Hz → 8kHz) if enabled
        if filter_sweep:
            try:
                # Filter frequency typically ranges 0-1 (normalized)
                # We'll use exponential curve for more natural sweep
                # Start at ~0.1 (200Hz equivalent) and end at ~0.9 (8kHz equivalent)
                filter_start = 0.1 * (1.0 - intensity * 0.05)  # Slightly lower for higher intensity
                filter_end = 0.9 + (intensity * 0.1)  # Higher end for higher intensity

                ableton_connection.send_command("add_clip_envelope", {
                    "track_index": track_index,
                    "clip_index": clip_slot,
                    "parameter": "filter_frequency",
                    "points": [
                        {"time": 0.0, "value": filter_start},
                        {"time": clip_length * 0.5, "value": 0.5},  # Exponential curve
                        {"time": clip_length, "value": filter_end}
                    ]
                })
                automation_envelopes_created += 1
                logger.info(f"Created filter sweep automation: {filter_start} → {filter_end}")
            except Exception as filter_error:
                logger.warning(f"Could not create filter envelope: {filter_error}")
                logger.warning("Filter automation may need to be added manually")

        # Step 5: Add volume fade in (exponential curve)
        try:
            # Volume typically ranges 0-1
            # Exponential fade in for dramatic buildup
            volume_start = 0.0
            volume_end = 0.85 + (intensity * 0.15)  # Scale by intensity

            ableton_connection.send_command("add_clip_envelope", {
                "track_index": track_index,
                "clip_index": clip_slot,
                "parameter": "volume",
                "points": [
                    {"time": 0.0, "value": volume_start},
                    {"time": clip_length * 0.3, "value": 0.2},  # Exponential curve
                    {"time": clip_length * 0.7, "value": 0.5},
                    {"time": clip_length, "value": volume_end}
                ]
            })
            automation_envelopes_created += 1
            logger.info(f"Created volume fade automation: {volume_start} → {volume_end}")
        except Exception as volume_error:
            logger.warning(f"Could not create volume envelope: {volume_error}")
            logger.warning("Volume automation may need to be added manually")

        # Step 6: Name the clip
        clip_name = f"FC_Riser_{length_bars}bar_{pitch_rise_semitones}st"
        ableton_connection.send_command("set_clip_name", {
            "track_index": track_index,
            "clip_index": clip_slot,
            "name": clip_name
        })

        # Calculate bar range
        end_bar = start_bar + length_bars - 1
        bars_range = f"{start_bar}-{end_bar}"

        result = {
            "status": "success",
            "clip_created": True,
            "automation_envelopes": automation_envelopes_created,
            "pitch_rise": pitch_rise_semitones,
            "bars": bars_range,
            "clip_name": clip_name,
            "warnings": []
        }

        if automation_envelopes_created == 0:
            result["warnings"].append("No automation envelopes created - may need manual setup")
            result["warnings"].append("Base MCP server may not support add_clip_envelope command")

        logger.info(f"Buildup riser generated: {clip_name}, {automation_envelopes_created} envelopes")
        return result

    except Exception as e:
        error_msg = f"Error generating buildup riser: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg
        }
