# GoAI — Flyin' Colors Production System

**What:** Complete AI-assisted music production architecture for creating trauma-based Trance music
**Who:** Avi (non-developer, vibe coder) + Claude (co-creator AI)
**Why:** Transform October 7th trauma into defiant, triumphant music using semi-automated production workflow

---

## Quick Navigation

**New here? Start with:**
1. [QUICK_START_CHECKLIST.md](QUICK_START_CHECKLIST.md) — Get from zero to first production session (4-6 hours)
2. [docs/INTEGRATION_WORKFLOW.md](docs/INTEGRATION_WORKFLOW.md) — How all the pieces fit together

**Core Architecture:**
- [flyin-colors-architecture/](flyin-colors-architecture/) — Complete 12-agent system, knowledge bases, MCP commands
- [flyin-colors-architecture/agents/README.md](flyin-colors-architecture/agents/README.md) — Architecture overview

**Planning & Guides:**
- [docs/guides/FLYIN_COLORS_ARCHITECTURE_REVIEW_2.md](docs/guides/FLYIN_COLORS_ARCHITECTURE_REVIEW_2.md) — 50 improvements with timeline
- [docs/guides/CONSOLIDATED_PROJECT_MAP.md](docs/guides/CONSOLIDATED_PROJECT_MAP.md) — How to merge 11 agents → 4 Claude Projects
- [docs/guides/CONTEXT_WINDOW_BUDGET.md](docs/guides/CONTEXT_WINDOW_BUDGET.md) — Token math for each project

**Production Templates:**
- [templates/CONTINUATION_BRIEF_TEMPLATE.md](templates/CONTINUATION_BRIEF_TEMPLATE.md) — Resume work between sessions
- [templates/FAST_CAPTURE_BRIEF_TEMPLATE.md](templates/FAST_CAPTURE_BRIEF_TEMPLATE.md) — Capture spontaneous ideas
- [templates/REJECTION_BRIEF_TEMPLATE.md](templates/REJECTION_BRIEF_TEMPLATE.md) — Send feedback upstream
- [templates/PROMPT_AB_TEST_TEMPLATE.md](templates/PROMPT_AB_TEST_TEMPLATE.md) — Test prompt improvements

**Tools:**
- [librosa_analysis_pipeline.py](librosa_analysis_pipeline.py) — Semi-automated reference track analysis
- [requirements.txt](requirements.txt) — Python dependencies

**Archive:**
- [docs/archive/](docs/archive/) — Historical documentation and deprecated files

---

## What This System Does

### The Vision
Create professional Trance music that fuses:
- **Goa Trance** (Filteria, Pleiadians) — Arpeggiated sequences, psychedelic atmospheres
- **Nitzhonot** (Eyal Iceman) — Fast rolling bass, 145+ BPM, "winning" energy
- **Nu-Metal** (BMTH, MCR) — Syncopated drums, emotional aggression, distorted textures
- **Psycore** — Chaotic metallic textures, dark atmospheres
- **Modern Classical** (Einaudi) — Melodic minimalism, emotional depth

Narrative arc: **Horror → Defiance → Triumph** (responding to October 7th trauma)

### The Workflow

**Option A: Single Project (Recommended for First Track)**
```
You → Shadow Creator (Claude Project)
     ├─ Acts as all agents in one conversation
     ├─ Narrative → Theory → Design → MIDI → Mix
     └─ You execute in Ableton manually

Time to first music: 4-6 hours of setup + production time
```

**Option B: 4-Project Specialized (After 1-2 Tracks)**
```
Shadow Creator → Production Studio → Quality Control → System Architect
     ↓                ↓                    ↓                 ↓
  Concept        Sound + MIDI          Mix + Master      Infrastructure
  + Theory       + Arrangement         + Export          + Docs

Handoff briefs passed between projects
Time to first music: 10-12 hours of setup + production time
```

