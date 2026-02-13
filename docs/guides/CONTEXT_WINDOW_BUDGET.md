# Context Window Budget — Flyin' Colors Consolidated Projects

**Date:** February 13, 2026
**Model:** Claude (Opus 4.6 / Sonnet 4.5)
**Estimated context window:** ~200k tokens (Claude Projects)

---

## Why This Matters

Every token spent on system content (custom instructions, knowledge files, project briefs) is a token NOT available for your actual production conversation. Long conversations about arrangement decisions, MIDI generation, sound design tweaks — these eat context fast. If your system content is bloated, you hit the wall mid-session and lose continuity.

**Rule of thumb:** Keep system content under 20% of context window. That means ≤ 40k tokens for system content, leaving 160k+ for conversation.

---

## Token Estimation Method

Rough conversion: 1 token ≈ 4 characters for English text. Markdown formatting adds ~10-15% overhead. Code blocks add ~5% overhead.

For each project below, I estimate based on the current file sizes in the architecture, accounting for the consolidation merges.

---

## Project 1: Shadow Creator

**Role:** Starting tracks, creative decisions, concept work, fast-capture mode

### System Content Breakdown

| Component | Est. Characters | Est. Tokens | Notes |
|-----------|----------------|-------------|-------|
| Shared context (`01-shared-context.md`) | ~8,000 | ~2,200 | After removing collaborative mode |
| Project brief (`FLYIN_COLORS_PROJECT_BRIEF.md`) | ~12,000 | ~3,300 | Includes reference artist lists (moved from Shadow Creator) |
| Shadow Creator prompt (`00-shadow-creator.md`) | ~6,000 | ~1,700 | **After trimming from 13k to 6k** |
| Narrative Architect prompt (`04-narrative-architect.md`) | ~4,000 | ~1,100 | As "mode switch" section |
| Music Theory Architect prompt (`05-music-theory-architect.md`) | ~5,000 | ~1,400 | As "mode switch" section |
| Fast-capture mode addition | ~3,000 | ~850 | New section in Shadow Creator |
| Music theory knowledge base (core) | ~10,000 | ~2,800 | **Core only — deep theory loads on demand** |
| Style fingerprint index | ~3,000 | ~850 | Summary/index, not full files |
| Memory files (preferences + last 10 sessions) | ~8,000 | ~2,200 | Pruned to recent history |
| Rejection brief template | ~1,500 | ~420 | Template only |
| Continuation brief template | ~2,000 | ~560 | Template only |
| Handoff protocol + templates | ~3,000 | ~850 | From shared context |
| **TOTAL** | **~65,500** | **~18,230** | |

### On-Demand Content (loaded per conversation as needed)

| Content | Est. Tokens | When to Load |
|---------|-------------|--------------|
| Deep Nitzhonot theory | ~2,500 | When producing Nitzhonot-influenced sections |
| Deep Goa theory | ~2,500 | When producing Goa-influenced sections |
| Nu-Metal → Trance dictionary | ~2,000 | When working on fusion elements |
| Emotional-to-musical mapping | ~1,500 | When translating narrative to musical parameters |
| Individual reference track analyses | ~1,500 each | When referencing specific tracks |
| Full style-fingerprint files | ~1,000-2,000 each | When making decisions about signature sound |

### Budget Assessment

- **System content:** ~18k tokens ✅ (well under 40k target)
- **Conversation space:** ~182k tokens
- **Verdict:** Healthy. Room to grow as style-fingerprint and memory files expand.
- **Watch out for:** Reference analyses accumulating in system content. Keep them in the on-demand bucket — only load specific ones when discussing specific tracks.

---

## Project 2: Production Studio

**Role:** Sound design, arrangement, MIDI production, automation

### System Content Breakdown

