# Flyin' Colors — Music Production Agent Architecture v1.1

**Adapted from:** mastering-claude-code tier-based development system
**Purpose:** Professional music production workflow using specialized AI agents
**Update:** Added Reference Analyst for musical DNA extraction

---

## Architecture Overview

```
SHADOW CREATOR (Orchestrator)
├── Coordinates all agents
├── Maintains artistic vision
├── Makes creative decisions
└── Ensures narrative coherence

TIER 0: INFRASTRUCTURE (Foundation)
├── System Architect (MCP server, AbletonOSC, Push 3)
└── Reference Analyst (Musical DNA extraction) ← NEW

TIER 1: CONCEPT & VISION (Sequential)
├── Narrative Architect → Music Theory Architect

TIER 2: DESIGN (Parallel)
├── Sound Designer ←→ Arrangement Architect

TIER 3: PRODUCTION (Parallel)
├── MIDI Producer ←→ Automation Engineer

TIER 4: QUALITY (Sequential)
├── Mix Engineer → Mastering Engineer

TIER 5: DELIVERY
└── Export Manager

TIER 6: DOCUMENTATION (Async - Runs Throughout)
└── Technical Writer
```

---

## Complete Agent Roster (12 Agents)

### Shadow Creator (Orchestrator)
| Role | File | Function |
|------|------|----------|
| **Shadow Creator** | `00-shadow-creator.md` | Main orchestrator. Coordinates all agents. Makes creative/narrative decisions. |

### Tier 0: Infrastructure (Foundation)
| # | Agent | File | Role |
|---|-------|------|------|
| 0a | System Architect | `03-system-architect.md` | Technical infrastructure. MCP server, AbletonOSC, Push 3 integration. |
| 0b | **Reference Analyst** | `02-reference-analyst.md` | **Musical DNA extraction from reference artists.** ← NEW |

### Tier 1: Concept & Vision (Sequential)
| # | Agent | File | Role |
|---|-------|------|------|
| 1 | Narrative Architect | `04-narrative-architect.md` | Defines track concept, emotional arc, story, samples needed |
| 2 | Music Theory Architect | `05-music-theory-architect.md` | Defines key, scale, BPM, chord progressions, harmonic structure |

### Tier 2: Design (Parallel)
| # | Agent | File | Role |
|---|-------|------|------|
| 3 | Sound Designer | `06-sound-designer.md` | Synth selection, patch design, sound palette, timbre choices |
| 4 | Arrangement Architect | `07-arrangement-architect.md` | Track structure, sections, transitions, build/release points |

### Tier 3: Production (Parallel)
| # | Agent | File | Role |
|---|-------|------|------|
| 5 | MIDI Producer | `08-midi-producer.md` | Generates MIDI patterns, places notes, creates basslines/melodies/arps/drums |
| 6 | Automation Engineer | `09-automation-engineer.md` | Filter sweeps, volume curves, parameter automation, risers, impacts |

### Tier 4: Quality (Sequential)
| # | Agent | File | Role |
|---|-------|------|------|
| 7 | Mix Engineer | `10-mix-engineer.md` | Balance, EQ, compression, spatial placement, effects processing |
| 8 | Mastering Engineer | `11-mastering-engineer.md` | Final polish, loudness, frequency balance, export prep |

### Tier 5: Delivery
| # | Agent | File | Role |
|---|-------|------|------|
| 9 | Export Manager | `12-export-manager.md` | Bounces, formats, metadata, deliverables |

### Tier 6: Documentation (Async)
| # | Agent | File | Role |
|---|-------|------|------|
| 10 | Technical Writer | `13-technical-writer.md` | Documents process, settings, creative decisions, session notes |

---

## NEW: Reference Analyst Integration

### Purpose
Extract musical DNA from reference artists (Filteria, Pleiadians, Eyal Iceman, etc.) and translate it into actionable patterns for Flyin' Colors.

### What It Analyzes
- Ableton project files (.als)
- MIDI files (.mid)
- Listening descriptions (you describe, it formalizes)
- Visual materials (screenshots, spectrograms)
- Metadata and context

### What It Delivers
- **Musical DNA Reports** — Complete analysis with patterns, progressions, structure
- **MIDI Pattern Files** — Extracted basslines, arps, melodies
- **Sound Design Recipes** — Step-by-step synth recreation
- **Arrangement Templates** — Reusable structure templates
- **Application Guidance** — How to use DNA in Flyin' Colors context

### Workflow Integration

**Before production:**
```
1. Reference Analyst extracts DNA from reference tracks
2. Shadow Creator reviews DNA
3. Music Theory Architect uses DNA as foundation
4. Sound Designer recreates reference sounds + adds Flyin' Colors character
5. MIDI Producer uses patterns as templates
```

