"""Twitter API client with self-healing and rate limit handling."""

import tweepy
import backoff
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class TwitterClient:
    """Self-healing Twitter client following Peter's patterns."""
    
    def __init__(self, config):
        self.config = config
        self.client = None
        self.user_cache = {}
        self.rate_limit_reset = {}
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize Twitter client with appropriate auth method."""
        if self.config.twitter_bearer_token:
            # Bearer token auth (app-only)
            self.client = tweepy.Client(
                bearer_token=self.config.twitter_bearer_token,
                wait_on_rate_limit=True
            )
        elif self.config.twitter_api_key and self.config.twitter_api_secret:
            # OAuth 2.0 auth
            self.client = tweepy.Client(
                consumer_key=self.config.twitter_api_key,
                consumer_secret=self.config.twitter_api_secret,
                wait_on_rate_limit=True
            )
        else:
            raise ValueError("No Twitter credentials provided")
            
    @backoff.on_exception(
        backoff.expo,
        (tweepy.TooManyRequests, tweepy.TwitterServerError),
        max_tries=3
    )
    def get_user_id(self, username: str) -> Optional[str]:
        """Get user ID from username with caching."""
        if username in self.user_cache:
            return self.user_cache[username]
            
        try:
            user = self.client.get_user(username=username)
            if user.data:
                user_id = user.data.id
                self.user_cache[username] = user_id
                return user_id
        except Exception as e:
            logger.error(f"Failed to get user ID for {username}: {e}")
            return None
            
    @backoff.on_exception(
        backoff.expo,
        tweepy.TooManyRequests,
        max_tries=5
    )
    def get_user_tweets(
        self, 
        user_id: str, 
        max_results: int = 20,
        since_id: Optional[str] = None,
        exclude_replies: bool = False
    ) -> List[Dict[str, Any]]:
        """Get tweets from user with self-healing."""
        tweet_fields = [
            'id', 'text', 'created_at', 'author_id', 
            'conversation_id', 'referenced_tweets', 'entities',
            'public_metrics'
        ]
        
        try:
            # First try the user timeline endpoint (requires credits)
            tweets = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                since_id=since_id,
                exclude=['retweets'] if not exclude_replies else ['retweets', 'replies'],
                tweet_fields=tweet_fields
            )
            
            if not tweets.data:
                return []
                
            return [self._tweet_to_dict(tweet) for tweet in tweets.data]
            
        except Exception as e:
            if "402" in str(e) or "credits" in str(e).lower():
                # Fall back to search API which works without credits!
                logger.warning("User timeline requires credits, using search API")
                return self.search_user_tweets(self.config.target_user, max_results, exclude_replies)
            elif isinstance(e, tweepy.TooManyRequests):
                # Extract rate limit info
                reset_time = e.response.headers.get('x-rate-limit-reset', 0)
                logger.warning(f"Rate limited. Reset at {reset_time}")
                raise
            else:
                raise
                
    def search_user_tweets(
        self,
        username: str,
        max_results: int = 20,
        exclude_replies: bool = False
    ) -> List[Dict[str, Any]]:
        """Search for user's tweets using search API (works without credits!)."""
        try:
            # Build search query
            query = f"from:{username} -is:retweet"
            if exclude_replies:
                query += " -is:reply"
                
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['id', 'text', 'created_at', 'author_id', 
                             'conversation_id', 'referenced_tweets', 
                             'entities', 'public_metrics']
            )
            
            if not tweets.data:
                return []
                
            return [self._tweet_to_dict(tweet) for tweet in tweets.data]
            
        except Exception as e:
            logger.error(f"Search API failed: {e}")
            return []
            
    def get_tweet_replies(self, tweet_id: str) -> List[Dict[str, Any]]:
        """Get replies to a specific tweet."""
        # Search for replies
        query = f"conversation_id:{tweet_id}"
        
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=100,
                tweet_fields=['id', 'text', 'created_at', 'author_id', 'entities']
            )
            
            if not tweets.data:
                return []
                
            return [self._tweet_to_dict(tweet) for tweet in tweets.data]
            
        except Exception as e:
            logger.error(f"Failed to get replies for {tweet_id}: {e}")
            return []
            
    def get_conversation_thread(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get full conversation thread."""
        query = f"conversation_id:{conversation_id}"
        
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=100,
                tweet_fields=['id', 'text', 'created_at', 'author_id', 'in_reply_to_user_id']
            )
            
            if not tweets.data:
                return []
                
            # Sort by creation time
            sorted_tweets = sorted(tweets.data, key=lambda t: t.created_at)
            return [self._tweet_to_dict(tweet) for tweet in sorted_tweets]
            
        except Exception as e:
            logger.error(f"Failed to get conversation {conversation_id}: {e}")
            return []
            
    def _tweet_to_dict(self, tweet) -> Dict[str, Any]:
        """Convert tweet object to dictionary."""
        result = {
            'id': tweet.id,
            'text': tweet.text,
            'created_at': tweet.created_at.isoformat(),
            'author_id': tweet.author_id,
        }
        
        # Add optional fields
        if hasattr(tweet, 'conversation_id'):
            result['conversation_id'] = tweet.conversation_id
            
        if hasattr(tweet, 'entities') and tweet.entities:
            # Extract mentions
            if 'mentions' in tweet.entities:
                result['mentions'] = [m['username'] for m in tweet.entities['mentions']]
                
            # Extract URLs
            if 'urls' in tweet.entities:
                result['urls'] = [u['expanded_url'] for u in tweet.entities['urls']]
                
            # Extract hashtags
            if 'hashtags' in tweet.entities:
                result['hashtags'] = [h['tag'] for h in tweet.entities['hashtags']]
                
        if hasattr(tweet, 'public_metrics'):
            result['metrics'] = {
                'likes': tweet.public_metrics.get('like_count', 0),
                'retweets': tweet.public_metrics.get('retweet_count', 0),
                'replies': tweet.public_metrics.get('reply_count', 0),
                'quotes': tweet.public_metrics.get('quote_count', 0),
            }
            
        return result
        
    def health_check(self) -> Dict[str, Any]:
        """Check API health and rate limits."""
        try:
            # Try to get rate limit status
            me = self.client.get_me()
            
            return {
                "ok": True,
                "message": "API connection healthy",
                "authenticated_as": me.data.username if me.data else "app"
            }
        except Exception as e:
            return {
                "ok": False,
                "message": str(e)
            }
            
    def estimate_remaining_calls(self) -> int:
        """Estimate remaining API calls before rate limit."""
        # This is a simplified estimation
        # Real implementation would track actual calls
        return self.config.rate_limit_calls