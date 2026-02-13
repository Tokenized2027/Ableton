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
