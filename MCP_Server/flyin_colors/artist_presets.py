"""
Per-artist style presets derived from reference track DNA analysis.

Each artist preset contains averaged values from their analyzed tracks,
allowing you to dial in a specific artist's sonic fingerprint when creating
sessions or generating MIDI patterns.

Artists:
- Filteria (3 tracks: Speech Module, Navigate, Lunar Civilization remix)
- Pleiadians (2 tracks: Maia, Alcyone)
- Etnica (2 tracks: Starship 101, Vimana)
- Shakta (1 track: Arsim On Acid)
"""

import json
import logging

logger = logging.getLogger("FlyinColors.ArtistPresets")

ARTIST_PRESETS = {
    "filteria": {
        "display_name": "Filteria",
        "tracks_analyzed": [
            "Filteria - Speech Module",
            "Filteria - Navigate",
            "Crop Circles - Lunar Civilization (Filteria Higher Remix)",
        ],
        "track_count": 3,
        "tempo": {
            "avg_bpm": 146.4,
            "bpm_values": [143.6, 152.0, 143.6],
        },
        "key": {
            "detected_keys": ["C", "Am", "Dm"],
            "detected_scales": ["phrygian_dominant", "phrygian", "harmonic_minor"],
            "recommended_scale": "phrygian_dominant",
            "recommended_key": "Dm",
        },
        "bass": {
            "velocity_pattern_midi": [124, 126, 125, 126, 125, 125, 123, 124, 125, 125, 123, 124, 124, 125, 124, 124],
            "velocity_range": [121, 127],
        },
        "spectral": {
            "avg_centroid_hz": 2960,
            "per_track_centroids": [2991, 2817, 3073],
            "bass_filter_min_hz": 1023,
            "bass_filter_max_hz": 2000,
        },
        "frequency_distribution_pct": {
            "sub_bass": 52.1,
            "bass": 24.8,
            "low_mid": 11.2,
            "mid": 5.8,
            "high_mid": 3.2,
            "high": 2.9,
        },
        "harmony": {
            "avg_bars_per_chord_change": 10.0,
            "chord_change_values": [15.8, 8.2, 6.0],
        },
        "groove": {
            "avg_grid_deviation_ms": 25.4,
        },
        "character": (
            "Melodic, shimmering, psychedelic. Wide spectral spread with bright "
            "centroid (~2960Hz). Phrygian dominant/phrygian scales give exotic, "
            "Eastern-tinged melodic lines. Moderate chord movement (10 bars). "
            "Bass filter opens wide (1023-2000Hz). Less sub-heavy than average (52%)."
        ),
    },
    "pleiadians": {
        "display_name": "Pleiadians",
        "tracks_analyzed": [
            "Pleiadians - Maia",
            "Pleiadians - Alcyone",
        ],
        "track_count": 2,
        "tempo": {
            "avg_bpm": 143.6,
            "bpm_values": [143.6, 143.6],
        },
        "key": {
            "detected_keys": ["Gm", "A#"],
            "detected_scales": ["dorian", "harmonic_minor"],
            "recommended_scale": "harmonic_minor",
            "recommended_key": "Gm",
        },
        "bass": {
            "velocity_pattern_midi": [123, 126, 122, 125, 122, 126, 123, 122, 123, 124, 120, 122, 122, 123, 121, 122],
            "velocity_range": [117, 127],
        },
        "spectral": {
            "avg_centroid_hz": 3041,
            "per_track_centroids": [2953, 3128],
            "bass_filter_min_hz": 1076,
            "bass_filter_max_hz": 2000,
        },
        "frequency_distribution_pct": {
            "sub_bass": 56.1,
            "bass": 25.0,
            "low_mid": 9.8,
            "mid": 4.8,
            "high_mid": 2.5,
            "high": 1.8,
        },
        "harmony": {
            "avg_bars_per_chord_change": 11.3,
            "chord_change_values": [11.9, 10.7],
        },
        "groove": {
            "avg_grid_deviation_ms": 25.6,
        },
        "character": (
            "Hypnotic, spacious, cosmic. Brightest centroid of all artists (~3041Hz). "
            "Dorian/harmonic minor scales create a floating, ethereal quality. "
            "Slowest chord changes (11.3 bars) — long hypnotic drones. "
            "Wider velocity range (117-127) adds dynamic variation. "
            "Bass filter starts high (1076Hz), stays open."
        ),
    },
    "etnica": {
        "display_name": "Etnica",
        "tracks_analyzed": [
            "Etnica - Starship 101 (Original Mix)",
            "Etnica - Vimana (Original Mix)",
        ],
        "track_count": 2,
        "tempo": {
            "avg_bpm": 143.6,
            "bpm_values": [143.6, 143.6],
        },
        "key": {
            "detected_keys": ["F", "A#m"],
            "detected_scales": ["major", "major"],
            "recommended_scale": "harmonic_minor",
            "recommended_key": "Am",
        },
        "bass": {
            "velocity_pattern_midi": [122, 121, 120, 122, 121, 120, 124, 123, 121, 125, 126, 121, 122, 126, 121, 125],
            "velocity_range": [117, 127],
        },
        "spectral": {
            "avg_centroid_hz": 2386,
            "per_track_centroids": [2709, 2062],
            "bass_filter_min_hz": 797,
            "bass_filter_max_hz": 2000,
        },
        "frequency_distribution_pct": {
            "sub_bass": 54.4,
            "bass": 26.2,
            "low_mid": 10.4,
            "mid": 4.8,
            "high_mid": 2.4,
            "high": 1.8,
        },
        "harmony": {
            "avg_bars_per_chord_change": 3.5,
            "chord_change_values": [3.1, 3.8],
        },
        "groove": {
            "avg_grid_deviation_ms": 26.1,
        },
        "character": (
            "Dark, driving, deep. Lowest centroid of all artists (~2386Hz) — "
            "heavy low-end focus. Fastest chord changes (3.5 bars) give a restless, "
            "urgent harmonic rhythm. Bass filter starts low (797Hz) creating a "
            "darker, more constrained sound. Velocity accents on positions 10,13 "
            "(off-beat emphasis). Most groove deviation (26.1ms) — rawer feel."
        ),
    },
    "shakta": {
        "display_name": "Shakta",
        "tracks_analyzed": [
            "Shakta - Arsim On Acid",
        ],
        "track_count": 1,
        "tempo": {
            "avg_bpm": 152.0,
            "bpm_values": [152.0],
        },
        "key": {
            "detected_keys": ["Am"],
            "detected_scales": ["phrygian"],
            "recommended_scale": "phrygian",
            "recommended_key": "Am",
        },
        "bass": {
            "velocity_pattern_midi": [120, 124, 118, 125, 123, 120, 123, 122, 125, 123, 127, 123, 125, 119, 120, 115],
            "velocity_range": [115, 127],
        },
        "spectral": {
            "avg_centroid_hz": 2359,
            "per_track_centroids": [2359],
            "bass_filter_min_hz": 612,
            "bass_filter_max_hz": 1996,
        },
        "frequency_distribution_pct": {
            "sub_bass": 65.1,
            "bass": 22.0,
            "low_mid": 7.4,
            "mid": 3.0,
            "high_mid": 1.5,
            "high": 1.0,
        },
        "harmony": {
            "avg_bars_per_chord_change": 2.7,
            "chord_change_values": [2.7],
        },
        "groove": {
            "avg_grid_deviation_ms": 24.5,
        },
        "character": (
            "Aggressive, sub-heavy, fast. Fastest BPM (152) and fastest chord changes "
            "(2.7 bars). Widest velocity range (115-127) — most dynamic bass pattern. "
            "Darkest sound with 65% sub-bass energy and lowest filter start (612Hz). "
            "Phrygian scale adds tension. Tightest groove (24.5ms) — most precise."
        ),
    },
}


