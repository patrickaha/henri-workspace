# Repoprompt Secure Setup Plan

## Overview

Repoprompt is a tool for converting entire codebases into XML format for LLM consumption. We need to set this up with strict access control so ONLY Patrick (U04C7A4DE) can use it.

## Current Findings

1. **Open-Repoprompt** (Go CLI)
   - GitHub: wildberry-source/open-repoprompt
   - Desktop app that copies folders to XML
   - Can be installed via releases or built from source

2. **MCP Integration**
   - No dedicated MCP server found yet
   - Could create custom MCP wrapper

## Recommended Architecture

### Option 1: CLI Tool with Access Control

```bash
# Install on Patrick's Mac (not the Mini)
brew install go
git clone https://github.com/wildberry-source/open-repoprompt
cd open-repoprompt
go build -o repoprompt ./cmd

# Create wrapper script with access control
cat > /usr/local/bin/repoprompt-secure << 'EOF'
#!/bin/bash
# Only Patrick can run this
if [[ "$USER" != "patrick" ]]; then
    echo "Access denied. This tool is restricted."
    exit 1
fi
exec /path/to/repoprompt "$@"
EOF
chmod +x /usr/local/bin/repoprompt-secure
```

### Option 2: MCP Server Setup

Create a custom MCP server that wraps Repoprompt:

```typescript
// repoprompt-mcp-server.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { exec } from 'child_process';

const server = new Server({
  name: 'repoprompt-server',
  version: '1.0.0',
});

// Tool definition
server.setRequestHandler('tools', async () => ({
  tools: [{
    name: 'repoprompt',
    description: 'Convert codebase to XML for LLM context',
    inputSchema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Directory path' },
        includePatterns: { type: 'array', items: { type: 'string' } },
        excludePatterns: { type: 'array', items: { type: 'string' } }
      },
      required: ['path']
    }
  }]
}));

// Tool execution with access control
server.setRequestHandler('tool/call', async (request) => {
  // CRITICAL: Verify caller identity
  const callerId = request.meta?.userId;
  if (callerId !== 'U04C7A4DE') {
    throw new Error('Access denied. Tool restricted to Patrick only.');
  }

  // Execute repoprompt
  const result = await executeRepoprompt(request.params);
  return { result };
});
```

### Option 3: Network Access via Tailscale

Since I'm on the Mac Mini and Repoprompt would run on your Mac:

1. **Install on your Mac:**
   ```bash
   # Install repoprompt
   go install github.com/wildberry-source/open-repoprompt/cmd@latest
   
   # Create API wrapper
   npm init -y
   npm install express body-parser
   ```

2. **Create secure API:**
   ```javascript
   // repoprompt-api.js
   const express = require('express');
   const { exec } = require('child_process');
   const app = express();
   
   // AUTH MIDDLEWARE - CRITICAL
   app.use((req, res, next) => {
     const token = req.headers.authorization;
     if (token !== process.env.REPOPROMPT_TOKEN) {
       return res.status(403).json({ error: 'Forbidden' });
     }
     next();
   });
   
   app.post('/convert', (req, res) => {
     const { path, options } = req.body;
     // Execute repoprompt
     exec(`repoprompt ${path}`, (error, stdout) => {
       if (error) return res.status(500).json({ error });
       res.json({ xml: stdout });
     });
   });
   
   app.listen(8787, '127.0.0.1');
   ```

3. **Expose via Tailscale:**
   ```bash
   tailscale serve https /repoprompt http://127.0.0.1:8787
   ```

## Clawdbot Integration

### As a Tool (Recommended)

Configure in Henri to only respond to Patrick:

```javascript
// In tool handler
if (message.userId !== 'U04C7A4DE') {
  return "This tool is restricted to Patrick only.";
}

// Call repoprompt API
const response = await fetch('https://patrick-mac.ts.net/repoprompt/convert', {
  method: 'POST',
  headers: {
    'Authorization': process.env.REPOPROMPT_TOKEN,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ path, options })
});
```

### Security Measures

1. **Token Authentication**
   - Long random token in environment
   - Never in config files

2. **User ID Verification**
   - Check Slack user ID before execution
   - Log all access attempts

3. **Network Isolation**
   - Only accessible via Tailscale
   - No public exposure

4. **Path Restrictions**
   - Whitelist allowed directories
   - Prevent access to sensitive areas

## Implementation Steps

1. **Choose approach** (CLI, MCP, or API)
2. **Install Repoprompt** on Patrick's Mac
3. **Set up access control**
4. **Configure Henri integration**
5. **Test with non-sensitive directory**
6. **Add to Henri's tool registry**

## Usage Example

```
Patrick: "Use repoprompt on ~/projects/search-swarm"

Henri: [Checks user ID = U04C7A4DE ✓]
       [Calls repoprompt API]
       "Here's the XML representation of search-swarm:
       <prompt>
         <files>
           ...
         </files>
       </prompt>"
```

## Critical Security Note

**NEVER** allow this tool to be:
- Used by anyone except Patrick
- Accessible without authentication
- Able to read directories outside whitelist
- Exposed to public internet

The tool effectively dumps entire codebases - treat it like `cat /*` permissions.