**Example:**
```
You: "Analyze Filteria's 'Birds Lingva Franca'"
Reference Analyst: [Extracts bass pattern, key, BPM, structure]

You → Shadow Creator: "Create a track using Filteria's DNA but darker"
Shadow Creator → Uses DNA as blueprint, adapts for narrative
```

---

## Workflow (Updated)

```
START: Avi provides concept to Shadow Creator
  ↓
Shadow Creator activates Tier 0 (if needed)

TIER 0: Reference Analysis (optional, before Tier 1)
  Reference Analyst: Extracts DNA from reference tracks
  System Architect: Builds infrastructure if needed
  ↓ DNA Report + Patterns

TIER 1: Narrative + Music Theory
  Narrative Architect: Defines story/emotional arc
  Music Theory Architect: Uses DNA + narrative to define key/scale/progression
  ↓ Handoff Brief

TIER 2: Sound Design + Arrangement
  Sound Designer: Uses DNA recipes + adds Flyin' Colors character
  Arrangement Architect: Uses DNA templates + adapts to narrative
  ↓ Handoff Brief

TIER 3: MIDI Production + Automation
  MIDI Producer: Uses DNA patterns as starting point, modifies for narrative
  Automation Engineer: Applies automation techniques from DNA
  ↓ Handoff Brief

TIER 4: Mix → Master
  Mix Engineer: Uses reference mixing approach
  Mastering Engineer: Targets reference loudness/quality
  ↓ Handoff Brief

TIER 5: Export
  Export Manager: Creates deliverables
  ↓

TIER 6: Technical Writer
  Documents DNA used, creative adaptations made
```

---

## Setup Instructions (Updated)

### NEW: Create Reference Analyst Project

1. Create Claude Project: "Reference Analyst - Flyin' Colors"
2. Add custom instructions:
   - `01-shared-context.md`
   - `FLYIN_COLORS_PROJECT_BRIEF.md`
   - `02-reference-analyst.md`
3. Create workspace:
   ```bash
   mkdir C:\trance-workspace\reference-analysis
   mkdir C:\trance-workspace\reference-analysis\ableton-projects
   mkdir C:\trance-workspace\reference-analysis\midi-patterns
   mkdir C:\trance-workspace\reference-analysis\reports
   ```

### Recommended Project Setup

**Essential (Create These First):**
1. Shadow Creator (main orchestrator)
2. Reference Analyst (DNA extraction)
3. System Architect (infrastructure)

**Production (Create When Needed):**
4. Narrative Architect
5. Music Theory Architect
6. Sound Designer
7. Arrangement Architect
8. MIDI Producer
9. Mix Engineer

**Or:** Use Shadow Creator in direct mode (acts as all agents)

---

## When to Use Reference Analyst

### **Before Starting Production**
```
New track → Identify reference artists → Reference Analyst extracts DNA →
Shadow Creator uses DNA as foundation
```

### **When Learning a Technique**
```
"How does Eyal Iceman make that rolling bass?" → Reference Analyst analyzes →
Shows exact pattern + sound design → You apply to your track
```

### **Building Pattern Library**
```
Analyze multiple tracks → Extract common patterns →
Build reusable MIDI template library
```

### **Understanding an Artist's Style**
```
Analyze full album → Find signature techniques →
Apply principles to Flyin' Colors
```

---

## Updated File Organization

```
flyin-colors-project/
├── agents/
│   ├── 00-shadow-creator.md
│   ├── 01-shared-context.md
│   ├── 02-reference-analyst.md ← NEW
│   ├── 03-system-architect.md
│   ├── 04-13-*.md (other agents)
│   └── README.md (this file)
├── templates/
│   └── FLYIN_COLORS_PROJECT_BRIEF.md
├── docs/
│   └── MUSIC_THEORY_KNOWLEDGE_BASE.md
└── technical/
    ├── MCP_SERVER_IMPLEMENTATION_PLAN.md
    ├── PUSH_3_INTEGRATION.md
    └── SINGLE_MACHINE_ARCHITECTURE.md
```

---

## Key Concepts (Updated)

### **DNA-Driven Production**
1. Reference Analyst extracts musical DNA from reference artists
2. Music Theory Architect uses DNA as harmonic foundation
3. Sound Designer recreates reference sounds + adds Flyin' Colors character
4. MIDI Producer uses DNA patterns as templates
5. Result: Grounded in proven techniques, adapted for unique vision

### **Contract-Based Production**
Music Theory Architect creates musical contract (key, scale, progression).
All agents follow this contract—no mismatched notes.

### **Narrative-First**
Narrative Architect defines emotional story BEFORE DNA extraction or sound design.
DNA serves the narrative, not the other way around.

### **Semi-Automated Execution**
- Tiers 0-2: Human-AI collaborative (creative decisions)
- Tier 3: Mostly automated via MCP (technical execution)
- Tier 4-5: Semi-automated (AI proposes, human approves)

---

**Architecture v1.1 — Now with Reference Analyst for musical DNA extraction**
