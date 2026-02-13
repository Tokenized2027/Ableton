# Reference Analyst Setup Guide

**Agent:** Reference Analyst (Musical DNA Extractor)
**Purpose:** Analyze reference tracks/albums from your artist list
**Output:** Detailed DNA reports with patterns, scales, arrangements, sound design

---

## Quick Setup (Claude Projects)

### Step 1: Create Project
**Name:** `Reference Analyst - Flyin' Colors`
**Description:** `Musical DNA extraction from reference artists`

### Step 2: Add Custom Instructions

Paste these 3 files in order:

1. `C:\Users\Avi\Desktop\GoAI\flyin-colors-architecture\agents\01-shared-context.md`
2. `C:\Users\Avi\Desktop\GoAI\flyin-colors-architecture\templates\FLYIN_COLORS_PROJECT_BRIEF.md`
3. `C:\Users\Avi\Desktop\GoAI\flyin-colors-architecture\agents\02-reference-analyst.md`

### Step 3: Create Reference Analysis Workspace

```bash
mkdir C:\trance-workspace\reference-analysis
mkdir C:\trance-workspace\reference-analysis\ableton-projects
mkdir C:\trance-workspace\reference-analysis\midi-patterns
mkdir C:\trance-workspace\reference-analysis\reports
mkdir C:\trance-workspace\reference-analysis\sound-design
```

---

## How to Use

### **Scenario 1: Analyze Ableton Project**

