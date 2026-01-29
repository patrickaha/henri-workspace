# GIF Posting Fix (2026-01-28)

## The Problem
- The slack-files skill was using the deprecated `files.upload` API endpoint
- Markdown image syntax `![alt](url)` doesn't work in Slack
- Using `buffer` parameter in message tool wasn't working

## The Solution
Use the `clawdbot message send` command with the `--media` parameter:

```bash
clawdbot message send --target CHANNEL_ID --message "Text" --media "URL_TO_GIF" --channel slack
```

### Via message tool directly:
```json
{
  "action": "send",
  "target": "CHANNEL_ID",
  "message": "Text message",
  "media": "https://media.tenor.com/example.gif"
}
```

## Important Notes
- GIFs must be under 6MB (Slack limit)
- Use `gifgrep` to search for appropriate GIFs
- Always test with smaller file sizes if you get size errors

## Example Workflow
```bash
# Search for GIFs
gifgrep "thumbs up" --max 5 --format url

# Send the GIF
clawdbot message send --target C0ABEJ78E83 --message "Success!" --media "https://media.tenor.com/NTeRUfGwLb4AAAAC/cat-thumbs-up.gif" --channel slack
```