# Flyin' Colors — Project Brief v1.0

> **Instructions:** Paste this at the start of every new agent conversation alongside any handoff brief. This is the single source of truth for the Flyin' Colors project. Update it as things change.

---

## Project Overview

### What Is Flyin' Colors?

**Flyin' Colors** is a groundbreaking Trance music project born from trauma—a sonic response to the October 7th, 2023 attacks on Israel, including the massacre at the Nova Festival where 1,400+ Israelis were slaughtered.

This music is:
- A defiant creative response to jihadist terror
- A sonic testament: "We will never stop dancing"
- An expression of collective Israeli PTSD and the constant search for "karahana" (the extreme peak/high)
- A demand for sovereignty and PLUR (Peace, Love, Unity, Respect)

**Parallel to My Chemical Romance:** Gerard Way witnessed 9/11 and created art from trauma. Avi witnessed October 7th and created Flyin' Colors. Both transform trauma into narrative-driven music.

---

## The Vision: Molecular-Level Genre Fusion

This is not simple genre blending—it's meticulous fusion at the molecular level of sound design and composition.

### The Three Pillars

#### Pillar 1: The Narrative of Resilience
Every track moves through emotional stages:
1. **The Horror** - Dissonant harmonies, industrial Psycore textures, aggressive Nu-Metal distortion (the sound of chaos and rubble)
2. **The Defiance** - Relentless Nitzhonot basslines, syncopated Nu-Metal drums (the refusal to submit, the "winning" spirit)
3. **The Triumph** - Soaring Goa Trance melodies, Classical beauty (the cathartic peak, the phoenix rising)

**Emotional arc is track-specific.** Not formulaic. Each track tells its own story based on its narrative.

#### Pillar 2: The Fusion of Contradictions

**Goa Trance & Nitzhonot** (The Foundation)
- Intricate arpeggiated sequences and melodic layers
- Driving 16th-note basslines
- 1990s Nitzhonot: fast rolling bass, raw unpolished energy
- PLUR philosophy as the ultimate goal
- The Israeli psyche's connection to Trance (overrepresentation in the genre due to PTSD)

**Nu-Metal & Metalcore** (The Aggression)
- Aggressive syncopated drumming and powerful distortion
- Heavy guitar textures translated into synthesis
- Percussive vocal chops
- Raw emotional delivery (rage, suffering, defiance)

**Psycore/Dark Psy** (The Psychoactive Edge)
- Highly distorted, chaotic, metallic textures
- Dark atmospheres that are felt, not just heard
- Aggressive guitar riffs in Trance context
- The industrial machine from the visual metaphor

**Modern Classical** (The Emotional Core)
- Melancholic, minimalist structures (Ludovico Einaudi)
- Narrative sophistication in intros, breakdowns, melodic themes
- Emotional depth beyond the dancefloor
- The secret weapon for cinematic elements

**Israeli Music** (The Heart & Soul)
- Hebrew spoken-word samples and quotes
- Linguistic and cultural identity
- Poignant social commentary with rhythmic flow
- Direct narrative embedding

#### Pillar 3: Technical Mastery
Every instruction is detailed, precise, and tailored to Ableton Live 12 Suite and the specific hardware/plugin setup. No guessing—meticulous building.

---

## Musical Parameters

| Parameter | Specification |
|-----------|--------------|
| **BPM** | 145+ (Nitzhonot range) |
| **Scales** | Goa Trance and Nitzhonot patterns analyzed from reference artists' actual tracks |
| **Track Length** | 6-12 minutes (epic journey format) |
| **Key Signatures** | Analyzed from reference tracks (typically minor keys: Am, Cm, Dm, Em, Fm, Gm) |
| **Arrangement** | Narrative-driven structure (not formulaic intro/buildup/drop) |
| **Emotional Arc** | Track-specific based on narrative concept |

---

## Reference Artists (Musical DNA Source)

### Goa Trance
Filteria, Man With No Name, Agneton, Hallucinogen, Astral Projection, Goasia, Simon Posford, Asia 2001, California Sunshine, Etnica, Pleiadians, K.O.B, Shakta, Morphic Resonance, Chi-ad, Celestial Intelligence, Cosmosis

### Psycore/Dark Psy
Will O Wisp, Kasatka, Audiosyntax, Yaminahua, SUN Project

### Nitzhonot
Eyal Iceman

### Psytrance
Infected Mushroom (pre-2007), Astrix

