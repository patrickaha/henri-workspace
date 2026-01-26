#!/usr/bin/env python3
"""
Analyze chat patterns to identify agent opportunities.
"""

import json
import argparse
from collections import Counter, defaultdict
from datetime import datetime
import re
import hashlib

class AgentOpportunityAnalyzer:
    def __init__(self, chat_data, config=None):
        self.chat_data = chat_data
        self.config = config or self.default_config()
        self.patterns = defaultdict(list)
        self.tool_usage = Counter()
        self.repetitive_tasks = []
        self.workflow_sequences = []
        
    def default_config(self):
        return {
            "min_pattern_frequency": 3,
            "similarity_threshold": 0.8,
            "high_impact_keywords": [
                "every day", "always have to", "keeps happening",
                "again", "same thing", "repeat", "routine"
            ],
            "tool_indicators": [
                "run", "execute", "check", "analyze", "generate",
                "create", "update", "deploy", "test"
            ]
        }
    
    def analyze(self):
        """Run all analysis modules."""
        results = {
            "summary": self._generate_summary(),
            "repetitive_tasks": self._find_repetitive_tasks(),
            "tool_patterns": self._analyze_tool_usage(),
            "workflow_bottlenecks": self._find_workflows(),
            "recommendations": self._generate_recommendations()
        }
        return results
    
    def _generate_summary(self):
        """Generate analysis summary statistics."""
        total_messages = 0
        unique_users = set()
        channels_analyzed = []
        
        # Count messages and users
        for channel, data in self.chat_data.get("channels", {}).items():
            channels_analyzed.append(channel)
            for msg in data.get("messages", []):
                total_messages += 1
                unique_users.add(msg.get("user"))
        
        return {
            "total_messages": total_messages,
            "unique_participants": len(unique_users),
            "channels_analyzed": channels_analyzed,
            "date_range": self.chat_data.get("date_range")
        }
    
    def _find_repetitive_tasks(self):
        """Identify repetitive requests and patterns."""
        message_patterns = defaultdict(list)
        
        for channel, data in self.chat_data.get("channels", {}).items():
            for msg in data.get("messages", []):
                text = msg.get("text", "").lower()
                
                # Skip very short messages
                if len(text) < 10:
                    continue
                
                # Create pattern signature
                pattern = self._extract_pattern(text)
                if pattern:
                    message_patterns[pattern].append({
                        "channel": channel,
                        "timestamp": msg.get("ts"),
                        "user": msg.get("user"),
                        "original_text": msg.get("text")
                    })
        
        # Filter patterns by frequency
        repetitive = []
        for pattern, instances in message_patterns.items():
            if len(instances) >= self.config["min_pattern_frequency"]:
                repetitive.append({
                    "pattern": pattern,
                    "frequency": len(instances),
                    "examples": instances[:3]  # First 3 examples
                })
        
        return sorted(repetitive, key=lambda x: x["frequency"], reverse=True)
    
    def _extract_pattern(self, text):
        """Extract actionable pattern from message text."""
        # Remove URLs, user mentions, channel references
        text = re.sub(r'https?://\S+', '[URL]', text)
        text = re.sub(r'<@U\w+>', '[USER]', text)
        text = re.sub(r'<#C\w+>', '[CHANNEL]', text)
        
        # Look for action patterns
        for indicator in self.config["tool_indicators"]:
            if indicator in text:
                # Extract the action phrase
                match = re.search(rf'{indicator}\s+(\w+\s+){{1,4}}', text)
                if match:
                    return match.group(0)
        
        # Look for question patterns
        if "?" in text:
            # Extract question structure
            question_words = ["how", "what", "when", "where", "can", "should"]
            for word in question_words:
                if text.startswith(word):
                    return f"{word} [QUERY]"
        
        return None
    
    def _analyze_tool_usage(self):
        """Analyze patterns of tool/command usage."""
        tool_patterns = Counter()
        command_sequences = defaultdict(list)
        
        for channel, data in self.chat_data.get("channels", {}).items():
            messages = data.get("messages", [])
            
            for i, msg in enumerate(messages):
                text = msg.get("text", "")
                
                # Look for command-like patterns
                commands = re.findall(r'`([^`]+)`', text)
                for cmd in commands:
                    tool_patterns[cmd] += 1
                
                # Track command sequences
                if i > 0 and commands:
                    prev_msg = messages[i-1]
                    prev_commands = re.findall(r'`([^`]+)`', prev_msg.get("text", ""))
                    if prev_commands and prev_msg.get("user") == msg.get("user"):
                        for prev_cmd in prev_commands:
                            command_sequences[prev_cmd].append(commands[0])
        
        return {
            "most_used_tools": tool_patterns.most_common(10),
            "common_sequences": self._analyze_sequences(command_sequences)
        }
    
    def _analyze_sequences(self, sequences):
        """Find common command sequences."""
        common_sequences = []
        
        for cmd, next_cmds in sequences.items():
            if len(next_cmds) >= 2:
                most_common_next = Counter(next_cmds).most_common(1)
                if most_common_next:
                    next_cmd, count = most_common_next[0]
                    if count >= 2:
                        common_sequences.append({
                            "sequence": f"{cmd} -> {next_cmd}",
                            "frequency": count
                        })
        
        return sorted(common_sequences, key=lambda x: x["frequency"], reverse=True)
    
    def _find_workflows(self):
        """Identify multi-step workflows that could be automated."""
        workflows = []
        
        # Look for threads with multiple back-and-forth messages
        for channel, data in self.chat_data.get("channels", {}).items():
            threads = defaultdict(list)
            
            for msg in data.get("messages", []):
                thread_ts = msg.get("thread_ts")
                if thread_ts:
                    threads[thread_ts].append(msg)
            
            # Analyze threads for workflow patterns
            for thread_ts, messages in threads.items():
                if len(messages) >= 5:  # Substantial thread
                    workflow = self._extract_workflow(messages)
                    if workflow:
                        workflows.append(workflow)
        
        return workflows
    
    def _extract_workflow(self, thread_messages):
        """Extract workflow pattern from thread."""
        steps = []
        participants = set()
        
        for msg in thread_messages:
            participants.add(msg.get("user"))
            text = msg.get("text", "")
            
            # Look for step indicators
            if any(indicator in text.lower() for indicator in ["first", "then", "next", "finally", "step"]):
                steps.append(text[:100])  # First 100 chars
        
        if len(steps) >= 3:
            return {
                "thread_ts": thread_messages[0].get("thread_ts"),
                "participants": len(participants),
                "step_count": len(steps),
                "sample_steps": steps[:3]
            }
        
        return None
    
    def _generate_recommendations(self):
        """Generate specific agent recommendations."""
        recommendations = []
        
        # Analyze repetitive tasks
        for task in self.patterns.get("repetitive_tasks", [])[:5]:
            agent = self._recommend_agent_for_pattern(task)
            if agent:
                recommendations.append(agent)
        
        # Analyze tool usage patterns  
        tool_patterns = self.patterns.get("tool_patterns", {})
        if tool_patterns.get("most_used_tools"):
            for tool, frequency in tool_patterns["most_used_tools"][:3]:
                agent = self._recommend_agent_for_tool(tool, frequency)
                if agent:
                    recommendations.append(agent)
        
        # Rank by priority
        for rec in recommendations:
            rec["priority"] = self._calculate_priority(rec)
        
        return sorted(recommendations, key=lambda x: x["priority"], reverse=True)
    
    def _recommend_agent_for_pattern(self, pattern):
        """Generate agent recommendation for a pattern."""
        pattern_text = pattern.get("pattern", "")
        
        # Map patterns to agent types
        if "deploy" in pattern_text or "release" in pattern_text:
            return {
                "name": "deployment-assistant",
                "role": "Automated deployment and release management",
                "trigger_phrases": ["deploy", "release", "rollout"],
                "estimated_time_savings": pattern.get("frequency", 0) * 15,  # 15 min per instance
                "evidence": pattern.get("examples", [])
            }
        
        if "check" in pattern_text or "status" in pattern_text:
            return {
                "name": "status-monitor", 
                "role": "Proactive system status checking and reporting",
                "trigger_phrases": ["check status", "how is", "what's the status"],
                "estimated_time_savings": pattern.get("frequency", 0) * 5,  # 5 min per check
                "evidence": pattern.get("examples", [])
            }
        
        # Add more pattern mappings as needed
        return None
    
    def _recommend_agent_for_tool(self, tool, frequency):
        """Generate agent recommendation for tool usage."""
        # This is simplified - in reality would analyze the context around tool usage
        return None
    
    def _calculate_priority(self, recommendation):
        """Calculate priority score for recommendation."""
        score = 0
        
        # Time savings weight
        score += recommendation.get("estimated_time_savings", 0) * 2
        
        # Evidence weight
        score += len(recommendation.get("evidence", [])) * 10
        
        # Complexity reduction (workflows are higher priority)
        if "workflow" in recommendation.get("role", "").lower():
            score += 50
        
        return score

