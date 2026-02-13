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
