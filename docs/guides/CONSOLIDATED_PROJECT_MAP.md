# Consolidated Project Map — Flyin' Colors

**Purpose:** Guide for setting up 4 Claude Projects from the current 11 agent files.

---

## Overview

| # | Project Name | Agents Merged | Primary Use |
|---|-------------|---------------|-------------|
| 1 | **Shadow Creator** | Shadow Creator + Narrative Architect + Music Theory Architect | Concept, creative direction, theory |
| 2 | **Production Studio** | Sound Designer + Arrangement Architect + MIDI Producer + Automation Engineer | Building the track |
| 3 | **Quality Control** | Mix Engineer + Mastering Engineer + Export Manager | Polish and delivery |
| 4 | **System Architect** | System Architect + Technical Writer | Infrastructure and docs |

---

## Project 1: Shadow Creator

### Custom Instructions Structure

```
═══════════════════════════════════
SECTION 1: SHARED CONTEXT
═══════════════════════════════════
[Contents of 01-shared-context.md]
  → Remove collaborative mode section
  → Add rejection brief template reference
  → Add fast-capture mode reference

═══════════════════════════════════
SECTION 2: PROJECT BRIEF
═══════════════════════════════════
[Contents of FLYIN_COLORS_PROJECT_BRIEF.md]
  → This is where reference artist lists live (moved from Shadow Creator prompt)

═══════════════════════════════════
SECTION 3: SHADOW CREATOR (Default Mode)
═══════════════════════════════════
[Contents of 00-shadow-creator.md — TRIMMED to ≤6,000 chars]
  → Remove: Key Knowledge Areas (moved to knowledge base)
  → Remove: Reference artist lists (moved to project brief)
  → Remove: Workflow examples (duplicate of README)
  → Add: Fast-capture mode section
  → Add: I/O contract at top
  → Keep: Identity, responsibilities, modes, communication style, decision-making

═══════════════════════════════════
SECTION 4: NARRATIVE ARCHITECT MODE
═══════════════════════════════════
When I say "switch to Narrative Architect" or "narrative mode":

[Contents of 04-narrative-architect.md]
  → Add: I/O contract at top
  → Trim any content that duplicates shared context

═══════════════════════════════════
SECTION 5: MUSIC THEORY ARCHITECT MODE
═══════════════════════════════════
When I say "switch to Music Theory Architect" or "theory mode":

[Contents of 05-music-theory-architect.md]
  → Add: I/O contract at top
  → Trim any content that duplicates shared context
```

### Knowledge Files to Attach

| File | Always Loaded | Notes |
|------|--------------|-------|
| `MUSIC_THEORY_KNOWLEDGE_BASE.md` (core) | Yes | Trimmed to core theory only |
| `memory/preferences.md` | Yes | Your production preferences |
| `memory/creative-decisions.json` | Yes | Last 10 sessions of decisions |
| `memory/session-history.json` | Yes | Last 10 session summaries |
| Style-fingerprint files | **No — on demand** | Load specific ones per conversation |
| Reference analyses | **No — on demand** | Load specific ones when discussing references |
| Deep Nitzhonot/Goa theory | **No — on demand** | Load when working on those styles |

### Mode Switching Commands

| Command | Activates |
|---------|-----------|
| "shadow creator mode" / (default) | Shadow Creator |
| "narrative mode" / "switch to narrative architect" | Narrative Architect |
| "theory mode" / "switch to music theory architect" | Music Theory Architect |
| "fast capture" / "I just made something" | Fast-Capture Mode |

### Mode Switching Behavior

**Persistence:** Mode switches persist for the entire conversation until explicitly changed.

**Returning to default:** Say "default mode" or "back to Shadow Creator" to return.

**Current mode indication:** After switching, I'll confirm the new mode in my first response (e.g., "Switching to Narrative Architect mode. Ready to define the emotional arc and story for your track.")

**Example:**
```
You: "switch to narrative mode"
Me: "Switching to Narrative Architect mode. I'll help you define the track concept, emotional arc, and samples needed. What's the story you want to tell?"

[You work on narrative for 10 messages]

You: "back to shadow creator"
Me: "Returning to Shadow Creator mode (default). Ready to coordinate the full production workflow. What's next?"
```

### Estimated Token Budget

