#!/bin/bash
# Weekly automation script for agent opportunity analysis

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPORT_DIR="${SCRIPT_DIR}/../exports"
REPORTS_DIR="${SCRIPT_DIR}/../reports"
DATE=$(date +%Y-%m-%d)

# Create directories if needed
mkdir -p "$EXPORT_DIR" "$REPORTS_DIR"

echo "Starting weekly agent hiring analysis for $DATE"

# 1. Export last week's chat history
echo "Exporting chat history..."
python "${SCRIPT_DIR}/export_chat_history.py" \
  --days 7 \
  --output "${EXPORT_DIR}/weekly_export_${DATE}.json"

# 2. Run analysis
echo "Analyzing patterns..."
python "${SCRIPT_DIR}/analyze_patterns.py" \
  "${EXPORT_DIR}/weekly_export_${DATE}.json" \
  --output "${REPORTS_DIR}/weekly_report_${DATE}.md"

# 3. Post to Slack (using clawdbot message tool)
echo "Posting summary to Slack..."
SUMMARY=$(head -20 "${REPORTS_DIR}/weekly_report_${DATE}.md")

# This would use clawdbot's message tool in production
# For now, just echo what would be sent
echo "Would post to #henri_admin:"
echo "$SUMMARY"
echo ""
echo "Full report: ${REPORTS_DIR}/weekly_report_${DATE}.md"

# 4. Archive old exports (keep last 4 weeks)
echo "Archiving old exports..."
find "$EXPORT_DIR" -name "weekly_export_*.json" -mtime +28 -delete

echo "Weekly analysis complete!"