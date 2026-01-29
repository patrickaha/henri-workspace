"""Content Analyzer - Agent 3: Analyzes tweet content for wisdom and patterns."""

import re
import logging
import queue
from typing import List, Tuple
from .base import BaseAgent
from ..storage import Storage

logger = logging.getLogger(__name__)

class ContentAnalyzer(BaseAgent):
    """
    Analyzes tweet content for:
    - Wisdom score (1-10)
    - Code snippets
    - Mentioned tools/technologies
    - Architectural patterns
    """
    
    def __init__(self, config, message_queue):
        super().__init__(config, message_queue, "Content Analyzer")
        self.storage = Storage(config)
        self.work_queue = queue.Queue()
        self._init_patterns()
        
    def _init_patterns(self):
        """Initialize patterns for detection."""
        # Tool/tech patterns
        self.tool_patterns = [
            # AI/ML tools
            r'\b(claude|gpt|codex|opus|sonnet|gemini|llm|agent)\b',
            # Dev tools
            r'\b(typescript|python|rust|go|swift|nodejs|react|nextjs)\b',
            # Peter's specific tools
            r'\b(clawdbot|cloude?bot|repoprompt|mcporter|tmux|cli)\b',
            # Concepts
            r'\b(parallel|agent|orchestrat|weav|prompt|architect)\b',
        ]
        
        # Code indicators
        self.code_patterns = [
            r'```',  # Code blocks
            r'\b(func|def|class|const|let|var|import|export)\b',  # Keywords
            r'=>|->|\|\||&&',  # Operators
            r'\(\)|\[\]|\{\}',  # Brackets
        ]
        
        # Wisdom indicators
        self.wisdom_keywords = [
            'pattern', 'principle', 'philosophy', 'approach', 'strategy',
            'lesson', 'learned', 'insight', 'realize', 'understand',
            'ship', 'build', 'scale', 'optimize', 'architect',
            'never', 'always', 'wrong', 'right', 'better'
        ]
        
    def handle_message(self, message):
        """Queue tweets for analysis."""
        if message['type'] in ['new_tweet', 'new_reply']:
            self.work_queue.put(message['data'])
            
    def run_cycle(self):
        """Analyze queued tweets."""
        try:
            # Process up to 10 tweets per cycle
            processed = 0
            while processed < 10:
                try:
                    task = self.work_queue.get(timeout=1)
                    self._analyze_tweet(task['tweet_id'])
                    processed += 1
                except queue.Empty:
                    break
                    
            # Also process any unanalyzed tweets from storage
            if processed < 5:
                unprocessed = self.storage.get_unprocessed_tweets(limit=5)
                for tweet in unprocessed:
                    self._analyze_tweet(tweet['id'])
                    
        except Exception as e:
            logger.error(f"Analysis cycle error: {e}")
            
    def _analyze_tweet(self, tweet_id: str):
        """Analyze a single tweet."""
        # Get tweet from storage
        tweets = self.storage.search_tweets(tweet_id, limit=1)
        if not tweets:
            return
            
        tweet = tweets[0]
        text = tweet['text'].lower()
        
        # Calculate wisdom score
        wisdom_score = self._calculate_wisdom_score(text)
        
        # Detect code
        has_code = self._has_code(text)
        
        # Extract tools mentioned
        tools = self._extract_tools(text)
        
        # Update storage
        self.storage.update_tweet_analysis(
            tweet_id,
            wisdom_score,
            has_code,
            tools
        )
        
        logger.info(f"Analyzed tweet {tweet_id}: wisdom={wisdom_score}, code={has_code}, tools={tools}")
        
        # Notify other agents if high wisdom
        if wisdom_score >= self.config.wisdom_threshold:
            self.send_message(
                "Knowledge Extractor",
                "high_wisdom_tweet",
                {
                    "tweet_id": tweet_id,
                    "wisdom_score": wisdom_score,
                    "tools": tools
                }
            )
            
            self.broadcast(
                "wisdom_alert",
                {
                    "tweet_id": tweet_id,
                    "score": wisdom_score,
                    "preview": tweet['text'][:100]
                }
            )
            
    def _calculate_wisdom_score(self, text: str) -> int:
        """Calculate wisdom score 1-10."""
        score = 5  # Base score
        
        # Check for wisdom keywords
        wisdom_count = sum(1 for keyword in self.wisdom_keywords if keyword in text)
        score += min(wisdom_count, 3)
        
        # Length bonus (longer usually more insightful)
        if len(text) > 200:
            score += 1
        if len(text) > 400:
            score += 1
            
        # Specific high-value patterns
        if 'i learned' in text or 'lesson' in text:
            score += 1
        if 'never' in text or 'always' in text:
            score += 1
        if 'ship' in text and ('fast' in text or 'quick' in text):
            score += 1
            
        # Peter-specific patterns
        if 'parallel' in text and 'agent' in text:
            score += 2
        if 'close the loop' in text:
            score += 2
        if 'weav' in text:  # weave, weaving
            score += 1
            
        return min(score, 10)
        
    def _has_code(self, text: str) -> bool:
        """Detect if tweet contains code."""
        for pattern in self.code_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
        
    def _extract_tools(self, text: str) -> List[str]:
        """Extract mentioned tools/technologies."""
        tools = set()
        
        for pattern in self.tool_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            tools.update(matches)
            
        # Special case extractions
        if 'gpt' in text:
            if '5.2' in text:
                tools.add('gpt-5.2')
            elif '4' in text:
                tools.add('gpt-4')
                
        return list(tools)