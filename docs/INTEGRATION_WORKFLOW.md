# Integration Workflow — How All GoAI Documents Work Together

**Purpose:** Show how the 8 files + flyin-colors-architecture work as a complete system
**Audience:** Avi (when resuming work after a break or onboarding a collaborator)

---

## Document Map

### Core Architecture (Read Once, Reference Often)
| File | Purpose | When to Use |
|------|---------|-------------|
| `flyin-colors-architecture/agents/README.md` | Complete agent system overview | Starting new track, understanding tier workflow |
| `flyin-colors-architecture/templates/FLYIN_COLORS_PROJECT_BRIEF.md` | Single source of truth for project vision | When agents give generic advice, reconnect to vision |
| `FLYIN_COLORS_ARCHITECTURE_REVIEW_2.md` | 50 improvements, prioritized | Planning improvements, understanding what's missing |

### Planning & Setup (Use Before Production)
| File | Purpose | When to Use |
|------|---------|-------------|
| `QUICK_START_CHECKLIST.md` | Step-by-step setup guide | First time setup, onboarding collaborator |
| `CONSOLIDATED_PROJECT_MAP.md` | How to merge 11 agents → 4 projects | When single-project feels cramped, need specialization |
| `CONTEXT_WINDOW_BUDGET.md` | Token math for each project | When custom instructions feel too long, planning knowledge file strategy |

### Production Templates (Use During Sessions)
| File | Purpose | When to Use |
|------|---------|-------------|
| `CONTINUATION_BRIEF_TEMPLATE.md` | Resume work between sessions | Start of EVERY production session |
| `FAST_CAPTURE_BRIEF_TEMPLATE.md` | Capture spontaneous ideas | When you jam something good on Push 3, when synth exploration yields gold |
| `REJECTION_BRIEF_TEMPLATE.md` | Send feedback upstream when something's wrong | When arrangement doesn't match narrative, when chords fight the bass, when mix reveals theory issues |

### Testing & Refinement (Use When Optimizing)
| File | Purpose | When to Use |
|------|---------|-------------|
| `PROMPT_AB_TEST_TEMPLATE.md` | Systematically test prompt improvements | After 2-3 tracks, when you know what "good" output looks like |

### Tools (Use As Needed)
| File | Purpose | When to Use |
|------|---------|-------------|
| `librosa_analysis_pipeline.py` | Semi-automated reference track analysis | Analyzing reference artists, building pattern library |
| `requirements.txt` | Python dependencies for librosa script | Initial setup, new machine setup |

---

## Workflow Scenarios

### Scenario 1: Starting Your First Track (Concept-First)

```
1. QUICK_START_CHECKLIST.md
   → Complete Phase 0 + Phase 1
   → You now have Shadow Creator project + 1 reference analysis

2. Open Shadow Creator (Claude Project)
   → "I want to create a track about [October 7th moment]"

3. Shadow Creator guides you through:
   → Narrative brief (emotional arc, samples needed)
   → Music theory (key, scale, BPM, progressions)
   → Provides handoff brief for next phase

4. CONTINUATION_BRIEF_TEMPLATE.md
   → At end of session, fill this in
   → Paste at start of next session to resume

5. If something feels wrong during production:
   → Use REJECTION_BRIEF_TEMPLATE.md
   → Example: "The chord progression sounds too happy for a Horror section"
   → Send back to Music Theory Architect mode
```

**Documents used:** Quick Start → Shadow Creator prompts → Continuation Brief → Rejection Brief (if needed)

---

### Scenario 2: Starting from a Jam (Fast-Capture-First)

```
1. You're jamming on Push 3, stumble onto a great bass riff
   → Don't stop to write a narrative brief
   → Keep playing, get it into Ableton

2. Open Shadow Creator project
   → "Fast capture. I just made a rolling bass in Dm, sounds mechanical and dark"

3. FAST_CAPTURE_BRIEF_TEMPLATE.md
   → Shadow Creator helps you fill this in
   → Extracts: pattern DNA, emotional character, narrative fit
   → Suggests: what surrounds this moment, where in a track it lives

4. Decision point:
   → Build outward NOW: Shadow Creator becomes production co-pilot
   → Save for later: Tag it ("mechanical-heartbeat-bass"), return when ready

5. If building outward:
   → Shadow Creator reverse-engineers narrative from your riff
   → Provides partial brief (just the relevant section)
   → Guides you on what comes before/after

6. CONTINUATION_BRIEF_TEMPLATE.md
   → Document at end of session
   → Note: "Started from fast-capture, developed into Drop 1 section"
```

**Documents used:** Fast-Capture Brief → Shadow Creator → Continuation Brief

---

### Scenario 3: Analyzing Reference Artists

```
1. Pick reference track
   → Example: Filteria - "Birds Lingva Franca"

2. Export as WAV (if needed)
   → From Spotify/YouTube → Audacity → Export

3. librosa_analysis_pipeline.py
   → Run: python librosa_analysis_pipeline.py "path/to/track.wav" --bpm-hint 148
   → Outputs: reference-analysis-birds-lingva-franca.md (pre-filled)

4. Complete [TODO] fields manually
   → What makes this track special
   → Bassline DNA (pattern type, velocity, filter behavior)
   → DNA to extract for Flyin' Colors

5. Save to: flyin-colors-architecture/docs/reference-analysis/

6. Use during production
   → When working on similar section, paste relevant DNA into Shadow Creator conversation
   → "Reference Filteria's bass DNA from bars 45-80 — I want that rolling energy"
```

