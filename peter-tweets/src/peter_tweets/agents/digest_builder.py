"""Digest Builder - Agent 4: Builds daily/weekly digests."""

import logging
import schedule
from datetime import datetime
from .base import BaseAgent
from ..storage import Storage

logger = logging.getLogger(__name__)

class DigestBuilder(BaseAgent):
    """
    Builds periodic digests of Peter's wisdom.
    Runs on schedule: daily at 8 PM, weekly on Sundays.
    """
    
    def __init__(self, config, message_queue):
        super().__init__(config, message_queue, "Digest Builder")
        self.storage = Storage(config)
        self._setup_schedule()
        
    def _setup_schedule(self):
        """Set up digest generation schedule."""
        # Daily digest at 8 PM
        schedule.every().day.at("20:00").do(self._build_daily_digest)
        
        # Weekly digest on Sundays
        schedule.every().sunday.at("18:00").do(self._build_weekly_digest)
        
    def run_cycle(self):
        """Check if any scheduled digests need to run."""
        schedule.run_pending()
        
        # Sleep for a minute before checking again
        self.sleep_until_next_cycle(60)
        
    def _build_daily_digest(self):
        """Build daily digest."""
        logger.info("Building daily digest")
        digest = self.build_digest("today")
        
        # Save to exports
        export_path = self.config.export_dir / f"daily-{datetime.now():%Y-%m-%d}.md"
        export_path.write_text(digest)
        
        # Notify
        self.broadcast(
            "digest_ready",
            {
                "type": "daily",
                "path": str(export_path),
                "preview": digest[:500]
            }
        )
        
    def _build_weekly_digest(self):
        """Build weekly digest."""
        logger.info("Building weekly digest")
        digest = self.build_digest("week")
        
        # Save to exports
        export_path = self.config.export_dir / f"weekly-{datetime.now():%Y-%m-%d}.md"
        export_path.write_text(digest)
        
        # Notify
        self.broadcast(
            "digest_ready",
            {
                "type": "weekly",
                "path": str(export_path)
            }
        )
        
    def build_digest(self, period: str) -> str:
        """Build a digest for the specified period."""
        tweets = self.storage.get_tweets_by_period(period)
        
        if not tweets:
            return f"# Peter's Wisdom - {period.title()}\n\nNo tweets found for this period."
            
        # Separate into categories
        high_wisdom = [t for t in tweets if t.get('wisdom_score', 0) >= self.config.wisdom_threshold]
        with_code = [t for t in tweets if t.get('has_code')]
        
        # Build markdown
        lines = [
            f"# 🧠 Peter's Wisdom - {period.title()}",
            f"*Generated: {datetime.now():%Y-%m-%d %H:%M}*",
            "",
            f"**Total tweets:** {len(tweets)}",
            f"**High wisdom:** {len(high_wisdom)}",
            f"**With code:** {len(with_code)}",
            "",
        ]
        
        # Top wisdom section
        if high_wisdom:
            lines.extend([
                "## 🔥 Top Wisdom",
                ""
            ])
            
            for tweet in high_wisdom[:10]:
                score = tweet.get('wisdom_score', 0)
                lines.extend([
                    f"### {'🔥' * (score - 6)} Score: {score}/10",
                    f"*{tweet['created_at']}*",
                    "",
                    tweet['text'],
                    ""
                ])
                
                if tweet.get('tools_mentioned'):
                    tools = eval(tweet['tools_mentioned']) if isinstance(tweet['tools_mentioned'], str) else tweet['tools_mentioned']
                    lines.append(f"**Tools:** {', '.join(tools)}")
                    lines.append("")
                    
        # Code snippets section
        if with_code:
            lines.extend([
                "## 💻 Code & Technical",
                ""
            ])
            
            for tweet in with_code[:5]:
                lines.extend([
                    f"### {tweet['created_at']}",
                    "",
                    tweet['text'],
                    ""
                ])
                
        # Tool mentions summary
        all_tools = {}
        for tweet in tweets:
            if tweet.get('tools_mentioned'):
                tools = eval(tweet['tools_mentioned']) if isinstance(tweet['tools_mentioned'], str) else tweet['tools_mentioned']
                for tool in tools:
                    all_tools[tool] = all_tools.get(tool, 0) + 1
                    
        if all_tools:
            lines.extend([
                "## 🛠️ Most Mentioned Tools",
                ""
            ])
            
            sorted_tools = sorted(all_tools.items(), key=lambda x: x[1], reverse=True)
            for tool, count in sorted_tools[:10]:
                lines.append(f"- **{tool}**: {count} mentions")
                
        # Save digest record
        digest_content = "\n".join(lines)
        self.storage.save_digest(period, digest_content, len(tweets))
        
        return digest_content