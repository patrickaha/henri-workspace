# Firecrawl: Comprehensive Web Scraping & Content Extraction Research

## Overview

Firecrawl is a powerful API service designed to convert websites into clean, LLM-ready data. It specializes in handling complex web scraping scenarios including JavaScript-heavy sites, dynamic content, and structured data extraction. Unlike simple HTTP scrapers, Firecrawl renders pages fully and can interact with elements before extraction.

## Core Capabilities

### 1. JavaScript & Dynamic Content Handling

**Strengths:**
- **Full JavaScript rendering**: Firecrawl executes JavaScript and waits for dynamic content to load
- **Smart wait feature**: Automatically detects when pages are fully loaded
- **Additional wait time**: Can specify extra `waitFor` parameter (in milliseconds) for slow-loading content
- **Browser actions**: Can interact with pages before scraping:
  - Click buttons/links
  - Fill forms and submit data
  - Scroll to load infinite scroll content
  - Execute custom JavaScript
  - Press keyboard keys
  - Take screenshots at various stages

**Example actions workflow:**
```json
{
  "actions": [
    {"type": "wait", "duration": 2000},
    {"type": "click", "selector": "#load-more-button"},
    {"type": "wait", "selector": ".loaded-content"},
    {"type": "scroll", "direction": "down"},
    {"type": "screenshot", "fullPage": true}
  ]
}
```

### 2. Structured Data Extraction

**JSON Mode:**
- Extract structured data using schemas (supports Pydantic)
- Can extract without schema using just a prompt
- LLM automatically determines structure based on content

**Extract Endpoint (Beta):**
- Advanced AI-powered extraction from single pages, multiple pages, or entire domains
- Supports wildcards (e.g., `https://example.com/*`)
- Can follow links outside the domain with `enableWebSearch`
- FIRE-1 agent available for complex multi-page navigation

**Example structured extraction:**
```json
{
  "prompt": "Extract all product information",
  "schema": {
    "type": "object",
    "properties": {
      "products": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "price": {"type": "string"},
            "features": {"type": "array", "items": {"type": "string"}}
          }
        }
      }
    }
  }
}
```

### 3. Output Formats

Firecrawl supports multiple output formats that can be requested simultaneously:
- **Markdown**: Clean, formatted markdown (default)
- **HTML**: Cleaned HTML with optional tag filtering
- **Raw HTML**: Complete unprocessed HTML
- **Summary**: AI-generated content summary
- **Links**: All links found on the page
- **Images**: Image URLs and metadata
- **Screenshot**: Full page screenshots
- **JSON**: Structured data extraction
- **PDF**: Generate PDF of the page

## API Details

### Authentication
- Bearer token authentication required
- API keys available at https://firecrawl.dev

### Key Endpoints

1. **Scrape** (`/v2/scrape`)
   - Single URL scraping with format options
   - Supports actions, headers, mobile emulation
   - Caching available (default 2 days)

2. **Crawl** (`/v2/crawl`)
   - Recursive crawling of entire websites
   - Returns job ID for async processing
   - Can limit depth and filter URLs

3. **Map** (`/v2/map`)
   - Fast sitemap generation
   - Discovers all URLs on a domain

4. **Search** (`/v2/search`)
   - Web search with automatic scraping
   - Returns cleaned content from results
   - Supports multiple sources (web, news, images)

5. **Extract** (`/v2/extract`)
   - AI-powered structured data extraction
   - Supports bulk URLs and wildcards
   - Can use FIRE-1 agent for complex tasks

### Proxy & Anti-Bot Handling

Firecrawl offers three proxy modes:
- **Basic**: Fast proxies for simple sites
- **Stealth**: Advanced proxies for anti-bot protected sites (5 credits/request)
- **Auto**: Automatically retries with stealth if basic fails

Additional anti-bot features:
- Ad blocking and cookie popup removal
- Mobile device emulation
- Custom headers and user agents
- Location-based request routing

## When to Use Firecrawl Over Other Tools

### Use Firecrawl when you need:

1. **JavaScript rendering**: Sites that load content dynamically
2. **Complex interactions**: Need to click, fill forms, or navigate
3. **Structured extraction**: Want clean JSON data from messy HTML
4. **Scale & reliability**: High-volume scraping with proxy rotation
5. **Multi-format output**: Need markdown, screenshots, and data together
6. **AI-powered extraction**: Complex data patterns requiring LLM understanding

### Consider alternatives when:

1. **Simple static HTML**: Basic HTTP requests suffice
2. **Real-time streaming**: Need websocket or live data
3. **Extreme budget constraints**: Free tier is limited to 500 pages
4. **Local-only requirements**: Firecrawl is cloud-based (self-host option available)

## Limitations

1. **Rate Limits**:
   - Free: 500 credits one-time
   - Hobby: 3,000 credits/month
   - Standard: 100,000 credits/month
   - Growth: 500,000 credits/month

2. **Concurrency**:
   - Free: 2 concurrent requests
   - Hobby: 5 concurrent requests
   - Standard: 50 concurrent requests
   - Growth: 100 concurrent requests

3. **Beta Features**:
   - Extract endpoint still in beta
   - Large-scale site coverage not fully supported
   - Complex logical queries may be inconsistent

4. **Technical Limits**:
   - 300-second maximum timeout per request
   - PDF extraction charged per page (1 credit/page)
   - Stealth proxy costs 5x regular requests

## Integration Options

### SDKs Available:
- Python
- Node.js
- CLI tool
- Go (community)
- Rust (community, v1 only)

### Framework Integrations:
- LangChain (Python & JS)
- LlamaIndex
- Crew.ai
- Dify
- Zapier
- And many more

## Best Practices

1. **Use caching**: Enable `maxAge` to avoid redundant scrapes
2. **Choose appropriate proxy mode**: Start with auto, use stealth only when needed
3. **Batch requests**: Use crawl/extract for multiple pages instead of individual scrapes
4. **Specify output formats**: Only request formats you need to save credits
5. **Handle async jobs**: Use job IDs to check status for large crawls
6. **Test with actions**: Use wait actions liberally when dealing with dynamic content

## Conclusion

Firecrawl excels at converting complex, JavaScript-heavy websites into clean, structured data. Its strength lies in handling dynamic content, providing multiple output formats, and offering AI-powered extraction capabilities. While it has a cost associated with it, the reliability, proxy handling, and advanced features make it valuable for serious web scraping projects where simple HTTP requests fall short.