| Component | Est. Characters | Est. Tokens | Notes |
|-----------|----------------|-------------|-------|
| Shared context (`01-shared-context.md`) | ~8,000 | ~2,200 | Same as above |
| Project brief (trimmed) | ~6,000 | ~1,700 | Production-relevant sections only |
| Sound Designer prompt (`06-sound-designer.md`) | ~5,000 | ~1,400 | With I/O contracts added |
| Arrangement Architect prompt (`07-arrangement-architect.md`) | ~5,000 | ~1,400 | With narrative-driven variations |
| MIDI Producer prompt (`08-midi-producer.md`) | ~5,000 | ~1,400 | With musically-intelligent generation |
| Automation Engineer prompt (`09-automation-engineer.md`) | ~4,000 | ~1,100 | With I/O contracts |
| MIDI note reference table | ~1,500 | ~420 | Quick win — always loaded |
| BPM-to-time conversion table | ~1,000 | ~280 | Quick win — always loaded |
| Frequency range ownership chart | ~1,500 | ~420 | Quick win — always loaded |
| MCP server tool reference | ~4,000 | ~1,100 | Available OSC commands + parameters |
| Handoff protocol + templates | ~3,000 | ~850 | From shared context |
| Memory files (production patterns + preferences) | ~5,000 | ~1,400 | Production-specific subset |
| **TOTAL** | **~49,000** | **~13,670** | |

### On-Demand Content

| Content | Est. Tokens | When to Load |
|---------|-------------|--------------|
| Specific style-fingerprint files | ~1,000-2,000 each | Per production phase |
| AbletonOSC API reference | ~3,000 | When writing MCP commands |
| Current track's continuation brief | ~800 | Start of every session |
| Specific reference track DNA | ~1,500 each | When replicating specific techniques |

### Budget Assessment

- **System content:** ~14k tokens ✅ (very lean)
- **Conversation space:** ~186k tokens
- **Verdict:** Excellent. This project handles the most back-and-forth conversation (iterating on MIDI patterns, tweaking sound design parameters), so the extra conversation space is valuable.

---

## Project 3: Quality Control

**Role:** Mixing, mastering, export

### System Content Breakdown

| Component | Est. Characters | Est. Tokens | Notes |
|-----------|----------------|-------------|-------|
| Shared context (trimmed) | ~5,000 | ~1,400 | QC-relevant sections only |
| Project brief (trimmed) | ~4,000 | ~1,100 | QC-relevant sections only |
| Mix Engineer prompt | ~5,000 | ~1,400 | With I/O contracts |
| Mastering Engineer prompt | ~4,000 | ~1,100 | With I/O contracts |
| Export Manager prompt | ~3,000 | ~850 | With I/O contracts |
| Frequency range ownership chart | ~1,500 | ~420 | Critical for mix decisions |
| Mix preferences from style-fingerprint | ~3,000 | ~850 | Always loaded for QC |
| **TOTAL** | **~25,500** | **~7,120** | |

### Budget Assessment

- **System content:** ~7k tokens ✅ (very lean)
- **Conversation space:** ~193k tokens
- **Verdict:** Lots of room. QC conversations tend to be shorter and more technical anyway.

---

## Project 4: System Architect

**Role:** Infrastructure, MCP server, documentation

### System Content Breakdown

| Component | Est. Characters | Est. Tokens | Notes |
|-----------|----------------|-------------|-------|
| Shared context (trimmed) | ~4,000 | ~1,100 | Tech-relevant sections only |
| System Architect prompt | ~4,000 | ~1,100 | |
| Technical Writer prompt | ~3,000 | ~850 | |
| MCP server architecture doc | ~5,000 | ~1,400 | Current implementation state |
| AbletonOSC API reference | ~5,000 | ~1,400 | Full reference here |
| Git workflow | ~2,000 | ~560 | |
| **TOTAL** | **~23,000** | **~6,410** | |

### Budget Assessment

- **System content:** ~6k tokens ✅
- **Conversation space:** ~194k tokens
- **Verdict:** Minimal overhead. This project is used least frequently.

---

## Growth Projections

As Flyin' Colors evolves, system content will grow. Here's when to watch for budget pressure:

| Milestone | Estimated System Content Growth | Action if Needed |
|-----------|-------------------------------|-----------------|
| 5 reference tracks analyzed | +7.5k tokens if all loaded | Keep in on-demand bucket |
| 3 own-tracks analyzed | +4.5k tokens if all loaded | Keep in on-demand bucket |
| Style-fingerprint fully populated | +8k tokens | Load relevant files per conversation, not all |
| 20 sessions of memory | +4k tokens | Prune to last 10 sessions |
| Nu-Metal + Goa + Nitzhonot deep theory | +7.5k tokens | Always on-demand, never in system content |

**Ceiling estimate:** If everything grows to maximum, the Shadow Creator project (heaviest) might reach ~30k tokens of system content. Still under the 40k target, but monitor it.

---

## How to Verify Actual Token Usage

