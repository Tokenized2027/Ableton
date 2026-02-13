# Flyin' Colors Production System

**What this is:** AI-assisted music production architecture for creating trauma-based Trance music responding to the October 7th, 2023 attacks on Israel.

**Goal:** Transform trauma into defiant, triumphant music using semi-automated production workflow with Claude as co-creator.

---

## Project Context

### The Music
- **Genre fusion:** Goa Trance + Nitzhonot + Nu-Metal + Psycore + Modern Classical
- **Narrative arc:** Horror → Defiance → Triumph (track-specific, not formulaic)
- **BPM range:** 145-155 (Nitzhonot standard)
- **Track length:** 6-12 minutes (192 bars @ 148 BPM standard)
- **Key:** Minor keys (Am, Dm, Em, Cm most common)

### The Setup
- **DAW:** Ableton Live 12 Suite
- **Hardware:** Push 3, RME Fireface UCX II, Dynaudio Core 7
- **Plugins:** Serum, Vital, Massive, Sylenth1, FabFilter, iZotope RX 10, Kontakt
- **Environment:** Windows 10/11 via Git Bash (MINGW64)

### The Workflow
**Current (manual):**
1. Shadow Creator (Claude Project) provides creative guidance
2. You execute in Ableton manually
3. Continuation briefs preserve context between sessions

**Future (automated via MCP):**
1. Shadow Creator provides guidance (Claude Projects)
2. Claude Desktop executes via [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp)
3. You maintain creative control at decision points

**Note:** Using existing ableton-mcp (not building custom). See `flyin-colors-architecture/technical/ABLETON_MCP_SETUP.md`

---

## Repository Structure

```
GoAI/
├── CLAUDE.md (this file)               ← Project context for Claude Code
├── README.md                            ← Navigation hub
├── QUICK_START_CHECKLIST.md            ← Start here (Phase 0-4)
├── INTEGRATION_WORKFLOW.md             ← How all docs work together
│
├── Production Templates (use every session)
│   ├── CONTINUATION_BRIEF_TEMPLATE.md  ← Resume between sessions
│   ├── FAST_CAPTURE_BRIEF_TEMPLATE.md  ← Capture jams quickly
│   ├── REJECTION_BRIEF_TEMPLATE.md     ← Feedback when issues arise
│   └── PROMPT_AB_TEST_TEMPLATE.md      ← Test prompt improvements
│
├── Tools
│   ├── librosa_analysis_pipeline.py    ← Reference track analysis
│   └── requirements.txt                 ← Python dependencies
│
└── flyin-colors-architecture/
    ├── agents/                          ← 12 AI agent prompts
    │   ├── 00-shadow-creator.md        ← Main orchestrator (USE THIS FIRST)
    │   ├── 01-shared-context.md        ← Foundation for all agents
    │   └── 02-13-*.md                  ← Specialized agents
    ├── templates/
    │   └── FLYIN_COLORS_PROJECT_BRIEF.md ← Single source of truth
    ├── docs/
    │   ├── MUSIC_THEORY_KNOWLEDGE_BASE.md
    │   ├── BPM_TO_TIME_REFERENCE.md     ← MIDI ticks for automation
    │   ├── FREQUENCY_RANGE_OWNERSHIP.md ← Mix guide
    │   ├── GIT_WORKFLOW.md              ← Branch strategy
    │   └── reference-analysis/          ← Analyzed reference tracks
    └── technical/
        ├── MCP_SERVER_IMPLEMENTATION_PLAN.md
        └── PUSH_3_INTEGRATION.md
```

---

## Critical Files (Always Read These First)

When working in Claude Code, read these to understand context:

1. **This file (CLAUDE.md)** — You're reading it now
2. **flyin-colors-architecture/templates/FLYIN_COLORS_PROJECT_BRIEF.md** — The vision
3. **flyin-colors-architecture/agents/00-shadow-creator.md** — Your primary role model

---

## Common Tasks & How to Help

### Task 1: Analyze a Reference Track
```bash
# Install dependencies if needed
pip install -r requirements.txt

# Run analysis
python librosa_analysis_pipeline.py "path/to/track.wav" --bpm-hint 148 --artist "Filteria" --track-name "Birds Lingva Franca"

# Fill in [TODO] fields manually
# Save to docs/reference-analysis/
```

**Your role:** Run the script, help fill in subjective analysis fields (what makes it special, DNA to extract)

### Task 2: Set Up Ableton MCP
```bash
# Read the setup guide
cat flyin-colors-architecture/technical/ABLETON_MCP_SETUP.md

# Using existing: https://github.com/ahujasid/ableton-mcp
# Install UV → Configure Claude Desktop → Test connection
```

**Your role:** Help install/configure ableton-mcp, test commands, create example workflows

### Task 3: Improve Agent Prompts
```bash
# Read current prompt
cat flyin-colors-architecture/agents/08-midi-producer.md

# Read I/O contract template
cat flyin-colors-architecture/agents/IO_CONTRACT_TEMPLATE.md

# Apply contract to prompt (add to top of file)
```

