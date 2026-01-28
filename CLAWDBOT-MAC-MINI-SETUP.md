# Clawdbot Mac Mini Setup Guide
*A battle-tested configuration for secure, remote Clawdbot deployment*

## Overview

This guide documents a production-ready Clawdbot setup running on an isolated Mac Mini with secure remote access via Tailscale and Jump Desktop. Hand this document to your Clawdbot and it will configure everything.

## Architecture

```
[Your Main Computer] 
    ↓ (Tailscale VPN)
[Mac Mini - Isolated Network]
    → Clawdbot Gateway
    → Dedicated to AI
    → No direct internet exposure
```

## Initial Setup Checklist

### 1. Mac Mini Preparation

```bash
# Enable remote access
sudo systemsetup -setremotelogin on

# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install essential tools
brew install node pnpm tailscale jump
```

### 2. Tailscale Setup (Secure VPN)

```bash
# Install and start Tailscale
brew install tailscale
sudo tailscaled install-system-daemon

# Login to Tailscale
tailscale up

# Note your Tailscale IP (100.x.x.x)
tailscale ip -4
```

**Security Benefits:**
- Zero-config VPN
- End-to-end encrypted
- No port forwarding needed
- Access control via Tailscale admin

### 3. Jump Desktop Configuration

**On Mac Mini:**
1. Install Jump Desktop Connect from App Store
2. Sign in with your Jump account
3. Enable "Remote Access"
4. Note the access code

**Security Settings in Jump:**
- Enable "Require password"
- Use strong password
- Enable "Lock on disconnect"
- Disable "Public access" (Tailscale only)

### 4. Clawdbot Installation

```bash
# Install globally via npm
npm install -g clawdbot

# Or via Homebrew (macOS)
brew tap clawdbot/tap
brew install clawdbot

# Run initial setup
clawdbot setup
```

## Security Configuration

### File Permissions

```bash
# Secure Clawdbot directories
chmod 700 ~/.clawdbot
chmod 600 ~/.clawdbot/clawdbot.json
chmod 700 ~/.clawdbot/credentials
chmod 700 ~/.clawdbot/agents
find ~/.clawdbot -name "*.json" -exec chmod 600 {} \;
```

### Environment Variables

Create `~/clawd/.env`:

```bash
# DO NOT COMMIT THIS FILE
# Gateway Security
CLAWDBOT_GATEWAY_TOKEN=$(openssl rand -hex 24)

# Add provider tokens as needed
# FIRECRAWL_API_KEY=fc-xxx
# GOOGLE_API_KEY=AIzaxxx
```

Set permissions:
```bash
chmod 600 ~/clawd/.env
```

### Gateway Configuration

**Critical Security Settings:**

```json5
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",  // Only localhost access
    "port": 18789,
    "auth": {
      "mode": "token",
      "token": "${CLAWDBOT_GATEWAY_TOKEN}"  // From .env
    },
    "tailscale": {
      "mode": "off"  // We handle Tailscale separately
    }
  },
  "channels": {
    // Configure your channels with proper access control
    "slack": {
      "dmPolicy": "allowlist",  // Not "open"!
      "dm": {
        "allowFrom": ["YOUR_USER_ID"]
      },
      "groupPolicy": "allowlist"
    }
  },
  "logging": {
    "redactSensitive": "tools",
    "redactPatterns": [
      "xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+",
      "sk-ant-[a-zA-Z0-9-]+",
      "Bearer [a-zA-Z0-9._-]+"
    ]
  }
}
```

### Git Security

Create `~/.gitignore_global`:

```
.env
.env.*
*.json.backup*
*.json.bak*
auth-profiles.json
**/clawdbot.json
credentials/
```

Enable globally:
```bash
git config --global core.excludesfile ~/.gitignore_global
```

## Network Isolation

### Recommended Network Setup

1. **Dedicated Network/VLAN**
   - Isolate Mac Mini on its own network
   - No access to main LAN
   - Internet access only (for API calls)

2. **Firewall Rules**
   ```bash
   # Only allow established connections
   sudo pfctl -e
   # Add rules to /etc/pf.conf
   ```

3. **Access via Tailscale Only**
   - Disable local network sharing
   - Access only through Tailscale VPN
   - Use Tailscale ACLs for additional control

