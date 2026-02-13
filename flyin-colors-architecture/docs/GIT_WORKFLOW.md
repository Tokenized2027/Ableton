# Git Workflow — Flyin' Colors

**Strategy:** Simple branch-per-track workflow with clear commit conventions.

---

## Branch Strategy

### Main Branch
- **Name:** `main` (or `master` if already initialized)
- **Purpose:** Stable, production-ready architecture
- **Contents:** Agent prompts, templates, knowledge base, completed tracks
- **Commits to main:** Architecture updates, completed tracks, documentation improvements

### Track Branches
- **Naming:** `track/<track-name>` (e.g., `track/iron-dome`, `track/war-of-the-worlds`)
- **Purpose:** Work-in-progress track production
- **Lifespan:** Created at track start, merged to main when track is complete
- **Contents:** Ableton project files, MIDI exports, continuation briefs, session notes

### Infrastructure Branches
- **Naming:** `infra/<feature>` (e.g., `infra/mcp-server-phase1`, `infra/push3-integration`)
- **Purpose:** Major infrastructure work (MCP server, system architecture changes)
- **Lifespan:** Created at start of infrastructure phase, merged when tested and working
- **Contents:** Python code, technical docs, setup scripts

### Agent Branches (Rare)
- **Naming:** `agent/<agent-name>-v<version>` (e.g., `agent/midi-producer-v2`)
- **Purpose:** Major agent prompt rewrites (after A/B testing proves improvements)
- **Lifespan:** Short — merge after testing with 1-2 tracks
- **Contents:** Updated agent .md files, A/B test results

---

## Workflow Patterns

### Pattern 1: Starting a New Track

```bash
# Make sure main is up to date
git checkout main
git pull

# Create track branch
git checkout -b track/iron-dome

# Work on track
# ... edit Ableton project, save continuation briefs, etc.

# Commit progress after each session
git add .
git commit -m "Iron Dome: Complete Drop 1 (bars 49-80)

- Added mechanical bass MIDI pattern
- Designed lead sound in Vital
- Programmed chord progression (i-bVI-bVII-i)
- Created filter sweep automation bars 49-56

Status: Drop 1 done, need to write lead melody

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Push to remote (backup)
git push -u origin track/iron-dome
```

### Pattern 2: Completing a Track

```bash
# Make sure track is fully done
# - Ableton project finalized
# - WAV export complete
# - Documentation written (technical writer)

# Merge back to main
git checkout main
git merge track/iron-dome --no-ff  # Use --no-ff to preserve track history

# Tag the release
git tag -a v1.0-iron-dome -m "Flyin' Colors — Iron Dome (Complete)

Track info:
- BPM: 148
- Key: Dm
- Length: 7:48 (192 bars)
- Narrative: Horror (Iron Dome activation) → Defiance → Triumph
- Status: Mixed, mastered, ready for release"

# Push to remote
git push origin main --tags

# Delete track branch (optional — can keep for reference)
git branch -d track/iron-dome
git push origin --delete track/iron-dome
```

### Pattern 3: Infrastructure Work

```bash
# Create infrastructure branch
git checkout -b infra/mcp-server-phase1

# Work on MCP server
# ... write Python code, test with AbletonOSC

# Commit phases
git add .
git commit -m "MCP Phase 1: Add transport control

- Implemented play/stop/record via AbletonOSC
- Added track creation tool
- Created error handling for OSC failures
- Tested with Ableton Live 12 Suite

Status: Phase 1 transport complete, Phase 2 (MIDI) next"

# Merge when working
git checkout main
git merge infra/mcp-server-phase1 --no-ff

# Tag infrastructure milestones
git tag -a infra-mcp-phase1 -m "MCP Server Phase 1 Complete - Transport Control"
git push origin main --tags
```

### Pattern 4: Agent Prompt Improvements

```bash
# After A/B testing proves new prompt is better
git checkout -b agent/midi-producer-v2

# Update agent file
# Edit: flyin-colors-architecture/agents/08-midi-producer.md

git add flyin-colors-architecture/agents/08-midi-producer.md
git commit -m "MIDI Producer v2: Add I/O contracts and velocity examples

A/B test results:
- Version 1 score: 17/25
- Version 2 score: 22/25
- Improvements: More specific MIDI output, exact velocity values

Changes:
- Added I/O contract (input/output specification)
- Added velocity pattern examples (rolling bass, arps)
- Removed vague descriptions, replaced with exact MIDI values

Tested on: Iron Dome track (Drop 1 bass pattern)
Result: Generated usable MIDI in first attempt (no iteration needed)

See: PROMPT_AB_TEST_TEMPLATE.md (test #1)"

# Merge
git checkout main
git merge agent/midi-producer-v2 --no-ff
git push origin main
```

---

## Commit Message Convention

### Format
```
<scope>: <subject>

<body>

<metadata>
```

### Scopes
- **Track name** (e.g., "Iron Dome", "War of the Worlds")
- **Agent name** (e.g., "MIDI Producer", "Shadow Creator")
- **Infrastructure** (e.g., "MCP Server", "Docs")
- **Architecture** (e.g., "Templates", "Knowledge Base")

### Subject Line
- Imperative mood ("Add X", not "Added X" or "Adding X")
- 50 characters max
- Capitalize first word
- No period at end

### Body
- Wrap at 72 characters
- Explain WHAT and WHY (not HOW — code shows how)
- Use bullet points for multiple changes
- Reference related commits/issues if relevant

### Metadata (Optional)
- `Status: <current state>` — Where the work is at
- `Tested on: <context>` — What you tested with
- `See: <reference>` — Links to related docs
- `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>` — Always include for AI-assisted work

### Examples

