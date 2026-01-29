"""Storage layer using SQLite - simple, fast, local."""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Storage:
    """SQLite storage following Peter's patterns - simple and effective."""
    
    def __init__(self, config):
        self.config = config
        self.db_path = config.db_path
        self._init_db()
        
    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tweets (
                    id TEXT PRIMARY KEY,
                    created_at TIMESTAMP,
                    text TEXT,
                    author_id TEXT,
                    conversation_id TEXT,
                    wisdom_score INTEGER DEFAULT 0,
                    has_code BOOLEAN DEFAULT 0,
                    tools_mentioned TEXT,
                    mentions TEXT,
                    urls TEXT,
                    hashtags TEXT,
                    metrics TEXT,
                    processed BOOLEAN DEFAULT 0,
                    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tweet_id TEXT,
                    pattern TEXT,
                    category TEXT,
                    confidence REAL,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (tweet_id) REFERENCES tweets(id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS digests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    period TEXT,
                    content TEXT,
                    tweet_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tweets_created ON tweets(created_at DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tweets_wisdom ON tweets(wisdom_score DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tweets_processed ON tweets(processed)")
            
            conn.commit()
            
    def save_tweet(self, tweet: Dict[str, Any]) -> bool:
        """Save or update a tweet."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO tweets (
                        id, created_at, text, author_id, conversation_id,
                        mentions, urls, hashtags, metrics
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    tweet['id'],
                    tweet['created_at'],
                    tweet['text'],
                    tweet.get('author_id'),
                    tweet.get('conversation_id'),
                    json.dumps(tweet.get('mentions', [])),
                    json.dumps(tweet.get('urls', [])),
                    json.dumps(tweet.get('hashtags', [])),
                    json.dumps(tweet.get('metrics', {}))
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to save tweet {tweet['id']}: {e}")
            return False
            
    def save_tweets(self, tweets: List[Dict[str, Any]]) -> int:
        """Batch save tweets."""
        saved = 0
        for tweet in tweets:
            if self.save_tweet(tweet):
                saved += 1
        return saved
        
    def get_latest_tweets(self, limit: int = 20, wisdom_only: bool = False) -> List[Dict[str, Any]]:
        """Get latest tweets with optional wisdom filter."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            query = """
                SELECT * FROM tweets 
                WHERE 1=1
            """
            
            if wisdom_only:
                query += " AND wisdom_score >= ?"
                params = [self.config.wisdom_threshold, limit]
            else:
                params = [limit]
                
            query += " ORDER BY created_at DESC LIMIT ?"
            
            cursor = conn.execute(query, params)
            return [self._row_to_tweet(row) for row in cursor.fetchall()]
            
    def get_unprocessed_tweets(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get tweets that haven't been analyzed yet."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            cursor = conn.execute("""
                SELECT * FROM tweets 
                WHERE processed = 0 
                ORDER BY created_at DESC 
                LIMIT ?
            """, [limit])
            
            return [self._row_to_tweet(row) for row in cursor.fetchall()]
            
    def update_tweet_analysis(self, tweet_id: str, wisdom_score: int, has_code: bool, tools: List[str]):
        """Update tweet with analysis results."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE tweets 
                SET wisdom_score = ?, 
                    has_code = ?, 
                    tools_mentioned = ?,
                    processed = 1
                WHERE id = ?
            """, (wisdom_score, has_code, json.dumps(tools), tweet_id))
            conn.commit()
            
    def save_knowledge(self, tweet_id: str, pattern: str, category: str, confidence: float):
        """Save extracted knowledge pattern."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO knowledge (tweet_id, pattern, category, confidence)
                VALUES (?, ?, ?, ?)
            """, (tweet_id, pattern, category, confidence))
            conn.commit()
            
    def search_tweets(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Full-text search in tweets."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Simple LIKE search - could upgrade to FTS5
            cursor = conn.execute("""
                SELECT * FROM tweets 
                WHERE text LIKE ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, [f"%{query}%", limit])
            
            return [self._row_to_tweet(row) for row in cursor.fetchall()]
            
    def get_tweets_by_period(self, period: str) -> List[Dict[str, Any]]:
        """Get tweets for a specific period."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            if period == 'today':
                start_date = datetime.now().replace(hour=0, minute=0, second=0)
            elif period == 'week':
                start_date = datetime.now() - timedelta(days=7)
            elif period == 'month':
                start_date = datetime.now() - timedelta(days=30)
            else:
                start_date = datetime.now() - timedelta(days=1)
                
            cursor = conn.execute("""
                SELECT * FROM tweets 
                WHERE created_at >= ? 
                ORDER BY wisdom_score DESC, created_at DESC
            """, [start_date.isoformat()])
            
            return [self._row_to_tweet(row) for row in cursor.fetchall()]
            
    def save_digest(self, period: str, content: str, tweet_count: int):
        """Save a generated digest."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO digests (period, content, tweet_count)
                VALUES (?, ?, ?)
            """, (period, content, tweet_count))
            conn.commit()
            
    def get_last_tweet_id(self) -> Optional[str]:
        """Get the ID of the most recent tweet (for since_id)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id FROM tweets ORDER BY created_at DESC LIMIT 1")
            row = cursor.fetchone()
            return row[0] if row else None
            
    def _row_to_tweet(self, row) -> Dict[str, Any]:
        """Convert database row to tweet dict."""
        tweet = dict(row)
        
        # Parse JSON fields
        for field in ['mentions', 'urls', 'hashtags', 'metrics']:
            if tweet.get(field):
                try:
                    tweet[field] = json.loads(tweet[field])
                except:
                    tweet[field] = []
                    
        return tweet
        
    def health_check(self) -> Dict[str, Any]:
        """Check database health."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) as count FROM tweets")
                tweet_count = cursor.fetchone()[0]
                
                # Check if DB is writable
                conn.execute("INSERT INTO tweets (id, text, created_at) VALUES ('test', 'test', ?)", 
                           [datetime.now().isoformat()])
                conn.execute("DELETE FROM tweets WHERE id = 'test'")
                conn.commit()
                
            return {
                "ok": True,
                "tweet_count": tweet_count,
                "db_size": self.db_path.stat().st_size
            }
        except Exception as e:
            return {
                "ok": False,
                "message": str(e)
            }