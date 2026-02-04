---
name: SessionEnd
description: Write session summary before ending. USE WHEN user says /fim, /end, goodbye, tchau, ending session, wrap up, OR wants to save what was done.
---

# SessionEnd (/fim)

Write a session summary to MEMORY before ending the conversation.

## What To Do

1. **Reflect** on what was accomplished in this session
2. **Write** a summary file to `~/ai-brain/MEMORY/sessions/`
3. **Confirm** the file path to the user

## File Format

```markdown
---
session_id: {session ID from environment or context}
timestamp: {current local time ISO format}
project: {project name from cwd}
cwd: {current working directory}
source: agent
---

# Session {first 8 chars of session_id}

**Date:** {YYYY-MM-DD} | **Project:** {project name}

## Summary

{2-3 sentence summary of what was accomplished}

## What Was Done

{Bullet list of concrete actions taken}

## Decisions Made

{Technical or design decisions, or "None"}

## Files Modified

{List files created/modified, or "None"}

## Learnings

{Anything notable learned, or "None"}

## Next Steps

{What could be done next, or "None"}

---
*Session summary by Claude (/fim)*
```

## Rules

- **Always** write to `~/ai-brain/MEMORY/sessions/` regardless of current project
- **Filename:** `{YYYY-MM-DD}_{HH-mm-ss}_{first-8-chars-of-session-id}.md`
  - Example: `2026-02-03_15-30-45_45e2aea2.md`
- If you don't have the session_id, use a short random hex string
- Be concise and factual - no filler
- Write in the same language the user used during the session
