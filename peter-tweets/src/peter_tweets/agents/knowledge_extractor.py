"""Knowledge Extractor - Agent 5: Extracts patterns and updates knowledge base."""

import logging
import re
import queue
from datetime import datetime
from typing import Dict, List, Tuple
from .base import BaseAgent
from ..storage import Storage

logger = logging.getLogger(__name__)

class KnowledgeExtractor(BaseAgent):
    """
    Extracts architectural patterns, principles, and insights.
    Updates the permanent knowledge base with Peter's wisdom.
    """
    
    def __init__(self, config, message_queue):
        super().__init__(config, message_queue, "Knowledge Extractor")
        self.storage = Storage(config)
        self.work_queue = queue.Queue()
        self._init_patterns()
        
    def _init_patterns(self):
        """Initialize pattern recognition rules."""
        self.pattern_categories = {
            "architecture": [
                r"architect\w*", r"design\w*", r"structure\w*", r"system\w*",
                r"pattern\w*", r"principle\w*"
            ],
            "parallel_agents": [
                r"parallel", r"agent\w*", r"orchestrat\w*", r"tmux",
                r"terminal\w*", r"concurrent\w*", r"simultan\w*"
            ],
            "development_flow": [
                r"ship\w*", r"deploy\w*", r"commit\w*", r"build\w*",
                r"test\w*", r"verif\w*", r"valid\w*"
            ],
            "ai_coding": [
                r"prompt\w*", r"llm", r"ai", r"claude", r"gpt", r"codex",
                r"agent\w*", r"model\w*"
            ],
            "philosophy": [
                r"always", r"never", r"should\w*", r"must\w*", r"principle\w*",
                r"belief\w*", r"approach\w*"
            ],
            "tooling": [
                r"cli", r"tool\w*", r"command\w*", r"script\w*", r"automat\w*"
            ]
        }
        
        # Specific patterns to extract
        self.extraction_patterns = [
            # Direct statements
            (r"always (\w+)", "principle"),
            (r"never (\w+)", "principle"),
            (r"you should (\w+)", "recommendation"),
            (r"the secret is (\w+)", "insight"),
            (r"i learned that (\w+)", "lesson"),
            
            # Architectural patterns
            (r"(\w+) architecture", "architecture"),
            (r"(\w+) pattern", "pattern"),
            (r"(\w+) principle", "principle"),
            
            # Workflow patterns  
            (r"(\d+) agents?", "parallel_count"),
            (r"(\d+) commits?/day", "productivity"),
            (r"close the loop", "methodology"),
            (r"weav\w+ (code|in)", "methodology")
        ]
        
    def handle_message(self, message):
        """Queue high-value content for extraction."""
        if message['type'] in ['high_wisdom_tweet', 'peter_conversation', 'significant_conversation']:
            self.work_queue.put(message)
            
    def run_cycle(self):
        """Extract knowledge from queued items."""
        try:
            # Process queue
            processed = 0
            while processed < 5:
                try:
                    task = self.work_queue.get(timeout=1)
                    
                    if task['type'] == 'high_wisdom_tweet':
                        self._extract_from_tweet(task['data']['tweet_id'])
                    elif task['type'] == 'peter_conversation':
                        self._extract_from_conversation(task['data'])
                    elif task['type'] == 'significant_conversation':
                        self._extract_from_thread(task['data'])
                        
                    processed += 1
                except queue.Empty:
                    break
                    
            # Periodically consolidate knowledge
            if self.cycle_count % 100 == 0:
                self._consolidate_knowledge()
                
        except Exception as e:
            logger.error(f"Knowledge extraction error: {e}")
            
    def _extract_from_tweet(self, tweet_id: str):
        """Extract knowledge from a single tweet."""
        tweets = self.storage.search_tweets(tweet_id, limit=1)
        if not tweets:
            return
            
        tweet = tweets[0]
        text = tweet['text']
        
        # Categorize tweet
        categories = self._categorize_text(text)
        
        # Extract specific patterns
        patterns = self._extract_patterns(text)
        
        # Save knowledge entries
        for pattern, pattern_type in patterns:
            confidence = 0.8 if len(categories) > 1 else 0.6
            
            self.storage.save_knowledge(
                tweet_id,
                pattern,
                pattern_type,
                confidence
            )
            
            logger.info(f"Extracted {pattern_type}: {pattern}")
            
    def _extract_from_conversation(self, data: Dict):
        """Extract patterns from Peter's conversations."""
        # Get all tweets in conversation
        original_id = data['original_tweet']
        reply_ids = data['peter_replies']
        
        # Analyze conversation flow and extract insights
        for reply_id in reply_ids:
            self._extract_from_tweet(reply_id)
            
    def _extract_from_thread(self, data: Dict):
        """Extract from significant conversation thread."""
        # Would implement thread analysis here
        logger.info(f"Analyzing thread {data['conversation_id']} with {data['tweet_count']} tweets")
        
    def _categorize_text(self, text: str) -> List[str]:
        """Categorize text into knowledge domains."""
        categories = []
        text_lower = text.lower()
        
        for category, patterns in self.pattern_categories.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    categories.append(category)
                    break
                    
        return categories
        
    def _extract_patterns(self, text: str) -> List[Tuple[str, str]]:
        """Extract specific patterns from text."""
        extracted = []
        
        for pattern, pattern_type in self.extraction_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = " ".join(match)
                extracted.append((match, pattern_type))
                
        return extracted
        
    def _consolidate_knowledge(self):
        """Periodically consolidate and export knowledge base."""
        logger.info("Consolidating knowledge base")
        
        # Would implement knowledge consolidation here
        # - Group similar patterns
        # - Identify recurring themes
        # - Export to knowledge base file
        
        self.broadcast(
            "knowledge_consolidated",
            {"timestamp": datetime.now().isoformat()}
        )