**You do:**
1. Load reference track in Ableton
2. Roughly transcribe bassline/arp (doesn't need to be perfect)
3. Save as: `C:\trance-workspace\reference-analysis\ableton-projects\Filteria_Birds.als`

**Tell Reference Analyst:**
```
Analyze C:\trance-workspace\reference-analysis\ableton-projects\Filteria_Birds.als

Extract:
- Bassline MIDI pattern
- Arp pattern
- Chord progression
- Arrangement structure
- Sound design approach
```

**Reference Analyst delivers:**
- Complete DNA report
- MIDI patterns extracted
- Sound design recipes
- Application guidance for Flyin' Colors

---

### **Scenario 2: Analyze MIDI Files**

**You do:**
1. Extract MIDI from reference track (using Melodyne, etc.)
2. Save as: `C:\trance-workspace\reference-analysis\midi-patterns\filteria_bass.mid`

**Tell Reference Analyst:**
```
Analyze C:\trance-workspace\reference-analysis\midi-patterns\filteria_bass.mid

This is the bassline from Filteria's "Birds Lingva Franca"
Extract the pattern, rhythm, velocity, and show me how to use it
```

**Reference Analyst delivers:**
- Pattern analysis
- Velocity map
- Rhythmic structure
- Recreation instructions for Serum/Vital

---

### **Scenario 3: Describe What You Hear**

**Tell Reference Analyst:**
```
I'm listening to Pleiadians - "Maia"

What I hear:
- Fast rolling bassline, sounds like 16th notes
- In a minor key, maybe Am or Em
- Arp goes up and down, 4-5 notes
- BPM around 145
- Has a big filter sweep around 2 minutes in

Extract the DNA and show me how to recreate it
```

**Reference Analyst delivers:**
- Formalized musical description
- Likely key, scale, progression
- MIDI pattern suggestions
- Step-by-step recreation guide

---

### **Scenario 4: Full Album Analysis**

**Tell Reference Analyst:**
```
I want to analyze Filteria's "Daze of our Lives" album

Tracks to focus on:
1. Birds Lingva Franca
2. The Big Blue
3. A Day on the Beach

Extract common DNA across all three:
- What makes Filteria's bass sound unique?
- What's his signature arp pattern?
- What scales/keys does he prefer?
- What's his arrangement structure?
```

**Reference Analyst delivers:**
- Multi-track comparative analysis
- Artist signature patterns
- Common techniques across tracks
- Consolidated DNA report

---

## What You'll Get

### 1. Musical DNA Report
Complete markdown document with:
- Basic parameters (BPM, key, scale)
- Harmonic structure (progressions)
- Bassline DNA (exact MIDI patterns)
- Melodic structures (arps, leads)
- Drum patterns
- Arrangement structure (timeline)
- Automation techniques
- Sound design recipes
- Flyin' Colors application guide

### 2. MIDI Pattern Files
Extracted patterns saved as .mid files:
- `filteria_bass_rolling_Dm.mid`
- `filteria_arp_4note_Dm.mid`
- `pleiadians_lead_melody_Am.mid`

### 3. Sound Design Recipes
Step-by-step instructions to recreate sounds in your synths:
```
Bass in Serum:
- Oscillator 1: Saw wave
- Oscillator 2: Square, detune +7 cents
- Filter: LP 24dB @ 800 Hz, res 0.4
- FX: Distortion (tube) → Compressor
```

### 4. Arrangement Templates
Reusable structure templates:
```json
{
  "intro": 32,
  "buildup1": 16,
  "drop1": 32,
  "breakdown": 32,
  "buildup2": 16,
  "drop2": 48,
  "outro": 32
}
```

---

## Integration with Production Workflow

### **Before Starting a New Track:**

1. **Pick reference artists** for this track's vibe
2. **Use Reference Analyst** to extract DNA
3. **Feed DNA to Shadow Creator** → Music Theory Architect
4. **Apply patterns** via MIDI Producer
5. **Recreate sounds** via Sound Designer

### **Example Workflow:**

```
You → Reference Analyst: "Analyze Eyal Iceman's Nitzhonot sound"
Reference Analyst → Extracts rolling bass pattern, BPM 148, key preferences

You → Shadow Creator: "Create a track using Eyal Iceman's DNA but darker and more aggressive"
Shadow Creator → Music Theory Architect: Uses Eyal's key/scale
Shadow Creator → Sound Designer: Uses Eyal's bass sound + adds distortion
Shadow Creator → MIDI Producer: Uses Eyal's pattern + modifies for narrative
```

---

## Best Practices

### **Start with Key Tracks**
Pick 3-5 "signature" tracks from each reference artist:
- Filteria: "Birds Lingva Franca", "The Big Blue"
- Pleiadians: "Maia", "Asterope"
- Eyal Iceman: Core Nitzhonot tracks

### **Transcribe Key Elements Only**
You don't need to recreate entire tracks, just:
- Bassline (most important)
- Main arp or lead melody
- Basic drum pattern
- Chord progression

### **Build a Pattern Library**
Create folders:
```
C:\trance-workspace\reference-analysis\
├── bassline-patterns\
│   ├── nitzhonot-rolling-16ths.mid
│   └── goa-walking-bass.mid
├── arp-patterns\
│   ├── classic-4note-arp.mid
│   └── triplet-rolling-arp.mid
└── drum-patterns\
    ├── four-on-floor-145bpm.mid
    └── nitzhonot-hats.mid
```

---

## First Analysis Recommendation

**Start here:**
```
Artist: Filteria
Track: "Birds Lingva Franca"
Why: Signature Goa sound, clear structure, perfect DNA source
```

**Steps:**
1. Load track in Ableton
2. Find the BPM (probably ~145)
3. Transcribe just the bassline (first 4-8 bars is enough)
4. Save project
5. Tell Reference Analyst to analyze it

---

## Example Opening Message

```
Hello, Reference Analyst.

I have Filteria's "Birds Lingva Franca" loaded in Ableton. I've transcribed the bassline roughly.

Project file: C:\trance-workspace\reference-analysis\ableton-projects\Filteria_Birds.als

Please extract:
1. Bassline MIDI pattern (exact notes, rhythm, velocity)
2. BPM and key
3. Chord progression
4. Arrangement structure (when sections change)
5. Sound design approach for the bass

Show me how to apply this DNA to a Flyin' Colors track.
```

---

**The Reference Analyst is ready to extract musical DNA from your favorite artists.**