- System content: ~18k tokens
- Conversation space: ~182k tokens
- Status: ✅ Healthy

---

## Project 2: Production Studio

### Custom Instructions Structure

```
═══════════════════════════════════
SECTION 1: SHARED CONTEXT (Production-focused)
═══════════════════════════════════
[Contents of 01-shared-context.md]
  → Same trimming as Shadow Creator
  → Emphasize handoff protocol + MCP server tools

═══════════════════════════════════
SECTION 2: PROJECT BRIEF (Production sections only)
═══════════════════════════════════
[Trimmed FLYIN_COLORS_PROJECT_BRIEF.md]
  → Keep: Technical setup, MCP server config, production approach
  → Remove: Full narrative/concept sections (that's Shadow Creator's domain)

═══════════════════════════════════
SECTION 3: SOUND DESIGNER (Default Mode)
═══════════════════════════════════
[Contents of 06-sound-designer.md]
  → Add: I/O contract at top
  → Add: Exact Ableton instruction format (not just specs)
  → Add: MCP command equivalents for every recommendation

═══════════════════════════════════
SECTION 4: ARRANGEMENT ARCHITECT MODE
═══════════════════════════════════
When I say "arrangement mode":

[Contents of 07-arrangement-architect.md]
  → Add: I/O contract at top
  → Add: Narrative-driven arrangement variations (non-formulaic examples)

═══════════════════════════════════
SECTION 5: MIDI PRODUCER MODE
═══════════════════════════════════
When I say "MIDI mode" or "midi producer":

[Contents of 08-midi-producer.md]
  → Add: I/O contract at top
  → Add: Musically-intelligent generation requirements

═══════════════════════════════════
SECTION 6: AUTOMATION ENGINEER MODE
═══════════════════════════════════
When I say "automation mode":

[Contents of 09-automation-engineer.md]
  → Add: I/O contract at top
```

### Knowledge Files to Attach

| File | Always Loaded | Notes |
|------|--------------|-------|
| MIDI note reference table | Yes | Quick reference for MIDI generation |
| BPM-to-time conversion table | Yes | Quick reference for timing |
| Frequency range ownership chart | Yes | Quick reference for mixing decisions |
| MCP server tool reference | Yes | Available OSC commands |
| `memory/production-patterns.md` | Yes | Reusable production patterns |
| `memory/preferences.md` | Yes | Production preferences |
| AbletonOSC API reference | **No — on demand** | Load when debugging MCP commands |
| Style-fingerprint files | **No — on demand** | Load relevant ones per session |

### Mode Switching Commands

| Command | Activates |
|---------|-----------|
| "sound design mode" / (default) | Sound Designer |
| "arrangement mode" | Arrangement Architect |
| "midi mode" / "midi producer" | MIDI Producer |
| "automation mode" | Automation Engineer |

### Estimated Token Budget

- System content: ~14k tokens
- Conversation space: ~186k tokens
- Status: ✅ Excellent

---

## Project 3: Quality Control

### Custom Instructions Structure

```
═══════════════════════════════════
SECTION 1: SHARED CONTEXT (QC-focused)
═══════════════════════════════════
[Trimmed 01-shared-context.md]
  → QC-relevant sections only

═══════════════════════════════════
SECTION 2: MIX ENGINEER (Default Mode)
═══════════════════════════════════
[Mix Engineer prompt]
  → Add: I/O contract at top
  → Include: frequency range ownership chart inline

═══════════════════════════════════
SECTION 3: MASTERING ENGINEER MODE
═══════════════════════════════════
When I say "mastering mode":

[Mastering Engineer prompt]
  → Add: I/O contract at top

═══════════════════════════════════
SECTION 4: EXPORT MANAGER MODE
═══════════════════════════════════
When I say "export mode":

[Export Manager prompt]
  → Add: I/O contract at top
```

### Knowledge Files to Attach

| File | Always Loaded | Notes |
|------|--------------|-------|
| Frequency range ownership chart | Yes | Critical for mix decisions |
| `style-fingerprint/MIX_PREFERENCES.md` | Yes | Always relevant for QC |
| `memory/preferences.md` | Yes | Mix/master preferences |

### Mode Switching Commands

| Command | Activates |
|---------|-----------|
| "mix mode" / (default) | Mix Engineer |
| "mastering mode" | Mastering Engineer |
| "export mode" | Export Manager |