def format_report(analysis_results):
    """Format analysis results as markdown report."""
    report = []
    report.append("# Agent Hiring Recommendations")
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    report.append("")
    
    # Summary
    summary = analysis_results.get("summary", {})
    report.append("## Executive Summary")
    report.append(f"- Total messages analyzed: {summary.get('total_messages', 0)}")
    report.append(f"- Unique participants: {summary.get('unique_participants', 0)}")
    
    # Top recommendation
    recs = analysis_results.get("recommendations", [])
    if recs:
        report.append(f"- Top opportunity: {recs[0].get('name', 'Unknown')}")
    
    report.append("")
    
    # Detailed recommendations
    report.append("## Recommended Hires")
    report.append("")
    
    for i, rec in enumerate(recs[:5], 1):
        report.append(f"### {i}. {rec.get('name', 'Unknown Agent')}")
        report.append(f"**Role:** {rec.get('role', 'No description')}")
        report.append("**Trigger Phrases:**")
        for phrase in rec.get('trigger_phrases', []):
            report.append(f"- \"{phrase}\"")
        report.append(f"**Expected Time Savings:** {rec.get('estimated_time_savings', 0)} minutes/week")
        report.append(f"**Implementation Priority:** High")
        report.append("")
        report.append("**Evidence from chat:**")
        for example in rec.get('evidence', [])[:3]:
            report.append(f"- [{example.get('timestamp')}] {example.get('channel')} - \"{example.get('original_text', '')[:100]}...\"")
        report.append("")
    
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='Analyze chat patterns for agent opportunities')
    parser.add_argument('input_file', help='Chat export JSON file')
    parser.add_argument('--output', default='analysis_report.md', help='Output report file')
    parser.add_argument('--quick', action='store_true', help='Quick analysis without LLM enhancement')
    parser.add_argument('--config', help='Configuration file')
    
    args = parser.parse_args()
    
    # Load chat data
    with open(args.input_file, 'r') as f:
        chat_data = json.load(f)
    
    # Run analysis
    analyzer = AgentOpportunityAnalyzer(chat_data)
    results = analyzer.analyze()
    
    # Format and save report
    report = format_report(results)
    with open(args.output, 'w') as f:
        f.write(report)
    
    print(f"Analysis complete. Report saved to {args.output}")

if __name__ == "__main__":
    main()