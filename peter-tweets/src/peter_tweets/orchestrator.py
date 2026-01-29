"""Orchestrator for parallel agents - Peter's Starcraft-style management."""

import threading
import queue
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .agents import (
    TimelineMonitor,
    ReplyHarvester,
    ContentAnalyzer,
    DigestBuilder,
    KnowledgeExtractor
)

logger = logging.getLogger(__name__)

class Orchestrator:
    """
    Manages parallel agents like Peter manages his 5-10 terminal sessions.
    Each agent runs independently but coordinates through message passing.
    """
    
    def __init__(self, config, num_agents: int = 5):
        self.config = config
        self.num_agents = num_agents
        self.agents = []
        self.threads = []
        self.running = False
        self.message_queue = queue.Queue()
        self.status_lock = threading.Lock()
        self.agent_status = {}
        
    def start(self):
        """Start all parallel agents."""
        self.running = True
        
        # Initialize agents
        agents_config = [
            ("Timeline Monitor", TimelineMonitor),
            ("Reply Harvester", ReplyHarvester),
            ("Content Analyzer", ContentAnalyzer),
            ("Digest Builder", DigestBuilder),
            ("Knowledge Extractor", KnowledgeExtractor)
        ]
        
        # Start agents up to num_agents
        for i in range(min(self.num_agents, len(agents_config))):
            name, agent_class = agents_config[i]
            agent = agent_class(self.config, self.message_queue)
            self.agents.append(agent)
            
            # Track status
            self.agent_status[name] = {
                "name": name,
                "status": "starting",
                "tasks_completed": 0,
                "start_time": datetime.now(),
                "last_activity": datetime.now()
            }
            
            # Start in thread
            thread = threading.Thread(
                target=self._run_agent,
                args=(agent, name),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
            
        # Start message dispatcher
        dispatcher = threading.Thread(target=self._dispatch_messages, daemon=True)
        dispatcher.start()
        
        logger.info(f"Started {self.num_agents} parallel agents")
        
    def stop(self):
        """Stop all agents gracefully."""
        self.running = False
        
        # Send stop message to all agents
        for _ in range(self.num_agents):
            self.message_queue.put({"type": "stop"})
            
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=5)
            
        logger.info("All agents stopped")
        
    def _run_agent(self, agent, name: str):
        """Run an agent in its own thread."""
        while self.running:
            try:
                # Update status
                with self.status_lock:
                    self.agent_status[name]["status"] = "running"
                    self.agent_status[name]["last_activity"] = datetime.now()
                    
                # Run agent's main loop
                agent.run_cycle()
                
                # Update completed tasks
                with self.status_lock:
                    self.agent_status[name]["tasks_completed"] += 1
                    
            except Exception as e:
                logger.error(f"Agent {name} error: {e}")
                
                with self.status_lock:
                    self.agent_status[name]["status"] = "error"
                    
                # Self-healing: wait and retry
                time.sleep(self.config.retry_delay)
                
        with self.status_lock:
            self.agent_status[name]["status"] = "stopped"
            
    def _dispatch_messages(self):
        """Dispatch messages between agents."""
        while self.running:
            try:
                # Get message with timeout
                message = self.message_queue.get(timeout=1)
                
                if message.get("type") == "stop":
                    continue
                    
                # Route message to appropriate agent
                target = message.get("target")
                if target:
                    for agent in self.agents:
                        if agent.name == target:
                            agent.handle_message(message)
                            break
                else:
                    # Broadcast to all agents
                    for agent in self.agents:
                        agent.handle_message(message)
                        
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Message dispatch error: {e}")
                
    def get_status(self) -> List[Dict[str, Any]]:
        """Get status of all agents."""
        with self.status_lock:
            status_list = []
            
            for name, status in self.agent_status.items():
                uptime = datetime.now() - status["start_time"]
                
                status_list.append({
                    "name": name,
                    "status": status["status"],
                    "tasks_completed": status["tasks_completed"],
                    "uptime": self._format_duration(uptime),
                    "idle_time": (datetime.now() - status["last_activity"]).total_seconds()
                })
                
        return status_list
        
    def _format_duration(self, duration: timedelta) -> str:
        """Format duration for display."""
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"