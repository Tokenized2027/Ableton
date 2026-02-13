# Flyin' Colors — Complete Production Architecture

**Version:** 1.0
**Created:** February 13, 2026
**Author:** Avi + Claude (Shadow Creator)

---

## What Is This?

This is the complete blueprint for **Flyin' Colors**, a groundbreaking Trance music project that transforms trauma into defiant art. Born from the October 7th, 2023 attacks on Israel, this music fuses Goa Trance, Nitzhonot, Nu-Metal, Psycore, and Modern Classical at the molecular level.

This architecture enables:
- **AI-assisted music production** via specialized agent teams
- **Automated Ableton Live control** via MCP server + AbletonOSC
- **Professional workflow** adapted from software development best practices
- **Semi-automated process** where Claude executes, Avi decides

---

## The Vision

**Emotional Arc:** Horror → Defiance → Triumph
**Musical DNA:** 145+ BPM, Goa/Nitzhonot scales, 6-12 minute tracks
**Narrative:** Each track tells a specific story within the trauma-to-triumph arc
**Message:** We deserve PLUR. We will never stop dancing.

---

## Architecture Components

### 1. Agent Framework (`/agents/`)

**11 specialized production agents** organized in 6 tiers:

| Tier | Agents | Function |
|------|--------|----------|
| **Shadow Creator** | Orchestrator | Main coordinator, artistic vision keeper |
| **Tier 0** | System Architect | Infrastructure (MCP server, OSC, Push 3) |
| **Tier 1** | Narrative Architect, Music Theory Architect | Concept & musical foundation |
| **Tier 2** | Sound Designer, Arrangement Architect | Design (parallel) |
| **Tier 3** | MIDI Producer, Automation Engineer | Production (parallel) |
| **Tier 4** | Mix Engineer, Mastering Engineer | Quality (sequential) |
| **Tier 5** | Export Manager | Delivery |
| **Tier 6** | Technical Writer | Documentation (async) |

**Key files:**
- `00-shadow-creator.md` — Main orchestrator
- `01-shared-context.md` — Shared by all agents
- `03-13-*.md` — Individual agent prompts
- `README.md` (agents folder) — Architecture overview

### 2. Project Brief (`/templates/`)

**FLYIN_COLORS_PROJECT_BRIEF.md** — Single source of truth
- Complete vision and narrative
- Musical parameters (BPM, scales, length)
- Reference artists and influence breakdown
- Tech stack (hardware, plugins)
- Current workflow patterns
- Timeline and approach

**Paste this at the start of every agent conversation.**

### 3. Technical Infrastructure (`/technical/`)

**ABLETON_MCP_SETUP.md** — 30-minute setup using ahujasid/ableton-mcp
- Install UV package manager
- Install remote script to Ableton
- Configure Claude Desktop
- Test track/MIDI creation automation

**MCP_SERVER_IMPLEMENTATION_PLAN_OLD.md** — Archived custom build plan (use ahujasid/ableton-mcp instead)

**SINGLE_MACHINE_ARCHITECTURE.md** — Current setup
- Windows PC running everything locally
- Data flow diagrams
- Migration path to dual-machine

**PUSH_3_INTEGRATION.md** — Hardware workflow
- Standalone mode for sketching
- Hands-on MIDI recording
- Parameter automation
- Scene launching

### 4. Knowledge Base (`/docs/`)

**MUSIC_THEORY_KNOWLEDGE_BASE.md** — Musical DNA reference
- Scales & modes (Goa, Nitzhonot)
- Chord progressions (uplifting, dark, euphoric)
- Bassline patterns (rolling, acid, pulsing)
- Melodic structures (arps, leads)
- Arrangement templates
- Reference artist analysis

---

## How to Use This Architecture

### Option A: Claude Projects (claude.ai)

**Setup:**
1. Create 11 Claude Projects (one per agent + Shadow Creator)
2. For each project, add custom instructions:
   - `01-shared-context.md` (all agents)
   - `FLYIN_COLORS_PROJECT_BRIEF.md` (all agents)
   - Agent-specific file (e.g., `06-sound-designer.md`)

**Workflow:**
1. Start with Shadow Creator
2. Shadow Creator activates appropriate agents
3. Agents produce handoff briefs
4. Shadow Creator coordinates next tier

### Option B: Claude Desktop with MCP (Automation - 30 min setup)

**Setup:**
1. Install ahujasid/ableton-mcp (follow `technical/ABLETON_MCP_SETUP.md`)
2. Configure Claude Desktop with MCP server
3. Use Shadow Creator (Claude Projects) for guidance

**Workflow:**
1. Shadow Creator provides creative direction (Claude Projects web)
2. Claude Desktop executes via MCP server (track/MIDI/instrument creation)
3. Avi maintains creative control at decision points