def get_available_artists():
    """Return list of available artist preset names."""
    return [
        {
            "name": key,
            "display_name": preset["display_name"],
            "track_count": preset["track_count"],
            "character_summary": preset["character"][:80] + "...",
        }
        for key, preset in ARTIST_PRESETS.items()
    ]


def apply_artist_style(artist: str):
    """
    Return the full DNA preset for a specific artist.

    This provides all the measured values from their reference tracks so you
    can use them to configure session creation, bass generation, arp patterns,
    narrative arc parameters, and mixing decisions.

    Parameters:
    - artist: Artist name (case-insensitive). One of: "filteria", "pleiadians", "etnica", "shakta"

    Returns dict with:
    - status: "success" or "error"
    - artist: Display name
    - preset: Full DNA preset dictionary
    - usage_hints: Practical tips for applying this artist's style
    """
    artist_key = artist.lower().strip()

    if artist_key not in ARTIST_PRESETS:
        available = ", ".join(ARTIST_PRESETS.keys())
        return {
            "status": "error",
            "message": f"Unknown artist '{artist}'. Available: {available}",
        }

    preset = ARTIST_PRESETS[artist_key]

    usage_hints = {
        "session_creation": {
            "recommended_bpm": preset["tempo"]["avg_bpm"],
            "recommended_key": preset["key"]["recommended_key"],
            "recommended_scale": preset["key"]["recommended_scale"],
        },
        "rolling_bass": {
            "velocity_pattern": preset["bass"]["velocity_pattern_midi"],
            "filter_hint": "closed" if preset["spectral"]["bass_filter_min_hz"] < 800 else "medium",
        },
        "groove": {
            "humanize": True,
            "humanize_amount": round(preset["groove"]["avg_grid_deviation_ms"] / 25.5, 2),
        },
        "narrative_arc": {
            "bass_filter_closed_hz": preset["spectral"]["bass_filter_min_hz"],
            "bass_filter_open_hz": preset["spectral"]["bass_filter_max_hz"],
            "sub_energy_target_pct": preset["frequency_distribution_pct"]["sub_bass"],
        },
        "harmony": {
            "bars_per_chord": preset["harmony"]["avg_bars_per_chord_change"],
            "tip": "faster chords = more restless energy" if preset["harmony"]["avg_bars_per_chord_change"] < 5 else "slow chords = hypnotic drones",
        },
    }

    return {
        "status": "success",
        "artist": preset["display_name"],
        "tracks_analyzed": preset["tracks_analyzed"],
        "preset": preset,
        "usage_hints": usage_hints,
    }
