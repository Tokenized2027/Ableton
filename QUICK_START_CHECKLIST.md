# Quick Start Checklist — Flyin' Colors Production Setup

**Goal:** Get from zero to first production session in 4-6 hours
**Strategy:** Minimum viable setup first, expand later

---

## Phase 0: Quick Wins (30 minutes)

### Fix Agent Files
- [ ] **Fix `-e` artifacts** (15 min)
  - Open each agent file in `flyin-colors-architecture/agents/`
  - Search for `-e` characters
  - Remove them
  - Save files

### Test Reference Analysis Pipeline
- [ ] **Install Python dependencies** (5 min)
  ```bash
  cd "C:\Users\Avi\Desktop\GoAI"
  pip install -r requirements.txt
  ```

- [ ] **Test librosa script** (10 min)
  - Pick one reference track (WAV or MP3)
  - Run: `python librosa_analysis_pipeline.py "path/to/track.wav" --bpm-hint 148`
  - Verify markdown file is created
  - Check if BPM/key estimates look reasonable

### Add Quick Reference Tables
- [ ] **MIDI note table** (Already exists in MUSIC_THEORY_KNOWLEDGE_BASE.md - verify it's there)
- [ ] **Frequency range chart** (Add to knowledge base if missing)

**Status Check:** If these work, proceed to Phase 1. If errors, fix before continuing.

---

## Phase 1: Minimum Viable Setup (4-6 hours)

### Option A: Single-Project Quick Start (Recommended for First Track)

**Create ONE Claude Project to test the workflow:**

- [ ] **Create Shadow Creator Project** (30 min)
  1. Go to https://claude.ai/projects
  2. Click "Create Project"
  3. Name: `Shadow Creator - Flyin' Colors [TEST]`
  4. Add custom instructions in order:
     - `flyin-colors-architecture/agents/01-shared-context.md`
     - `flyin-colors-architecture/templates/FLYIN_COLORS_PROJECT_BRIEF.md`
     - `flyin-colors-architecture/agents/00-shadow-creator.md`
  5. Save project

- [ ] **Test Shadow Creator** (15 min)
  - Start conversation: "Hello, Shadow Creator. I'm ready to begin."
  - Verify it responds with opening message
  - Test mode switching: "Switch to narrative mode"
  - Verify it changes behavior

- [ ] **Add Fast-Capture Mode** (30 min)
  - Edit Shadow Creator prompt to include fast-capture mode (see FLYIN_COLORS_ARCHITECTURE_REVIEW_2.md Part 8)
  - Update project custom instructions
  - Test: "Fast capture. I just jammed a dark rolling bass on Push 3."

- [ ] **Analyze First Reference Track** (45 min)
  - Pick: Filteria - "Birds Lingva Franca" (or similar Goa classic)
  - Run librosa pipeline
  - Open generated markdown
  - Fill in [TODO] fields by ear:
    - Section names (intro/buildup/drop/etc)
    - Bassline DNA (pattern type, filter behavior)
    - What makes it special
    - DNA to extract for Flyin' Colors
  - Save to `docs/reference-analysis/`

- [ ] **Create First Memory File** (15 min)
  - Create: `flyin-colors-architecture/memory/preferences.md`
  - Add basic preferences:
    ```markdown
    # Production Preferences

    ## Bass
    - Prefer rolling 16th patterns over pulsing quarter notes
    - Filter cutoff range: 600-1000Hz depending on section energy
    - Always layer: rolling bass + sub bass

    ## Arrangement
    - Longer breakdowns (32-48 bars) for emotional depth
    - Build tension gradually, drop suddenly

    ## Workflow
    - Prefer Push 3 for jamming initial ideas
    - Use fast-capture mode when inspiration hits
    ```

**Status Check:** Can you start a conversation, get musical advice, and capture ideas? If yes, you're ready to produce.

---

## Phase 2: First Production Session (2-4 hours)

### Pick Your Starting Point

**Path A: Concept-First**
- [ ] Open Shadow Creator project
- [ ] Share a concept: "I want to create a track about [specific October 7th moment/feeling]"
- [ ] Work through narrative brief
- [ ] Let Shadow Creator guide you through theory, sound design, arrangement

**Path B: Fast-Capture-First**
- [ ] Jam something on Push 3 / explore a synth
- [ ] Open Shadow Creator project
- [ ] Say: "Fast capture. Here's what I just made: [describe it]"
- [ ] Use fast-capture brief to reverse-engineer the narrative
- [ ] Build outward from the captured idea

### Track Your Session
- [ ] Use CONTINUATION_BRIEF_TEMPLATE.md to document at end of session
- [ ] Note: what worked, what felt clunky, open questions
- [ ] This feedback will guide Phase 3 migration decisions

---

## Phase 3: After First Track (Do Later)

**Only proceed here after you've produced at least one complete track section (intro + buildup + drop) with the single-project setup.**

- [ ] Review: Did the single Shadow Creator project work or was it too cramped?
- [ ] If cramped: Migrate to 4-project setup using CONSOLIDATED_PROJECT_MAP.md
- [ ] If it worked: Keep using Shadow Creator solo, add more reference analyses

- [ ] Set up Ableton MCP (if you want automation)
  - Using existing: https://github.com/ahujasid/ableton-mcp
  - Follow `technical/ABLETON_MCP_SETUP.md`
  - Install UV → Configure Claude Desktop → Test track creation
  - **Time:** 30 minutes setup, not 16-24 hours of building

- [ ] Analyze more reference tracks
  - 2-3 Goa tracks (Pleiadians, Etnica)
  - 2-3 Nitzhonot tracks (Eyal Iceman)
  - 1 Nu-Metal track (for fusion DNA)

- [ ] Build style-fingerprint directory
  - Start with `BASS_IDENTITY.md` (most important)
  - Add others as patterns emerge

---

## Success Criteria

### Phase 0 Success
✅ Python script runs without errors
✅ One reference track analyzed (even if [TODO] fields incomplete)
✅ Agent files are clean (no `-e` artifacts)

### Phase 1 Success
✅ Shadow Creator project responds coherently
✅ Fast-capture mode works (you can describe an idea and get it contextualized)
✅ One complete reference analysis done (all [TODO] fields filled)
✅ You have a preferences file started

### Phase 2 Success
✅ You have Ableton project with at least 32 bars of music
✅ Music follows a narrative concept (not just random patterns)
✅ You used continuation brief to document the session
✅ You want to keep building (not burned out by workflow friction)

---

## Common Pitfalls to Avoid

**Pitfall 1: Trying to build everything before producing**
- Don't analyze 20 reference tracks before making music
- Don't build all 4 projects before testing one
- Don't write complete style-fingerprint before producing a track

**Pitfall 2: Skipping documentation**
- If you don't use continuation briefs, you'll lose context between sessions
- If you don't save fast-captures, you'll forget your best ideas
- If you don't track preferences, Claude will give you different advice every session

**Pitfall 3: Analysis paralysis on agent prompts**
- Don't A/B test prompts before you've used them in real production
- Don't "optimize" agents based on theory — use them first, optimize later
- The current prompts are 85% good — ship and iterate

**Pitfall 4: Ignoring Push 3**
- Don't produce everything with mouse and MIDI editor
- Use Push 3 for initial jamming — it keeps you musical
- Fast-capture exists specifically to bridge Push 3 jams → structured production

---

## Emergency Escape Hatches

### If librosa fails
- Analyze reference tracks manually (just use the template without auto-filled technical fields)
- BPM: Use Ableton's warp detection
- Key: Use your ears or Mixed In Key software

### If Shadow Creator gives generic advice
- Load a reference analysis into the conversation
- Load your preferences file
- Say: "Reference the Filteria analysis — I want THAT bass sound"

### If workflow feels too heavy
- Skip the briefs temporarily
- Just use Shadow Creator as a conversational co-producer
- Return to structured workflow when you need to scale (multiple tracks, collaborators, etc.)

### If you're stuck on a creative decision
- Use PROMPT_AB_TEST_TEMPLATE.md but for creative options, not prompts
- Ask Shadow Creator: "Give me 3 options for this breakdown, score them"
- Pick one, move forward — momentum > perfection

---

## Time Estimates (Realistic)

| Phase | Optimistic | Realistic | If Issues |
|-------|-----------|-----------|-----------|
| Phase 0 | 20 min | 30 min | 1 hour |
| Phase 1 | 3 hours | 4-6 hours | 8 hours |
| Phase 2 | 2 hours | 3-4 hours | 6 hours |

**Total to first music:** 5-10 hours of setup + learning
**Expected by:** End of week 2 if doing this part-time

---

## Next Steps After This Checklist

Once you've completed Phase 2 and have your first track section:

1. Read: INTEGRATION_WORKFLOW.md (how all docs work together)
2. Decide: Single project or migrate to 4 projects?
3. Review: FLYIN_COLORS_ARCHITECTURE_REVIEW_2.md for deeper improvements
4. Plan: Use the implementation timeline to schedule next upgrades

**But don't read those until you've made music.** Theory is cheap. Shipping is hard. Make sound first.