**Your role:** Add I/O contracts, test with A/B methodology, measure improvement

### Task 4: Create Continuation Brief
**Your role:** Help fill in CONTINUATION_BRIEF_TEMPLATE.md at end of session with:
- Current state (what's placed in Ableton)
- Last creative decision and rationale
- Open questions for next session
- Musical context (key, BPM, chord progression)

---

## Workflow Philosophy

### Make Music First, Optimize Later
- ✅ Produce 1-2 tracks manually before building MCP server
- ✅ Use Shadow Creator as advisor, execute in Ableton yourself
- ✅ Build knowledge base FROM production experience, not before it

### Semi-Automated, Not Fully Automated
- **Human decides:** Narrative, emotional arc, creative choices
- **AI executes:** MIDI generation, technical parameters, optimization
- **Hybrid at:** Sound design, arrangement (AI suggests, human approves)

### Narrative-Driven Production
- Every musical decision serves the story (Horror → Defiance → Triumph)
- No generic trance formulas
- Reference artist DNA informs, doesn't dictate

---

## Communication Style

**Avi (the human):**
- Non-developer, builds through "vibe coding" with AI
- Direct, action-oriented communication
- Prefers complete files over snippets
- Commands first, then code, then brief explanation

**You (Claude as co-creator):**
- Lead with commands/code, then explain
- Complete files only — never "rest stays the same"
- Ask to see files before modifying (don't assume state)
- Respect the hardware (Ableton, Push 3, plugins listed above)

---

## Critical Rules

1. **COMPLETE FILES ONLY** — Never partial code or "..." placeholders
2. **NEVER ASSUME FILE STATE** — Read files before editing
3. **COMMANDS FIRST** — Terminal commands, then code, then explanation
4. **NARRATIVE-DRIVEN** — Every decision serves the emotional story
5. **SEMI-AUTOMATED** — Human creative control, AI technical execution

---

## Reference Artists (Musical DNA Sources)

**Goa Trance:** Filteria, Pleiadians, Etnica, Hallucinogen, Astral Projection
**Nitzhonot:** Eyal Iceman
**Nu-Metal:** Bring Me The Horizon, My Chemical Romance, System of a Down
**Psycore:** Will O Wisp, SUN Project, Kasatka
**Classical:** Ludovico Einaudi
**Israeli:** Tuna, Ravid Plotnik (Hebrew spoken-word reference)

---

## Current Status & Next Steps

**Architecture:** ✅ Complete and tested
**Agent Prompts:** ⚠️ Need I/O contracts applied
**Shadow Creator Project:** ⬜ Not created yet (Phase 1)
**MCP Server:** ⬜ Not started (optional, after manual production)

**Immediate next steps:**
1. Apply I/O contracts to Shadow Creator prompt
2. Create Shadow Creator Claude Project
3. Start producing first track (manual execution in Ableton)
4. Use continuation briefs to maintain context

---

## Git Workflow

**Branch strategy:**
- `main` — stable architecture, completed tracks
- `track/<name>` — work-in-progress tracks
- `infra/<feature>` — MCP server, infrastructure work

**Commit frequency:** After every meaningful session
**What to commit:** Agent prompts, MIDI exports, documentation, continuation briefs
**What NOT to commit:** Audio files (too large), sample libraries, .env files

See: `flyin-colors-architecture/docs/GIT_WORKFLOW.md` for details

---

## Emergency Context

**If user says "I'm stuck" or "this isn't working":**
1. Read the relevant agent prompt to understand their role
2. Check continuation brief (if exists) to understand current state
3. Reference INTEGRATION_WORKFLOW.md emergency section
4. Provide specific, actionable fix

**If user shares Ableton project path:**
- Don't try to read .als files directly (they're compressed XML)
- Ask user to describe what's in the project
- Use continuation brief as source of truth for state

**If user mentions October 7th context:**
- This is trauma-based art responding to the Nova Festival massacre
- Treat with respect and gravity
- The music is defiance — "we will never stop dancing"

---

## Permission Settings

You're running in Claude Code with the following assumed permissions:
- ✅ Read all files in this repo
- ✅ Write/edit files in this repo
- ✅ Run Python scripts (librosa, MCP server development)
- ✅ Run git commands (add, commit, status, diff)
- ✅ Run bash commands (mkdir, cp, cat, find, grep)
- ✅ Install Python packages via pip

**If a command fails due to permissions:** Ask user to adjust settings.

---

## Success Metrics

**Phase 0-1 success:** Shadow Creator project created, tested, usable
**Phase 2 success:** First 32 bars of music produced
**Phase 3 success:** 2-3 reference tracks analyzed, style patterns documented
**Long-term success:** Complete tracks that transform trauma into triumph

---

**Remember:** This is art born from collective trauma. Every decision serves the narrative. Make music that matters.
