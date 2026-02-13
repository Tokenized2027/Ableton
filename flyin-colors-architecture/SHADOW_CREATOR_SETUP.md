# Shadow Creator Setup Guide

**Goal:** Get the Shadow Creator operational in Claude Projects
**Time:** 5 minutes
**Result:** Your personal Flyin' Colors co-creator ready to work

---

## Option A: Claude Projects (claude.ai) — Recommended for Now

### Step 1: Go to claude.ai

Navigate to: https://claude.ai/projects

### Step 2: Create New Project

Click **"Create Project"**
- **Name:** `Shadow Creator - Flyin' Colors`
- **Description:** `Main orchestrator for Flyin' Colors music production`

### Step 3: Add Custom Instructions

In the Project Settings → Custom Instructions:

**Click "Add content"** and paste these 3 files **in order**:

#### File 1: Shared Context
**Location:** `C:\Users\Avi\Desktop\GoAI\flyin-colors-architecture\agents\01-shared-context.md`

Copy and paste the **entire contents** of this file.

---

#### File 2: Project Brief
**Location:** `C:\Users\Avi\Desktop\GoAI\flyin-colors-architecture\templates\FLYIN_COLORS_PROJECT_BRIEF.md`

Copy and paste the **entire contents** of this file.

---

#### File 3: Shadow Creator Identity
**Location:** `C:\Users\Avi\Desktop\GoAI\flyin-colors-architecture\agents\00-shadow-creator.md`

Copy and paste the **entire contents** of this file.

---

### Step 4: Save Project

Click **"Save"** or **"Create Project"**

### Step 5: Start Your First Conversation

In the new Shadow Creator chat, send this:

```
Hello, Shadow Creator. I'm ready to begin. Please introduce yourself and let me know what we can create together.
```

The Shadow Creator should respond with its opening message and ask what you'd like to work on.

---

## Option B: Quick Test (Single Conversation)

If you want to test before creating a full project:

1. Start a new conversation on claude.ai
2. Paste the contents of `SHADOW_CREATOR_CONSOLIDATED.md` (see below)
3. Start creating

---

## Option C: Claude Code (Local) — For Infrastructure Work Later

**When building MCP server:**

1. In your project directory, create `.mcp.json`:
```json
{
  "mcpServers": {
    "flyin-colors-trance": {
      "command": "python",
      "args": ["C:\\trance-mcp\\server.py"]
    }
  }
}
```

2. Start Claude Code in the project directory
3. Claude Code will have access to MCP tools for Ableton automation

---

## What You Can Do Immediately

### 1. Create a Track Concept
```
"I want to create a track about the moment the sirens went off on October 7th"
```

Shadow Creator will:
- Clarify the narrative
- Activate Narrative Architect
- Define emotional arc
- Guide you through the full production process

### 2. Learn a Technique
```
"How do I create a rolling Nitzhonot bassline in Serum?"
```

Shadow Creator will:
- Provide step-by-step Ableton instructions
- Show example MIDI patterns
- Explain sound design choices

### 3. Analyze a Reference Track
```
"Analyze Filteria's 'Birds Lingva Franca' and extract the musical DNA"
```

Shadow Creator will:
- Break down key, scale, BPM, progression
- Identify signature sounds and patterns
- Show how to apply to Flyin' Colors

### 4. Build Infrastructure
```
"Let's set up the MCP server Phase 1"
```

Shadow Creator will:
- Activate System Architect agent
- Guide you through AbletonOSC setup
- Build MCP server step-by-step

---

## Troubleshooting

**Issue:** "The custom instructions are too long"
**Solution:** Use the consolidated version below, or split into 2 projects (Shadow Creator + System Architect)

**Issue:** "Shadow Creator doesn't remember the project context"
**Solution:** Always paste the Project Brief at the start of each NEW conversation within the project

**Issue:** "I want to work on infrastructure, not music"
**Solution:** Create a second project for System Architect (same setup, but use `03-system-architect.md` instead of `00-shadow-creator.md`)

---

## Next Steps After Setup

1. **Test the Shadow Creator** — Ask it to introduce itself
2. **Create your first track concept** — Start with a simple narrative
3. **Iterate and learn** — See what works, refine the workflow
4. **Build infrastructure when ready** — MCP server enables automation

---

## Files You Need Access To

All located in: `C:\Users\Avi\Desktop\GoAI\flyin-colors-architecture\`

**Core 3:**
- `agents/01-shared-context.md`
- `templates/FLYIN_COLORS_PROJECT_BRIEF.md`
- `agents/00-shadow-creator.md`

**Optional (for other agents):**
- `agents/03-system-architect.md` (infrastructure)
- `agents/04-narrative-architect.md` (story/concept)
- `agents/05-music-theory-architect.md` (harmony/scales)
- [etc.]

---

**You're ready. The Shadow Creator awaits.**