## Remote Access Workflow

### Daily Access Pattern

1. **Connect to Tailscale** (if not using always-on)
   ```bash
   tailscale up
   ```

2. **Jump Desktop Access**
   - Open Jump Desktop
   - Connect to Mac Mini (via Tailscale IP)
   - Full GUI access for troubleshooting

3. **SSH Alternative**
   ```bash
   ssh user@[tailscale-ip]
   ```

## Security Best Practices

### 1. Access Control
- ✅ Use allowlists, not "open" policies
- ✅ DM policy: "allowlist" with specific user IDs
- ✅ Group policy: "allowlist" with specific channels
- ✅ Require mentions in groups

### 2. Token Management
- ✅ Use environment variables where possible
- ✅ For Slack HTTP mode: tokens must be in config (known limitation)
- ✅ Rotate tokens regularly
- ✅ Never commit tokens to git

### 3. File Security
- ✅ 700 permissions on directories
- ✅ 600 permissions on config files
- ✅ Regular cleanup of backup files

### 4. Model Selection
- ✅ Use strong models (Claude Opus 4+)
- ✅ Avoid weaker models for tool-enabled agents
- ✅ Consider sandboxing for untrusted content

## Maintenance

### Regular Security Audits

```bash
# Run weekly
clawdbot security audit --deep
clawdbot security audit --fix

# Check for updates
clawdbot status
```

### Update Process

```bash
# Safe update via gateway
clawdbot gateway call update.run --params '{"reason": "Security updates"}'

# Or manually
brew upgrade clawdbot
# or
npm update -g clawdbot
```

### Log Monitoring

```bash
# Check for suspicious activity
clawdbot logs --tail 100 | grep -i "error\|warn\|denied"
```

## Troubleshooting

### Common Issues

1. **Can't connect via Tailscale**
   - Check: `tailscale status`
   - Ensure: Mac Mini doesn't sleep
   - System Preferences → Energy Saver → Prevent sleep

2. **Gateway won't start**
   - Run: `clawdbot doctor`
   - Check: `~/.clawdbot/clawdbot.json` validity
   - Verify: File permissions (600/700)

3. **Jump Desktop issues**
   - Ensure: Both devices on Tailscale
   - Check: Jump Desktop Connect running
   - Verify: Firewall not blocking

## Quick Setup Script

Save as `setup-clawdbot-secure.sh`:

```bash
#!/bin/bash
set -e

echo "🦞 Setting up secure Clawdbot environment..."

# Create directories
mkdir -p ~/clawd
mkdir -p ~/.clawdbot

# Set permissions
chmod 700 ~/.clawdbot
chmod 700 ~/clawd

# Generate tokens
GATEWAY_TOKEN=$(openssl rand -hex 24)

# Create .env
cat > ~/clawd/.env << EOF
CLAWDBOT_GATEWAY_TOKEN=$GATEWAY_TOKEN
EOF
chmod 600 ~/clawd/.env

# Create minimal config
cat > ~/.clawdbot/clawdbot.json << EOF
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token"
    }
  },
  "agents": {
    "defaults": {
      "workspace": "~/clawd"
    }
  }
}
EOF
chmod 600 ~/.clawdbot/clawdbot.json

# Fix all permissions
find ~/.clawdbot -type d -exec chmod 700 {} \;
find ~/.clawdbot -type f -exec chmod 600 {} \;

echo "✅ Secure environment ready!"
echo "Gateway token: $GATEWAY_TOKEN"
echo "Next: Configure channels and start gateway"
```

## Final Checklist

- [ ] Mac Mini on isolated network
- [ ] Tailscale installed and connected
- [ ] Jump Desktop configured
- [ ] Clawdbot installed
- [ ] File permissions secured (600/700)
- [ ] Gateway auth token set
- [ ] Access controls configured (allowlists)
- [ ] Git ignores configured
- [ ] Security audit run
- [ ] Backups cleaned up

## Philosophy

"An isolated Mac Mini with Tailscale is your secure AI fortress. No public exposure, no port forwarding, just clean VPN access. The main threats are prompt injection and accidental leaks, not infrastructure attacks."

---

*Hand this document to your Clawdbot and say: "Follow this guide to secure our setup like Patrick's"*