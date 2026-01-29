"""Reply Harvester - Agent 2: Harvests replies and conversations."""

import logging
import queue
from .base import BaseAgent
from ..twitter_client import TwitterClient
from ..storage import Storage

logger = logging.getLogger(__name__)

class ReplyHarvester(BaseAgent):
    """
    Harvests replies to Peter's tweets and full conversation threads.
    Works on demand when notified by Timeline Monitor.
    """
    
    def __init__(self, config, message_queue):
        super().__init__(config, message_queue, "Reply Harvester")
        self.client = TwitterClient(config)
        self.storage = Storage(config)
        self.work_queue = queue.Queue()
        
    def handle_message(self, message):
        """Handle incoming messages from other agents."""
        if message['type'] == 'new_tweet_with_replies':
            self.work_queue.put({
                'action': 'fetch_replies',
                'tweet_id': message['data']['tweet_id']
            })
        elif message['type'] == 'conversation_detected':
            self.work_queue.put({
                'action': 'fetch_conversation',
                'conversation_id': message['data']['conversation_id']
            })
            
    def run_cycle(self):
        """Process reply harvesting tasks."""
        try:
            # Get work item with timeout
            work_item = self.work_queue.get(timeout=30)
            
            if work_item['action'] == 'fetch_replies':
                self._fetch_replies(work_item['tweet_id'])
            elif work_item['action'] == 'fetch_conversation':
                self._fetch_conversation(work_item['conversation_id'])
                
        except queue.Empty:
            # No work to do, that's fine
            logger.debug("No reply harvesting tasks in queue")
            
    def _fetch_replies(self, tweet_id: str):
        """Fetch replies to a specific tweet."""
        logger.info(f"Fetching replies for tweet {tweet_id}")
        
        replies = self.client.get_tweet_replies(tweet_id)
        
        if replies:
            logger.info(f"Found {len(replies)} replies")
            
            # Save replies
            saved_count = self.storage.save_tweets(replies)
            
            # Notify Content Analyzer about replies
            for reply in replies:
                self.send_message(
                    "Content Analyzer",
                    "new_reply",
                    {
                        "tweet_id": reply['id'],
                        "parent_tweet_id": tweet_id,
                        "is_from_peter": reply['author_id'] == self.config.target_user_id
                    }
                )
                
            # Check for high-value conversations
            peter_replies = [r for r in replies if r['author_id'] == self.config.target_user_id]
            if peter_replies:
                self.send_message(
                    "Knowledge Extractor",
                    "peter_conversation",
                    {
                        "original_tweet": tweet_id,
                        "peter_replies": [r['id'] for r in peter_replies]
                    }
                )
                
    def _fetch_conversation(self, conversation_id: str):
        """Fetch full conversation thread."""
        logger.info(f"Fetching conversation {conversation_id}")
        
        thread = self.client.get_conversation_thread(conversation_id)
        
        if thread:
            logger.info(f"Found {len(thread)} tweets in conversation")
            
            # Save all tweets in thread
            saved_count = self.storage.save_tweets(thread)
            
            # Analyze conversation flow
            peter_tweets = [t for t in thread if t['author_id'] == self.config.target_user_id]
            
            if len(peter_tweets) > 2:
                # This is a significant conversation
                self.send_message(
                    "Knowledge Extractor",
                    "significant_conversation",
                    {
                        "conversation_id": conversation_id,
                        "tweet_count": len(thread),
                        "peter_tweet_count": len(peter_tweets)
                    }
                )