**Documents used:** librosa script → Reference analysis template (auto-generated)

---

### Scenario 4: Migrating to 4-Project Setup

```
1. Decision point:
   → Have you completed 1 full track section with single Shadow Creator project?
   → Is conversation getting too long / hitting context limits?
   → Do you need specialized agents running simultaneously?

2. If YES to above:
   → Read: CONSOLIDATED_PROJECT_MAP.md
   → Read: CONTEXT_WINDOW_BUDGET.md (understand token limits)

3. CONSOLIDATED_PROJECT_MAP.md provides:
   → What goes in each of 4 projects
   → Which agents merge together
   → Mode switching commands
   → Migration checklist (step-by-step)

4. Execute migration:
   → Week 1: Prepare files (trim prompts, add I/O contracts)
   → Week 2: Create 4 Claude Projects
   → Week 3: Test with new track

5. Workflow changes:
   → Shadow Creator → produces handoff brief
   → Copy handoff brief to Production Studio project
   → Production Studio → produces handoff brief
   → Copy to Quality Control project
   → QC produces final output

6. If issues found during QC:
   → Use REJECTION_BRIEF_TEMPLATE.md
   → Copy rejection brief back to Production Studio or Shadow Creator
```

**Documents used:** Consolidated Project Map → Context Window Budget → Continuation Brief (between projects) → Rejection Brief (backward feedback)

---

### Scenario 5: Optimizing Agent Prompts

```
1. When to start:
   → After 2-3 tracks (you know what "good" output looks like)
   → When agents give consistently generic or off-target advice
   → When you want to test architecture review improvements

2. PROMPT_AB_TEST_TEMPLATE.md
   → Pick ONE agent to test (start with MIDI Producer — most concrete)
   → Create test task: "Generate 8-bar rolling bass in Am at 148 BPM"
   → Run with current prompt (version A)
   → Modify prompt (add I/O contract, exact velocity examples, etc.)
   → Run with modified prompt (version B)
   → Score both using rubric
   → Keep what worked, revert what didn't

3. Testing order (from template):
   → MIDI Producer (most testable)
   → Sound Designer
   → Arrangement Architect
   → Automation Engineer
   → Narrative Architect
   → Shadow Creator (most subjective, test last)

4. Document findings:
   → Update agent prompt files with winning versions
   → Add to memory/preferences.md: "MIDI Producer v3 with velocity examples works best"
   → Share insights in style-fingerprint/EVOLUTION_LOG.md
```

**Documents used:** Prompt A/B Test Template → Agent prompts (in flyin-colors-architecture/agents/)

---

## Information Flow Diagrams

### Single-Project Workflow (Phase 1)

```
┌─────────────────────────────────────────┐
│  YOU (Avi)                              │
│  - Concept / Fast-capture / Continuation│
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  SHADOW CREATOR (Claude Project)        │
│  - Acts as all agents in one            │
│  - Narrative → Theory → Design →        │
│    Arrangement → MIDI → Mix             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  ABLETON LIVE (Manual Execution)        │
│  - You execute the instructions         │
│  - Push 3 for hands-on performance      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  CONTINUATION BRIEF (Next Session)      │
│  - Paste into new conversation          │
│  - Maintain context across sessions     │
└─────────────────────────────────────────┘
```

### 4-Project Workflow (Phase 3)

```
┌────────────────┐
│  SHADOW        │  Handoff Brief
│  CREATOR       ├──────────────┐
│                │              │
│ Narrative +    │              ▼
│ Theory         │    ┌────────────────┐
└────────────────┘    │  PRODUCTION    │  Handoff Brief
                      │  STUDIO        ├──────────────┐
        ▲             │                │              │
        │             │ Sound Design + │              ▼
        │             │ Arrangement +  │    ┌────────────────┐
 Rejection Brief      │ MIDI + Auto    │    │  QUALITY       │
  (if issues)         └────────────────┘    │  CONTROL       │
        │                     ▲              │                │
        │                     │              │ Mix + Master + │
        └─────────────────────┘              │ Export         │
                      Rejection Brief        └────────────────┘
                       (if issues)                   │
                                                     ▼
                                              🎵 Final Track
```

### Reference Analysis → Production Pipeline

```
┌────────────────┐
│ REFERENCE      │
│ TRACK          │
│ (WAV/MP3)      │
└───────┬────────┘
        │
        ▼
┌────────────────────────────┐
│ librosa_analysis_pipeline  │ (Auto-fills technical data)
│ .py                        │
└───────┬────────────────────┘
        │
        ▼
┌────────────────────────────┐
│ Markdown template          │ (You fill [TODO] subjective fields)
│ (pre-filled)               │
└───────┬────────────────────┘
        │
        ▼
┌────────────────────────────┐
│ Save to:                   │
│ docs/reference-analysis/   │
│ filteria-birds.md          │
└───────┬────────────────────┘
        │
        ▼
┌────────────────────────────┐
│ Load into Shadow Creator   │ "Use Filteria's bass DNA"
│ when producing similar     │
│ sections                   │
└────────────────────────────┘
```

