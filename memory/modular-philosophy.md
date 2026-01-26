# Memory: Modularity Philosophy

## Principle
**Channels = Folders = Modular**

### What This Means
- **Channel** = Namespace for a domain
- **Folder** = Physical storage structure (`05-channels/{channel}/`)
- **Modular** = Self-contained, easy to understand, no cross-contamination

### Benefits
| Aspect | Result |
|--------|--------|
| Clean | Each channel owns its context |
| Scannable | No noise from other domains |
| Portable | Channel folder can be copied/moved |
| Scalable | 50+ hooks/canvas/docs stays organized |

### Pattern Examples
- Hooks → Channel Hooks canvas
- Canvases → Channel canvas storage
- Context → Channel CONTEXT.md
- Hook docs → 06-hooks/ channel-specific files

### The Mental Model
> Everything related to X lives with X. Don't scatter. Don't cross-reference unnecessarily. If it belongs to the channel, it lives in the channel's world.

## When in Doubt
Ask: "Does this belong to the channel?" → If yes, put it there. If no, find where it belongs.