**Option C: Ableton Automation (30 min setup)**
```
You → Claude Desktop → ahujasid/ableton-mcp → Ableton Live (automated)
          ↓                                           ↓
   Shadow Creator guidance                   Track/MIDI/instrument creation
   (Claude Projects web)                     (automated via MCP server)

Requires: Install UV + configure Claude Desktop (30 min)
See: flyin-colors-architecture/technical/ABLETON_MCP_SETUP.md
```

---

## File Organization

```
GoAI/
├── README.md (this file)
├── CLAUDE.md (Claude Code project context)
├── QUICK_START_CHECKLIST.md          ← START HERE
├── requirements.txt
├── librosa_analysis_pipeline.py
│
├── templates/                         Production templates
│   ├── CONTINUATION_BRIEF_TEMPLATE.md
│   ├── FAST_CAPTURE_BRIEF_TEMPLATE.md
│   ├── REJECTION_BRIEF_TEMPLATE.md
│   └── PROMPT_AB_TEST_TEMPLATE.md
│
├── docs/
│   ├── INTEGRATION_WORKFLOW.md       How it all fits together
│   ├── guides/                        Planning & setup guides
│   │   ├── FLYIN_COLORS_ARCHITECTURE_REVIEW_2.md
│   │   ├── CONSOLIDATED_PROJECT_MAP.md
│   │   └── CONTEXT_WINDOW_BUDGET.md
│   ├── archive/                       Historical docs
│   │   ├── CRITICAL_FIXES_APPLIED.md
│   │   ├── CRITICAL_RETHINKING_APPLIED.md
│   │   ├── IMPROVEMENTS_COMPLETED.md
│   │   ├── TRANCE_PRODUCTION_ARCHITECTURE.md
│   │   └── librosa_analysis_pipeline_old.py
│   └── session-states/                Exported session states (future)
│
└── flyin-colors-architecture/         Core architecture
    ├── agents/                        12 specialized AI agents
    │   ├── README.md
    │   ├── 00-shadow-creator.md
    │   ├── 01-shared-context.md
    │   ├── IO_CONTRACT_TEMPLATE.md
    │   └── 02-13-*.md
    ├── templates/
    │   └── FLYIN_COLORS_PROJECT_BRIEF.md
    ├── docs/
    │   ├── MUSIC_THEORY_KNOWLEDGE_BASE.md
    │   ├── BPM_TO_TIME_REFERENCE.md
    │   ├── FREQUENCY_RANGE_OWNERSHIP.md
    │   └── GIT_WORKFLOW.md
    ├── technical/
    │   ├── ABLETON_MCP_SETUP.md
    │   ├── MCP_CUSTOM_COMMANDS.md    12 custom Flyin' Colors commands
    │   ├── MCP_SERVER_IMPLEMENTATION_PLAN_OLD.md
    │   ├── PUSH_3_INTEGRATION.md
    │   └── SINGLE_MACHINE_ARCHITECTURE.md
    ├── SHADOW_CREATOR_SETUP.md
    ├── SHADOW_CREATOR_CONSOLIDATED.md
    └── REFERENCE_ANALYST_SETUP.md
```

---

## Current Status

**Phase:** Architecture complete, ready for implementation
**Next Action:** Follow QUICK_START_CHECKLIST.md Phase 0-1
**Timeline:** 4-6 hours to first production-ready session

### What's Complete
- ✅ 12-agent architecture designed
- ✅ Templates created (continuation, fast-capture, rejection, A/B test)
- ✅ librosa analysis pipeline built
- ✅ Context window budget calculated
- ✅ Integration workflow documented
- ✅ Quick start checklist created
- ✅ Filled template examples added
- ✅ Implementation timeline added to architecture review

### What's Not Started
- ⬜ Shadow Creator project creation (Phase 1, 4-6 hours)
- ⬜ Ableton MCP setup (optional, 30 min) — automates track/MIDI creation
- ⬜ Reference track analysis (Phase 3, ongoing)
- ⬜ Style-fingerprint development (Phase 3-4, ongoing)

---