---

## Document Dependencies

**Must Read First (Foundation):**
1. QUICK_START_CHECKLIST.md
2. flyin-colors-architecture/agents/README.md

**Read When Relevant (Just-In-Time):**
- Starting track: Shadow Creator prompts + Continuation Brief Template
- Jamming: Fast-Capture Brief Template
- Something's wrong: Rejection Brief Template
- Analyzing references: librosa script + reference analysis template
- Feeling cramped: Consolidated Project Map + Context Window Budget
- Optimizing: Prompt A/B Test Template + Architecture Review

**Read When Planning (Strategic):**
- FLYIN_COLORS_ARCHITECTURE_REVIEW_2.md (the 50 improvements)
- CONTEXT_WINDOW_BUDGET.md (token strategy)
- CONSOLIDATED_PROJECT_MAP.md (migration plan)

---

## File Modification Frequency

| File | How Often to Update |
|------|-------------------|
| `CONTINUATION_BRIEF_TEMPLATE.md` | Fill fresh copy every session |
| `FAST_CAPTURE_BRIEF_TEMPLATE.md` | Fill when capturing ideas (1-3x per week) |
| `REJECTION_BRIEF_TEMPLATE.md` | Fill when issues arise (hopefully rare) |
| `memory/preferences.md` | Update after every 2-3 tracks (patterns emerge) |
| `style-fingerprint/*.md` | Build gradually over 5-10 tracks |
| `reference-analysis/*.md` | Add 1-2 per week during learning phase |
| Agent prompts | Update only after A/B testing (quarterly max) |

---

## What to Ignore (For Now)

**Don't use these until you've completed 1 full track:**
- Prompt A/B Test Template
- Consolidated Project Map (if single project works)
- Architecture Review Part 4-7 (music knowledge gaps, technical improvements)

**Don't use these until you've completed 3-5 tracks:**
- MCP Server implementation
- Dual-machine architecture migration
- Memory system from mastering-claude-code v4.4

**Focus instead on:**
- Making music
- Capturing ideas (fast-capture)
- Analyzing 3-5 key reference tracks
- Building your preferences file

---

## Emergency: "I'm Lost, Which Doc Do I Need?"

| Situation | Document | Page/Section |
|-----------|----------|-------------|
| Setting up for first time | QUICK_START_CHECKLIST.md | Phase 0 + 1 |
| Starting a new session | CONTINUATION_BRIEF_TEMPLATE.md | Top section (quick version) |
| Just jammed something great | FAST_CAPTURE_BRIEF_TEMPLATE.md | Entire template |
| Chord progression feels wrong | REJECTION_BRIEF_TEMPLATE.md | "What's Wrong" section |
| Want to analyze Filteria track | librosa_analysis_pipeline.py | Command line usage |
| Conversations getting too long | CONSOLIDATED_PROJECT_MAP.md | Migration checklist |
| Agent giving generic advice | FLYIN_COLORS_ARCHITECTURE_REVIEW_2.md | Part 3 (Agent Optimization) |
| Forgot how the system works | THIS DOCUMENT | Workflow Scenarios |

---

## Version Control Strategy

**Git Workflow:**
```bash
# After setup
git add .
git commit -m "Complete Phase 1 setup - Shadow Creator ready"

# After first track section
git add .
git commit -m "First 32 bars - Drop 1 of [Track Name]"

# After analyzing reference
git add docs/reference-analysis/
git commit -m "Add Filteria Birds analysis"

# After prompt improvements
git add flyin-colors-architecture/agents/
git commit -m "Update MIDI Producer v2 - add velocity examples"
```

**What to commit:**
- ✅ Agent prompts (when modified)
- ✅ Reference analyses (completed ones)
- ✅ Memory/preferences files
- ✅ Style-fingerprint files
- ✅ Template modifications
- ❌ Filled continuation briefs (session-specific, ephemeral)
- ❌ Fast-capture briefs (unless golden ideas worth archiving)
- ❌ Rejection briefs (debugging artifacts, not permanent)

---

## Next Steps

**If you just read this for the first time:**
→ Go to QUICK_START_CHECKLIST.md, start Phase 0

**If you've completed Phase 1 (single project setup):**
→ Make music. Use Continuation Brief every session. Ignore everything else.

**If you've completed 1 track and want to improve:**
→ Read FLYIN_COLORS_ARCHITECTURE_REVIEW_2.md, pick 3-5 improvements from Phase 3

**If workflow feels cramped:**
→ Read CONSOLIDATED_PROJECT_MAP.md, plan migration to 4 projects

**If you're onboarding a collaborator:**
→ Give them: QUICK_START_CHECKLIST.md + this document + FLYIN_COLORS_PROJECT_BRIEF.md

---

**The system is designed to grow with you. Start small, expand as needed. Make music first, optimize later.**