### Nu-Metal & Metalcore
Bring Me The Horizon (albums: Sempiternal, That's The Spirit, Post Human: Survival Horror), My Chemical Romance (albums: Three Cheers for Sweet Revenge, The Black Parade), System of a Down, Linkin Park, The Used, Architects, Deftones, Slipknot, Frank Klepacki (Red Alert soundtrack), Pierce The Veil, Polaris

### Modern & Classical
Ludovico Einaudi

### Israeli Music
Tuna, Ravid Plotnik (Hebrew spoken-word style reference)

---

## Tech Stack

### DAW & Controller
| Component | Details |
|-----------|---------|
| **DAW** | Ableton Live 12 Suite |
| **Controller** | Ableton Push 3 (standalone mode available) |
| **Audio Interface** | RME Fireface UCX II (pristine quality, ultra-low latency, hybrid analog/digital routing) |
| **Monitoring** | Dynaudio Core 7 speakers (brutally honest, clinically accurate) |

### VST Plugins (Complete List)
1. FabFilter (full suite) — surgical EQ and dynamics
2. iZotope RX 10 — audio cleanup
3. Sylenth1 — classic Trance sounds
4. Komplete Kontrol — unified instrument access
5. Kontakt — vast sample libraries
6. Massive — deep wavetable synthesis
7. Polyverse Music - Wider — stereo imaging
8. Sonic Academy - Kick 2 — custom kick design
9. Splice — sample sourcing
10. Vital — modern wavetable synthesis
11. Serum — advanced wavetable design

### Infrastructure (In Development)
| Layer | Technology | Status |
|-------|------------|--------|
| **Automation** | MCP Server (Python) → AbletonOSC → Ableton Live | Building incrementally |
| **Current Setup** | Single Windows PC (Ableton + Claude Code) | Active |
| **Future Setup** | Linux mini PC (bosegame) + Windows PC via Tailscale | When mini PC arrives |
| **Version Control** | Git | TBD |
| **State Tracking** | JSON session state files | In design |

---

## Current Template Pattern (from "War of the Worlds")

Avi's existing workflow extracted from active project:

### Track Organization
**22 MIDI Tracks:**
- Acid basslines (intro + main variations)
- Kick2, Snare/HH, Drums (DR #1-3)
- Pads: Vital, Serum, Massive (multiple instances)
- Leads: Sylenth, Acid V, Serum, Vital, Massive (#1-4)
- Narrative elements (spoken word, radio samples)
- Reference MIDI tracks

**52 Audio Tracks:**
- SFX (Aliens, Space, Water, Woosh effects, Spaceships)
- Spoken word (Jeff Wayne's War of the Worlds, Shakespeare)
- Reference tracks (Agneton, Pleiadians)
- Percussion/Pad/Lead audio bounces
- Stereo placement (L/R/Center)

**6 Return Tracks:**
- 3 Delays (Short/Medium/Long)
- 3 Reverbs (Short/Medium/Long)

### Key Patterns
- Separate intro/main variations of elements
- Multiple instances of same synth for different roles
- Heavy use of reference tracks loaded in project
- Organized return sends (S/M/L structure)
- Narrative/spoken word integration throughout

---

## The Workflow: Hybrid Automation

**Ideal interaction:**
- Claude handles technical execution (MIDI generation, automation, arrangement via MCP server)
- Avi maintains creative control at narrative/emotional decision points
- Semi-automated process: test what works, iterate based on results
- Build trust in automation over time

**Key principle:** The system serves the artist, not the other way around.

---

## Hebrew Spoken-Word Samples

**Sources:**
- Some already sourced (Avi has specific recordings)
- Ongoing sourcing help needed (Claude assists in finding appropriate samples)

**Usage:**
- Narrative lyrical element (not background decoration)
- Cultural and linguistic identity grounding
- Specific emotional/political messaging
- Hebrew quotes embedded directly into arrangement

---

## Visual Metaphors (Guide Production Decisions)

### The Machine to Melody
Industrial brutality (rusted gears, sharp metal, raw power) → Vibrant multicolored musical notes erupting (the "karahana"). The fusion of Nu-Metal/Psycore weight with Trance/Classical transcendence.

### The Phoenix
Destroyed instruments (Nova Festival rubble) at the base → Phoenix rising with wings made of musical notes → Peace dove shield with Hebrew "כמו" (kmo - "like/as if"). Defiant rebirth through sound.

---

## The Message

**Mixed messaging is intentional:**
- Horror AND joy
- Suffering AND victory
- Pain AND triumph
- Demand for sovereignty through sound
- Proof: We deserve PLUR. We will never stop dancing.

---

## Collaboration & Multi-User Support

- Others may work on these projects
- Need clear handoff documentation
- Version control for all project files
- Shared state tracking
- Transparent, auditable workflow

---

## Timeline & Approach

**Timeline:** Long-term quality build (months, not days)
**Philosophy:** Build it right, test thoroughly, iterate based on real-world use
**Mindset:** Never rush at the expense of quality or artistic integrity

---

## Current Status (Update This Section)

**Date:** 2026-02-13

**Active Work:**
- Building Flyin' Colors architecture and agent framework
- Designing MCP server for Ableton Live automation
- Adapting mastering-claude-code tier system for music production

**Completed:**
- Finalized tool list (hardware + plugins)
- Analyzed existing template ("War of the Worlds")
- Captured complete project vision and configuration

**Next Steps:**
- Complete agent architecture design
- Write individual agent prompts
- Build MCP server Phase 1 (basic transport + track creation)
- Design Push 3 integration workflow

---

## Notes for Agents

- This is art born from trauma
- Every technical decision serves the emotional and political narrative
- Respect the hardware/plugin constraints
- Semi-automated workflow: Claude executes, Avi decides
- Track-specific emotional arcs (not formulaic)
- Hebrew samples are narrative elements, not decoration
- Reference artists are for DNA extraction, not imitation
- Long-term build: quality over speed

---

**Remember:** This is not just music production. This is defiance through sound. This is a sonic declaration that we will never stop dancing.
