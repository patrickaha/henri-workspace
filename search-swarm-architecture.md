# Search Swarm Architecture
*Query-driven tool selection for optimal results*

## Query Analysis & Routing Logic

### 1. Query Classification

```python
def classify_query(query):
    """Analyze query to determine search strategy"""
    
    # Check for specific platforms
    if "x.com" in query or "twitter" in query:
        return ["bird", "firecrawl"]
    
    if "reddit" in query:
        return ["reddit_api", "brave"]
    
    # Check for temporal needs
    if any(word in query.lower() for word in ["today", "latest", "current", "breaking"]):
        return ["perplexity", "brave"]
    
    # Academic/research queries
    if any(word in query.lower() for word in ["paper", "research", "study", "academic"]):
        return ["exa", "perplexity"]
    
    # Code/technical queries
    if any(word in query.lower() for word in ["code", "github", "api", "function"]):
        return ["exa", "github_search"]
    
    # Video/multimedia
    if any(word in query.lower() for word in ["youtube", "video", "watch"]):
        return ["summarize", "brave"]
    
    # Deep analysis needed
    if any(word in query.lower() for word in ["analyze", "compare", "opinion"]):
        return ["perplexity", "llm_panel"]
    
    # Default: single tool suffices
    return ["brave"]
```

### 2. Tool Stack

#### Primary Search Tools
- **Perplexity**: Real-time + citations
- **Brave**: Privacy-focused, 30B pages
- **Exa**: Semantic/similarity search
- **Firecrawl**: JavaScript scraping
- **Browserbase**: Full browser automation
- **Gemini CLI**: Google-grounded search

#### Platform-Specific
- **Bird**: X/Twitter content
- **Reddit API**: Reddit discussions
- **GitHub**: Code search
- **Summarize**: YouTube/video transcripts

#### LLM Opinion Panel
- **Claude**: Nuanced analysis
- **GPT**: Broad knowledge synthesis
- **Grok**: Real-time X integration
- **Gemini**: Google-grounded verification

### 3. Decision Matrix

| Query Type | Primary Tool | Secondary Tool | LLM Panel? |
|------------|--------------|----------------|------------|
| Breaking news | Perplexity | Brave | Optional |
| X.com thread | Bird | Firecrawl | No |
| Academic paper | Exa | Perplexity | Yes (deep) |
| Reddit consensus | Reddit API | Brave | Optional |
| Technical docs | Exa | GitHub | No |
| Product comparison | Perplexity | Exa | Yes |
| Video summary | Summarize | - | No |
| Complex analysis | Perplexity | Brave | Yes |

### 4. Cost Optimization

```python
def estimate_cost(tools, query_complexity):
    costs = {
        "perplexity": 0.001,  # $1/1M tokens
        "brave": 0.005,       # $5/1K queries
        "exa": 0.005,         # $5/1K queries
        "firecrawl": 0.01,    # ~1 credit
        "browserbase": 0.02,  # per session
        "claude": 0.015,      # per query
        "gpt": 0.01,          # per query
        "summarize": 0.0,     # free
        "bird": 0.0,          # free
    }
    
    total = sum(costs.get(tool, 0) for tool in tools)
    return total
```

### 5. Result Aggregation Strategy

#### Single Tool Queries
- Return results directly
- Add source attribution

#### Multi-Tool Queries
1. **Parallel execution** for speed
2. **Deduplication** of results
3. **Conflict resolution** (newer > older, cited > uncited)
4. **Synthesis** into coherent response

#### LLM Panel Queries
1. Gather raw data from search tools
2. Submit to 2-3 LLMs for analysis
3. Synthesize perspectives
4. Highlight agreements/disagreements

### 6. Example Query Flows

**"Latest developments in AI agents security"**
```
→ Classify: temporal + technical
→ Tools: Perplexity + Brave
→ Cost: $0.006
→ Execute: Parallel search
→ Synthesize: Merge with citation priority
```

**"What does X.com think about the new GPT model?"**
```
→ Classify: platform-specific + opinion
→ Tools: Bird + Firecrawl + LLM Panel
→ Cost: $0.025
→ Execute: Bird → Extract → LLM analysis
```

**"Find similar papers to [arxiv link]"**
```
→ Classify: academic + similarity
→ Tools: Exa
→ Cost: $0.005
→ Execute: Single tool sufficient
```

### 7. Implementation Plan

1. **Query Analyzer Agent**
   - Parses query intent
   - Estimates cost
   - Selects tools

2. **Execution Orchestrator**
   - Manages parallel searches
   - Handles failures/retries
   - Optimizes for speed

3. **Result Synthesizer**
   - Deduplicates findings
   - Resolves conflicts
   - Formats output

4. **Cost Monitor**
   - Tracks spending
   - Suggests optimizations
   - Alerts on high costs

### 8. Reddit Integration

```python
# Reddit-specific routing
if "reddit" in query:
    if "opinion" in query or "consensus" in query:
        tools = ["reddit_api", "reddit_search"]
    elif specific_subreddit:
        tools = ["reddit_api_targeted"]
    else:
        tools = ["brave site:reddit.com"]
```

### 9. Adaptive Learning

Track success metrics:
- Query satisfaction
- Cost per query
- Response time
- Tool effectiveness

Use this data to refine routing logic over time.

## Next Steps

1. Build query classifier
2. Implement tool orchestrator
3. Create result synthesizer
4. Add cost tracking
5. Deploy as search swarm