**Good:**
```
Iron Dome: Complete intro section (bars 1-32)

- Added kick pattern (four-on-floor, 148 BPM)
- Created atmospheric pad (Dm chord, wide stereo)
- Designed mechanical bass sound in Serum (FM technique)
- Programmed filter automation (400Hz → 800Hz sweep)

Narrative: Horror section — mechanical dread, pre-impact tension

Status: Intro complete, starting buildup next session
Tested on: Dynaudio Core 7 monitors, RME Fireface UCX II

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Bad:**
```
updated some stuff
```

**Bad:**
```
Fixed the bass and added a lead and also changed the arrangement because it didn't sound good and then I redid the mix and exported it but then I realized the kick was too loud so I adjusted that and re-exported and also I think the pad needs more reverb but I'll do that later.
```

---

## What to Commit

### Always Commit
- ✅ Agent .md files (when updated)
- ✅ Templates (when updated)
- ✅ Documentation (when updated)
- ✅ Python scripts (when updated)
- ✅ Ableton project files (.als) — track branches only
- ✅ MIDI exports (.mid) — for reference/reuse
- ✅ Completed continuation briefs (track documentation)
- ✅ Reference analyses (completed)
- ✅ Style-fingerprint files (when patterns emerge)

### Never Commit
- ❌ Audio files (.wav, .mp3, .aiff) — too large (use external storage/Dropbox/Google Drive)
- ❌ Sample libraries (Kontakt, Splice downloads) — too large
- ❌ Ableton's temp files (`.als~` backups, cache)
- ❌ Plugin presets from commercial libraries (copyright)
- ❌ `.env` files or API keys
- ❌ In-progress/partial continuation briefs (ephemeral, not reference material)

### Maybe Commit (Context-Dependent)
- 🤔 Small audio files (<5 MB) — vocal samples, SFX, one-shot sounds → OK to commit
- 🤔 Preset files you created (.fxp, .fxb for Serum/Vital) → Commit if reusable
- 🤔 Screenshots of spectrum analyzers, arrangement views → Commit if documenting a technique
- 🤔 Fast-capture briefs → Commit if the idea became a track centerpiece

---

## .gitignore Template

Create `.gitignore` in project root:

```gitignore
# Audio files (too large)
*.wav
*.mp3
*.aiff
*.flac
*.ogg

# Ableton backups
*.als~
Backup/

# Sample libraries
Samples/
**/Kontakt/
**/Splice/

# Plugins (commercial, copyright)
Presets/Factory/
Presets/Commercial/

# System files
.DS_Store
Thumbs.db
desktop.ini

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
.env

# IDE
.vscode/
.idea/

# Temporary files
*.tmp
*.log
```

**Exception:** If you created custom presets or small samples, move them to a separate folder and exclude that folder from .gitignore:

```gitignore
# Allow custom presets
!Presets/Custom/
```

---

## Collaboration Strategy (Future)

If you collaborate with other producers/musicians:

### Option A: Shared Main Branch
- Everyone commits to `main` after their work is complete
- Use track branches for work-in-progress
- Merge via pull requests with review

### Option B: Personal Branches
- Each collaborator has `main-avi`, `main-collaborator-name`
- Merge between personal mains when agreeing on changes
- Track branches off personal mains

### Option C: Fork Workflow
- Collaborators fork the repo
- Submit pull requests for contributions
- You control what merges to canonical main

**Recommendation for Flyin' Colors:** Start with solo workflow (track branches only). If collaborators join, use Option A (shared main, track branches, pull requests).

---

## Git Commands Quick Reference

### Daily Workflow
```bash
# Start work
git checkout main
git pull
git checkout -b track/new-track

# Save progress
git add .
git commit -m "Track: Session summary"
git push -u origin track/new-track

# End of track
git checkout main
git merge track/new-track --no-ff
git tag -a v1.0-track-name -m "Track complete"
git push origin main --tags
```

### Checking Status
```bash
git status                 # What's changed?
git log --oneline          # Recent commits
git log --graph --all      # Visual branch history
git diff                   # What changed since last commit?
```

### Undoing Mistakes
```bash
git restore <file>         # Discard changes to file
git restore --staged <file> # Unstage file
git reset --soft HEAD~1    # Undo last commit (keep changes)
git reset --hard HEAD~1    # Undo last commit (LOSE changes)
```

### Branch Management
```bash
git branch                 # List local branches
git branch -d <branch>     # Delete branch (safe - won't delete if unmerged)
git branch -D <branch>     # Force delete (DANGEROUS)
git checkout <branch>      # Switch to branch
git checkout -b <branch>   # Create and switch
```

---

## Emergency Recovery

### "I committed to the wrong branch"
```bash
# If you haven't pushed yet
git log                    # Find the commit hash
git checkout correct-branch
git cherry-pick <commit-hash>
git checkout wrong-branch
git reset --hard HEAD~1    # Remove from wrong branch
```

### "I need to undo a merge"
```bash
git log                    # Find merge commit hash
git revert -m 1 <merge-commit-hash>
```

### "I deleted a branch I needed"
```bash
git reflog                 # Find lost commit
git checkout -b recovered-branch <commit-hash>
```

---

## Flyin' Colors Standards

**Default workflow:** Track branches, merge to main when complete

**Commit frequency:** After every meaningful session (don't commit mid-thought)

**Tag frequency:** Every completed track, every infrastructure milestone

**Branch cleanup:** Delete track branches after merge (keep main clean)

**Remote backup:** Push to GitHub/GitLab after every session (protect against drive failure)

**Documentation:** Every commit includes Co-Authored-By for AI-assisted work

---

**Git is your safety net. Commit often, branch freely, merge confidently.**