## Technology Stack

**DAW:** Ableton Live 12 Suite
**Hardware:**
- Push 3 (hands-on MIDI performance)
- RME Fireface UCX II (audio interface)
- Dynaudio Core 7 (monitors)

**Plugins:**
- **Synths:** Serum, Vital, Massive, Sylenth1, Kontakt
- **FX:** FabFilter (Pro-Q 3, Pro-C 2, Pro-L 2), iZotope RX 10, Saturn 2, Polyverse Wider
- **Drums:** Sonic Academy Kick 2, samples

**AI:**
- Claude Sonnet 4.5 / Opus 4.6 (via Claude Projects or Claude Code)
- MCP (Model Context Protocol) for automation (future)

**Analysis:**
- Python 3.9+ with librosa, numpy, soundfile, matplotlib

---

## Three Paths to Your First Track

### Path 1: Fastest (4-6 hours setup)
1. Do QUICK_START_CHECKLIST.md Phase 0-1
2. Create Shadow Creator project only
3. Start producing manually in Ableton
4. Use Shadow Creator as advisor/co-pilot

**Pros:** Fastest to music, learn by doing
**Cons:** No automation, manual execution

### Path 2: Balanced (10-12 hours setup)
1. Do QUICK_START_CHECKLIST.md Phase 0-1
2. Create all 4 Claude Projects (CONSOLIDATED_PROJECT_MAP.md)
3. Analyze 2-3 reference tracks (librosa pipeline)
4. Start producing with specialized agents

**Pros:** Better workflow, specialized agents, reference library started
**Cons:** More upfront work before making sound

### Path 3: Full Build (15-20 hours setup)
1. Do QUICK_START_CHECKLIST.md Phase 0-1
2. Create all 4 Claude Projects
3. Set up ahujasid/ableton-mcp (30 min automation)
4. Analyze 5+ reference tracks
5. Develop style-fingerprint files

**Pros:** Automation, rich knowledge base, production-ready
**Cons:** Upfront investment before making music (but faster than custom MCP build)

**Recommendation:** Path 1 for first track, Path 2 for second track, Path 3 for long-term (after 3-5 tracks)

---

## Key Concepts

### DNA-Driven Production
Extract musical patterns from reference artists (Filteria, Pleiadians, Eyal Iceman) using librosa analysis pipeline → adapt for Flyin' Colors unique vision.

### Narrative-First Workflow
Every musical decision serves the emotional story (Horror → Defiance → Triumph). No generic trance formulas.

### Semi-Automated Execution
- **Tiers 0-2:** Human-AI collaborative (creative decisions)
- **Tier 3:** Automated via MCP server (technical execution) — future
- **Tiers 4-5:** Semi-automated (AI proposes, human approves)

### Contract-Based Production
Music Theory Architect defines key, scale, progression → all agents follow this contract → no mismatched notes.

### Fast-Capture Mode
Reverse workflow for spontaneous creation: Jam first → extract DNA → find narrative → build outward. Preserves creative momentum.

---

## Getting Help

**Architecture questions:** Read INTEGRATION_WORKFLOW.md
**Setup questions:** Follow QUICK_START_CHECKLIST.md step-by-step
**During production:** Use templates (CONTINUATION_BRIEF, FAST_CAPTURE_BRIEF, REJECTION_BRIEF)
**Improvements:** See FLYIN_COLORS_ARCHITECTURE_REVIEW_2.md for the 50 documented improvements

**Emergency:** "I'm lost" → Go to INTEGRATION_WORKFLOW.md bottom section ("Emergency: Which Doc Do I Need?")

---

## License & Attribution

- **Flyin' Colors Architecture:** Created by Avi + Claude (2026)
- **Framework Adapted From:** mastering-claude-code v4.4 (tier-based agent system)
- **Music:** All rights reserved (trauma-based artistic work)
- **Code/Templates:** MIT License (feel free to adapt for your projects)

---

**Make music. Everything else is just infrastructure.**
