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
    ],
    "dark_goa": [
        {"name": "FC_Kick", "type": "midi", "group": "Drums", "hint": "deep_kick"},
        {"name": "FC_Hats", "type": "midi", "group": "Drums", "hint": "minimal_hats"},
        {"name": "FC_Perc", "type": "midi", "group": "Drums", "hint": "tribal_perc"},
        {"name": "FC_Sub", "type": "midi", "group": "Bass", "hint": "heavy_sub"},
        {"name": "FC_RollingBass", "type": "midi", "group": "Bass", "hint": "dark_rolling"},
        {"name": "FC_Lead", "type": "midi", "group": "Melodic", "hint": "dark_lead"},
        {"name": "FC_Pad", "type": "midi", "group": "Melodic", "hint": "drone_pad"},
        {"name": "FC_Arp", "type": "midi", "group": "Melodic", "hint": "hypnotic_arp"},
        {"name": "FC_FX", "type": "audio", "group": "FX", "hint": "dark_fx"},
        {"name": "FC_Vocal", "type": "audio", "group": "FX", "hint": "dark_vocal"},
        {"name": "FC_Reference", "type": "audio", "group": None, "muted": True}
    ],
    "bright_goa": [
        {"name": "FC_Kick", "type": "midi", "group": "Drums", "hint": "punchy_kick"},
        {"name": "FC_Hats", "type": "midi", "group": "Drums", "hint": "open_hats"},
        {"name": "FC_Perc", "type": "midi", "group": "Drums", "hint": "shaker_perc"},
        {"name": "FC_Sub", "type": "midi", "group": "Bass", "hint": "tight_sub"},
        {"name": "FC_RollingBass", "type": "midi", "group": "Bass", "hint": "bright_rolling"},
        {"name": "FC_Lead", "type": "midi", "group": "Melodic", "hint": "soaring_lead"},
        {"name": "FC_Pad", "type": "midi", "group": "Melodic", "hint": "airy_pad"},
        {"name": "FC_Arp", "type": "midi", "group": "Melodic", "hint": "melodic_arp"},
        {"name": "FC_FX", "type": "audio", "group": "FX", "hint": "bright_fx"},
        {"name": "FC_Vocal", "type": "audio", "group": "FX", "hint": "bright_vocal"},
        {"name": "FC_Reference", "type": "audio", "group": None, "muted": True}
    ],
    "standard_goa": [
        {"name": "FC_Kick", "type": "midi", "group": "Drums", "hint": "standard_kick"},
        {"name": "FC_Hats", "type": "midi", "group": "Drums", "hint": "standard_hats"},
        {"name": "FC_Perc", "type": "midi", "group": "Drums", "hint": "standard_perc"},
        {"name": "FC_Sub", "type": "midi", "group": "Bass", "hint": "standard_sub"},
        {"name": "FC_RollingBass", "type": "midi", "group": "Bass", "hint": "standard_rolling"},
        {"name": "FC_Lead", "type": "midi", "group": "Melodic", "hint": "standard_lead"},
        {"name": "FC_Pad", "type": "midi", "group": "Melodic", "hint": "standard_pad"},
        {"name": "FC_Arp", "type": "midi", "group": "Melodic", "hint": "standard_arp"},
        {"name": "FC_FX", "type": "audio", "group": "FX", "hint": "standard_fx"},
        {"name": "FC_Vocal", "type": "audio", "group": "FX", "hint": "standard_vocal"},
        {"name": "FC_Reference", "type": "audio", "group": None, "muted": True}
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
    "jam": "bass_drums_only",
    "dark_goa": "all_tracks_dark_goa",
    "bright_goa": "all_tracks_bright_goa",
    "standard_goa": "all_tracks_standard_goa",
}

# Goa Trance style presets derived from 8-track reference analysis clustering
# Tracks cluster by spectral centroid into dark (~2100Hz), bright (~3100Hz), standard (~2750Hz)
GOA_STYLE_PRESETS = {
    "dark_goa": {
        "target_centroid_hz": 2100,
        "recommended_scale": "harmonic_minor",
        "bass_filter_range": (600, 1200),
        "sub_energy_target_pct": 58,
        "frequency_distribution_pct": {
            "sub_bass": 58.0,
            "bass": 26.0,
            "low_mid": 9.0,
            "mid": 4.0,
            "high_mid": 2.0,
            "high": 1.0,
        },
        "reference_tracks": ["Etnica - Vimana", "Shakta - Arsim On Acid"],
        "reference_centroids_hz": [2062, 2359],
        "recommended_bpm": 145,
        "harmony_bars_per_chord": 12.0,
        "description": "Deep, dark atmosphere. Heavy sub bass, minimal highs. "
                       "Hypnotic harmonic drones with slow chord movement. "
                       "Bass filter stays low (600-1200Hz). Etnica/Shakta territory.",
    },
    "bright_goa": {
        "target_centroid_hz": 3100,
        "recommended_scale": "phrygian",
        "bass_filter_range": (900, 2000),
        "sub_energy_target_pct": 52,
        "frequency_distribution_pct": {
            "sub_bass": 52.0,
            "bass": 24.0,
            "low_mid": 11.0,
            "mid": 6.5,
            "high_mid": 3.5,
            "high": 3.0,
        },
        "reference_tracks": ["Pleiadians - Alcyone", "Crop Circles - Lunar Civilization (Filteria Remix)"],
        "reference_centroids_hz": [3128, 3073],
        "recommended_bpm": 148,
        "harmony_bars_per_chord": 4.0,
        "description": "Airy, shimmering atmosphere. More mid/high presence, faster harmonic movement. "
                       "Bass filter opens wider (900-2000Hz). Phrygian/dorian scales. "
                       "Pleiadians/Filteria territory.",
    },
    "standard_goa": {
        "target_centroid_hz": 2750,
        "recommended_scale": "harmonic_minor",
        "bass_filter_range": (888, 2000),
        "sub_energy_target_pct": 55,
        "frequency_distribution_pct": {
            "sub_bass": 55.3,
            "bass": 25.3,
            "low_mid": 10.2,
            "mid": 4.9,
            "high_mid": 2.5,
            "high": 1.6,
        },
        "reference_tracks": [
            "Filteria - Speech Module", "Filteria - Navigate",
            "Etnica - Starship 101", "Pleiadians - Maia",
        ],
        "reference_centroids_hz": [2991, 2817, 2709, 2953],
        "recommended_bpm": 146,
        "harmony_bars_per_chord": 7.8,
        "description": "Balanced Goa trance. Average of all 8 reference tracks. "
                       "Sub-bass dominant (55%) with moderate mid presence. "
                       "Bass filter opens from ~888Hz to ~2000Hz across sections. "
                       "Harmonic minor and natural minor scales.",
    },
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