### Estimated Token Budget

- System content: ~7k tokens
- Conversation space: ~193k tokens
- Status: ✅ Very lean

---

## Project 4: System Architect

### Custom Instructions Structure

```
═══════════════════════════════════
SECTION 1: SHARED CONTEXT (Tech-focused)
═══════════════════════════════════
[Trimmed 01-shared-context.md]
  → Tech-relevant sections only

═══════════════════════════════════
SECTION 2: SYSTEM ARCHITECT (Default Mode)
═══════════════════════════════════
[System Architect prompt — 03-system-architect.md]

═══════════════════════════════════
SECTION 3: TECHNICAL WRITER MODE
═══════════════════════════════════
When I say "documentation mode" or "tech writer":

[Technical Writer prompt]
  → Add: Trigger mechanism (documentation as mandatory handoff step)
```

### Knowledge Files to Attach

| File | Always Loaded | Notes |
|------|--------------|-------|
| MCP server architecture doc | Yes | Current implementation |
| AbletonOSC API reference | Yes | Full reference lives here |
| Git workflow | Yes | Version control rules |

### Estimated Token Budget

- System content: ~6k tokens
- Conversation space: ~194k tokens
- Status: ✅ Minimal overhead

---

## Migration Checklist

### Step 1: Prepare Files

- [ ] Trim Shadow Creator prompt from ~13k to ≤6k characters
- [ ] Move reference artist lists from Shadow Creator to project brief
- [ ] Move Key Knowledge Areas from Shadow Creator to music theory knowledge base
- [ ] Remove workflow examples from Shadow Creator (duplicate of README)
- [ ] Remove collaborative mode from shared context
- [ ] Add I/O contracts to all agent prompts
- [ ] Add fast-capture mode section to Shadow Creator prompt
- [ ] Fix `-e` artifacts in all agent files
- [ ] Split music theory knowledge base into core (always loaded) and deep (on demand)
- [ ] Create production-only trim of project brief for Production Studio

### Step 2: Create Projects

- [ ] Create "Flyin' Colors — Shadow Creator" project
  - [ ] Paste combined custom instructions (sections 1-5)
  - [ ] Attach knowledge files (always-loaded only)
- [ ] Create "Flyin' Colors — Production Studio" project
  - [ ] Paste combined custom instructions (sections 1-6)
  - [ ] Attach knowledge files
- [ ] Create "Flyin' Colors — Quality Control" project
  - [ ] Paste combined custom instructions (sections 1-4)
  - [ ] Attach knowledge files
- [ ] Create "Flyin' Colors — System Architect" project
  - [ ] Paste combined custom instructions (sections 1-3)
  - [ ] Attach knowledge files

### Step 3: Test Each Project

- [ ] Shadow Creator: Start a new track concept. Test mode switching. Test fast-capture.
- [ ] Production Studio: Continue from Shadow Creator handoff. Test all 4 modes.
- [ ] Quality Control: Test with a near-complete track.
- [ ] System Architect: Test MCP server modification task.

### Step 4: Archive Old Projects

- [ ] Keep old 11 projects for reference (rename with "[ARCHIVED]" prefix)
- [ ] After 2 successful tracks with new system, delete archived projects

---

## Workflow Between Projects

```
┌─────────────────────────┐
│   SHADOW CREATOR        │
│   Concept → Brief       │
│   Fast-capture → Brief  │
└──────────┬──────────────┘
           │ Handoff Brief
           ▼
┌─────────────────────────┐
│   PRODUCTION STUDIO     │◄──── Rejection Brief (if issues found)
│   Sound → Arrange →     │
│   MIDI → Automation     │
└──────────┬──────────────┘
           │ Handoff Brief
           ▼
┌─────────────────────────┐
│   QUALITY CONTROL       │◄──── Rejection Brief (back to Production)
│   Mix → Master → Export │
└──────────┬──────────────┘
           │ Final Output
           ▼
        🎵 Track Complete

┌─────────────────────────┐
│   SYSTEM ARCHITECT      │  ← Used separately for infrastructure work
│   MCP → Docs → Git      │
└─────────────────────────┘
```

Copy-paste the handoff brief from one project's conversation into the next project's new conversation. The continuation brief template ensures no musical context is lost in the transition.