### Method 1: Claude API Token Counter (Most Accurate)

If you have API access, use the official token counter:

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Paste your full custom instructions as a string
system_content = """
[All your custom instructions combined]
"""

# Count tokens
message = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    system=system_content,
    messages=[{"role": "user", "content": "test"}]
)

print(f"System content tokens: {message.input_tokens}")
print(f"Estimated at 4 chars/token: {len(system_content) / 4}")
print(f"Difference: {abs(message.input_tokens - len(system_content) / 4)}")
```

**Run this for each project after setup.**

### Method 2: Claude Projects Dashboard (Approximate)

Claude Projects may show token usage in the UI (check settings or conversation info). This is less precise but easier.

### Method 3: Estimation Formula (Quick Check)

Use this for quick checks between verification runs:

```python
def estimate_tokens(file_path):
    """Estimate tokens for a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Base estimate: 1 token ≈ 4 characters
    base_estimate = len(content) / 4

    # Markdown adds ~10-15% overhead
    markdown_overhead = base_estimate * 0.125

    # Code blocks add ~5% overhead
    code_blocks = content.count('```')
    code_overhead = (code_blocks / 2) * 50  # ~50 tokens per code block

    total_estimate = base_estimate + markdown_overhead + code_overhead

    return round(total_estimate)

# Example usage
total = 0
total += estimate_tokens('agents/01-shared-context.md')
total += estimate_tokens('templates/FLYIN_COLORS_PROJECT_BRIEF.md')
total += estimate_tokens('agents/00-shadow-creator.md')
# ... add all files in custom instructions

print(f"Estimated system content: {total} tokens")
```

### Verification Schedule

| Milestone | When to Verify | What to Check |
|-----------|----------------|---------------|
| Initial setup | After creating each project | Total system content < 40k target |
| After 10 sessions | Weekly for first month | Are conversations hitting context limits? |
| After first track | Post-production review | Did you reference files not in system content? (Add them if frequently used) |
| Quarterly | Every 3 months | Audit and trim — remove unused knowledge, prune memory to last 10 sessions |
| After major changes | When adding new agent modes, knowledge files | Re-verify total doesn't exceed budget |

### Red Flags (You're Over Budget)

**Symptoms of context window bloat:**
1. Conversations feel "forgetful" after 20-30 exchanges
2. Claude starts ignoring earlier instructions as conversation progresses
3. You notice responses getting less specific/more generic over time in a session
4. System lags or errors when loading project

**What to do:**
1. Run Method 1 or 3 to get actual token count
2. If >40k system tokens:
   - Move largest knowledge files to on-demand (user pastes when needed)
   - Split agent prompts further (combine fewer agents per project)
   - Trim memory files to last 5 sessions instead of 10
3. If still >50k:
   - Consider creating 5-6 projects instead of 4 (more specialization)
   - Use CONSOLIDATED_PROJECT_MAP.md to re-plan splits

### Token Tracking Spreadsheet (Optional)

Track growth over time:

| Date | Project | System Tokens | Conversation Avg Tokens | Context Headroom | Notes |
|------|---------|---------------|-------------------------|------------------|-------|
| 2026-02-13 | Shadow Creator | 18,230 (est) | N/A (new) | 181,770 | Initial setup |
| 2026-03-01 | Shadow Creator | 22,400 (verified) | 15,000 avg | 162,600 | After 10 sessions |
| 2026-04-01 | Shadow Creator | 19,800 (verified) | 18,000 avg | 162,200 | Pruned memory files |

**Tool recommendation:** Simple Google Sheet or Notion table

---

## Key Rules

1. **System content = always loaded.** Only put things here that EVERY conversation needs.
2. **On-demand = user pastes or references.** Load specific files when the conversation needs them.
3. **Memory files get pruned.** Last 10 sessions max. Archive older sessions to a separate file.
4. **Reference analyses never go in system content.** Keep a 1-line index; load full analysis per conversation.
5. **Style-fingerprint files load selectively.** Working on bass? Load `BASS_IDENTITY.md`. Working on arrangement? Load `ARRANGEMENT_PATTERNS.md`. Never load all five at once.
6. **Measure quarterly.** Every 3 months, audit actual system content size and trim if needed.
7. **Verify with real data.** Estimations are useful for planning, but verify with actual token counts (Method 1 or 2) after setup and quarterly.
