"""Timeline Monitor - Agent 1: Monitors @steipete's timeline."""

import logging
from .base import BaseAgent
from ..twitter_client import TwitterClient
from ..storage import Storage

logger = logging.getLogger(__name__)

class TimelineMonitor(BaseAgent):
    """
    Continuously monitors Peter's timeline for new tweets.
    Triggers other agents when new content is found.
    """
    
    def __init__(self, config, message_queue):
        super().__init__(config, message_queue, "Timeline Monitor")
        self.client = TwitterClient(config)
        self.storage = Storage(config)
        self.target_user_id = None
        
    def run_cycle(self):
        """Check for new tweets from Peter."""
        # Get user ID if not cached
        if not self.target_user_id:
            self.target_user_id = self.client.get_user_id(self.config.target_user)
            if not self.target_user_id:
                logger.error(f"Could not find user {self.config.target_user}")
                return
                
            # Save to config for future runs
            self.config.target_user_id = self.target_user_id
            self.config.save()
            
        # Get last tweet ID for incremental fetch
        since_id = self.storage.get_last_tweet_id()
        
        logger.info(f"Checking timeline for @{self.config.target_user} since {since_id}")
        
        # Fetch new tweets (will auto-fallback to search if credits required)
        tweets = self.client.get_user_tweets(
            self.target_user_id,
            max_results=20,
            since_id=since_id,
            exclude_replies=False
        )
        
        if tweets:
            logger.info(f"Found {len(tweets)} new tweets")
            
            # Save to storage
            saved_count = self.storage.save_tweets(tweets)
            logger.info(f"Saved {saved_count} tweets to storage")
            
            # Notify other agents about new tweets
            for tweet in tweets:
                # Notify Reply Harvester if this tweet might have replies
                if tweet.get('metrics', {}).get('replies', 0) > 0:
                    self.send_message(
                        "Reply Harvester",
                        "new_tweet_with_replies",
                        {"tweet_id": tweet['id'], "reply_count": tweet['metrics']['replies']}
                    )
                    
                # Notify Content Analyzer
                self.send_message(
                    "Content Analyzer",
                    "new_tweet",
                    {"tweet_id": tweet['id']}
                )
                
                # Check for conversation threads
                if tweet.get('conversation_id') and tweet['conversation_id'] != tweet['id']:
                    self.send_message(
                        "Reply Harvester",
                        "conversation_detected",
                        {"conversation_id": tweet['conversation_id']}
                    )
                    
            # Broadcast that new tweets are available
            self.broadcast("new_tweets_available", {"count": len(tweets)})
            
        else:
            logger.debug("No new tweets found")
            
        # Sleep until next check
        self.sleep_until_next_cycle(self.config.poll_interval_minutes * 60)