### Option C: Hybrid (Recommended)

**Infrastructure:** Claude Code (System Architect builds MCP)
**Creative:** Claude Projects (Shadow Creator + production agents)
**Execution:** MCP server automates technical work
**Control:** Avi approves creative decisions, tweaks on Push 3

---

## Quick Start

### Immediate (No Infrastructure)

1. Open claude.ai
2. Create a Shadow Creator project
3. Add `01-shared-context.md` + `FLYIN_COLORS_PROJECT_BRIEF.md` as custom instructions
4. Add `00-shadow-creator.md` as custom instructions
5. Start conversation: "I want to create a track about [concept]"
6. Shadow Creator guides you through the process

### Full Setup (With MCP Automation)

1. **Phase 1:** Set up infrastructure (30 min)
   - Follow `technical/ABLETON_MCP_SETUP.md`
   - Install UV → configure Claude Desktop
   - Test basic Ableton control

2. **Phase 2:** Create first track
   - Shadow Creator coordinates agents (Claude Projects)
   - Claude Desktop + MCP handles track/MIDI creation
   - You approve creative decisions and tweak on Push 3

3. **Phase 3:** Iterate and refine
   - Learn what works, improve workflow
   - Update agents as needed
   - Build pattern library

---

## File Organization

```
flyin-colors-architecture/
├── README.md (this file)
│
├── agents/
│   ├── README.md (architecture overview)
│   ├── 00-shadow-creator.md
│   ├── 01-shared-context.md
│   └── 03-13-*.md (specialized agents)
│
├── templates/
│   └── FLYIN_COLORS_PROJECT_BRIEF.md
│
├── technical/
│   ├── ABLETON_MCP_SETUP.md (30 min setup)
│   ├── MCP_SERVER_IMPLEMENTATION_PLAN_OLD.md (archived)
│   ├── SINGLE_MACHINE_ARCHITECTURE.md
│   └── PUSH_3_INTEGRATION.md
│
└── docs/
    └── MUSIC_THEORY_KNOWLEDGE_BASE.md
```

---

## Current Status

**Completed:**
- ✅ Full agent architecture designed
- ✅ All 11 agent prompts written
- ✅ Project brief created
- ✅ MCP setup guide (using ahujasid/ableton-mcp)
- ✅ Single-machine architecture documented
- ✅ Push 3 integration workflow designed
- ✅ Music theory knowledge base compiled

**Next Steps:**
1. Create Shadow Creator Claude Project (Phase 1)
2. Optional: Set up ahujasid/ableton-mcp for automation (30 min)
3. Test with a simple track concept
4. Iterate and refine based on real-world use

**Timeline:** Long-term quality build (months, not days)

---

## Tools & Tech Stack

### Hardware
- Ableton Live 12 Suite
- Ableton Push 3
- RME Fireface UCX II
- Dynaudio Core 7 speakers

### Software/Plugins
- FabFilter (full suite)
- iZotope RX 10
- Sylenth1, Serum, Vital, Massive
- Komplete Kontrol, Kontakt
- Polyverse Wider
- Sonic Academy Kick 2
- Splice

### Infrastructure
- Python MCP server
- AbletonOSC
- Claude Code
- JSON state management

---

## The Shadow Creator's Opening Message

When you interact with the Shadow Creator:

> I am your Shadow Creator, ready to guide the creation of Flyin' Colors music.
>
> I understand the vision: transforming the trauma of October 7th into defiant, triumphant Trance. I coordinate your agent team, maintain narrative coherence, and execute technical production via the MCP server.
>
> What would you like to create today?
>
> - **New track** (concept → full production)
> - **Iterate on existing work** (refine a section)
> - **Learn/experiment** (explore a technique)
> - **Build infrastructure** (MCP server, Push 3 integration)
> - **Analyze references** (extract DNA from artist tracks)

---

## Key Principles

1. **This is art born from trauma** — Every technical decision serves the narrative
2. **Semi-automated workflow** — Claude executes, Avi decides
3. **Long-term quality build** — Months, not days. Build it right.
4. **Hybrid approach works best** — Automation handles tedious work, Avi maintains creative vision
5. **Push 3 keeps it musical** — Stay hands-on, away from mouse
6. **Reference artists = DNA, not templates** — Extract principles, don't copy

---

## Support & Next Steps

**Questions?** Start a conversation with the Shadow Creator and ask.

**Ready to build?** Begin with System Architect to set up MCP server Phase 1.

**Want to create immediately?** Use Shadow Creator in direct mode for step-by-step guidance.

---

**This is not just music production. This is defiance through sound. This is a sonic declaration that we will never stop dancing.**

---

**Flyin' Colors — February 2026**
