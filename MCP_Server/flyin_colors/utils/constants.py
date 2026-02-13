"""
Constants for Flyin' Colors session templates and configurations
"""

# Standard Flyin' Colors track layout
FLYIN_COLORS_TRACKS = {
    "full": [
        {"name": "FC_Kick", "type": "midi", "group": "Drums"},
        {"name": "FC_Hats", "type": "midi", "group": "Drums"},
        {"name": "FC_Perc", "type": "midi", "group": "Drums"},
        {"name": "FC_Sub", "type": "midi", "group": "Bass"},
        {"name": "FC_RollingBass", "type": "midi", "group": "Bass"},
        {"name": "FC_Lead", "type": "midi", "group": "Melodic"},
        {"name": "FC_Pad", "type": "midi", "group": "Melodic"},
        {"name": "FC_Arp", "type": "midi", "group": "Melodic"},
        {"name": "FC_FX", "type": "audio", "group": "FX"},
        {"name": "FC_Vocal", "type": "audio", "group": "FX"},
        {"name": "FC_Reference", "type": "audio", "group": None, "muted": True}
    ],
    "minimal": [
        {"name": "FC_Kick", "type": "midi", "group": "Drums"},
        {"name": "FC_Sub", "type": "midi", "group": "Bass"},
        {"name": "FC_RollingBass", "type": "midi", "group": "Bass"},
        {"name": "FC_Lead", "type": "midi", "group": "Melodic"}
    ],
    "jam": [
        {"name": "FC_Kick", "type": "midi", "group": "Drums"},
        {"name": "FC_Hats", "type": "midi", "group": "Drums"},
        {"name": "FC_RollingBass", "type": "midi", "group": "Bass"}
    ]
}

# Return track configuration
FLYIN_COLORS_SENDS = [
    {"name": "FC_Reverb_Short", "effect": "Reverb", "decay": 0.8},
    {"name": "FC_Reverb_Long", "effect": "Reverb", "decay": 3.5},
    {"name": "FC_Delay", "effect": "Delay", "type": "ping_pong"},
    {"name": "FC_Distortion", "effect": "Saturator", "drive": "medium"}
]

# Section type mappings
SECTION_TYPES = {
    "full": "all_tracks",
    "minimal": "kick_bass_lead",
    "jam": "bass_drums_only"
}

# Goa Trance DNA - consensus values from 8-track reference analysis
# Source: reference-analysis/COMBINED_GOA_DNA.json
# Tracks: Filteria (Speech Module, Navigate), Etnica (Starship 101, Vimana),
#          Shakta (Arsim On Acid), Crop Circles (Lunar Civilization),
#          Pleiadians (Maia, Alcyone)
GOA_TRANCE_DNA = {
    "tempo": {
        "avg_bpm": 145.7,
        "bpm_range": [143.6, 152.0],
        "dominant_bpm": 143.6,
    },
    "key": {
        "dominant_mode": "minor",
        "top_scales": ["harmonic_minor", "natural_minor", "phrygian", "phrygian_dominant"],
        "scale_scores": {
            "natural_minor": 0.345,
            "harmonic_minor": 0.354,
            "phrygian": 0.306,
            "phrygian_dominant": 0.302,
            "dorian": 0.271,
            "major": 0.276,
        },
    },
    "bass": {
        "pattern": "rolling_16th",
        "avg_onsets_per_bar": 6.0,
        "velocity_pattern_midi": [123, 124, 122, 125, 123, 123, 123, 123, 123, 124, 123, 122, 123, 124, 122, 122],
        "grid_histogram": [0.81, 0.86, 0.82, 0.96, 0.81, 0.88, 0.83, 0.93, 0.83, 0.88, 0.82, 0.95, 0.81, 0.9, 0.8, 0.92],
    },
    "arp": {
        "rate": "16th",
        "avg_onsets_per_bar": 7.9,
        "grid_histogram": [0.82, 0.89, 0.82, 0.94, 0.82, 0.9, 0.83, 0.97, 0.83, 0.9, 0.84, 0.96, 0.82, 0.88, 0.83, 0.96],
    },
    "spectral": {
        "avg_centroid_hz": 2762,
        "centroid_range_hz": [2062, 3128],
        "bass_filter_proxy": {
            "closed_hz": 888,
            "open_hz": 2000,
            "intro_avg_hz": 1701,
            "middle_avg_hz": 1898,
            "outro_avg_hz": 1878,
        },
    },
    "frequency_distribution_pct": {
        "sub_bass": 55.3,
        "bass": 25.3,
        "low_mid": 10.2,
        "mid": 4.9,
        "high_mid": 2.5,
        "high": 1.6,
    },
    "harmony": {
        "avg_bars_per_chord_change": 7.8,
        "chord_change_range": [2.7, 15.8],
    },
    "groove": {
        "avg_grid_deviation_ms": 25.5,
        "quantized": False,
    },
}
