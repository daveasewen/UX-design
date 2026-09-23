| group | items | tape (cl100k) | real (est) | measured anchor |
|---|--:|--:|--:|---|
| system prompt | 9 | 21,698 | 31,531 |  |
| first user turn | 14 | 20,382 | 29,320 |  |
| tool: mcp__widgets__* | 17 | 16,550 | 16,268 |  |
| tool: core Claude Code tools | 20 | 14,972 | 14,720 |  |
| tool: Artifact* | 1 | 11,906 | 11,704 |  |
| tool: mcp__remote-devices__* | 7 | 6,414 | 6,306 |  |
| tool: mcp__claude-code-remote__* | 6 | 5,546 | 5,451 |  |
| tool: mcp__memory__* | 5 | 3,624 | 3,562 |  |
| tool: the rest (skills/onboarding/review UI) | 4 | 2,661 | 2,616 |  |
| tool: mcp__claude_ai__* | 7 | 2,224 | 2,186 |  |
| tool: Projects | 1 | 1,868 | 1,836 |  |
| **prefix: all tools + system prompt** | 77 | 87,463 | 96,180 | **cache_read 96,179** |
| **first user turn** | 14 | 20,382 | 29,320 | **cache_creation + input 30,006** |
| **BOOT** | | **107,845** | **125,500** | **126,185** |
