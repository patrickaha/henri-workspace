"""Base agent class following Peter's patterns."""

import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
import backoff

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Base class for all parallel agents.
    Each agent runs independently but can communicate via message queue.
    """
    
    def __init__(self, config, message_queue, name: str):
        self.config = config
        self.message_queue = message_queue
        self.name = name
        self.cycle_count = 0
        self.last_error = None
        
    @abstractmethod
    def run_cycle(self):
        """Run one cycle of the agent's work."""
        pass
        
    def handle_message(self, message: Dict[str, Any]):
        """Handle incoming message from other agents."""
        # Default: log and ignore
        logger.debug(f"{self.name} received message: {message}")
        
    def send_message(self, target: str, message_type: str, data: Any):
        """Send message to another agent or broadcast."""
        message = {
            "from": self.name,
            "target": target,
            "type": message_type,
            "data": data,
            "timestamp": time.time()
        }
        self.message_queue.put(message)
        
    def broadcast(self, message_type: str, data: Any):
        """Broadcast message to all agents."""
        self.send_message(None, message_type, data)
        
    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=3,
        on_backoff=lambda details: logger.warning(f"Retrying after error: {details['exception']}")
    )
    def safe_run_cycle(self):
        """Run cycle with automatic retry on failure."""
        try:
            self.run_cycle()
            self.cycle_count += 1
            self.last_error = None
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"{self.name} cycle failed: {e}")
            raise
            
    def sleep_until_next_cycle(self, interval_seconds: int):
        """Sleep but check for messages."""
        end_time = time.time() + interval_seconds
        
        while time.time() < end_time:
            # Check for urgent messages
            remaining = end_time - time.time()
            if remaining <= 0:
                break
                
            # Sleep in small increments to stay responsive
            time.sleep(min(1, remaining))