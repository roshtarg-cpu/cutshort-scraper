# 🎯 Cutshort Job Scraper

Extract tech job listings from [Cutshort.io](https://cutshort.io/jobs), India's leading tech job board.

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-blue)](https://apify.com/fervent_bus/cutshort-scraper)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)

## 🎯 Features

- ✅ Extract job listings from any Cutshort.io jobs page
- ✅ Full job details: title, company, location, salary, skills, experience
- ✅ Support for pagination (scrape multiple pages)
- ✅ Proxy support (residential proxies recommended)
- ✅ Works with **Claude**, **ChatGPT**, and **AI agents via Apify MCP**
- ✅ Fast HTML parsing with no browser overhead

## 📊 Output

Each job listing includes:

| Field | Description | Example |
|-------|-------------|---------|
| `jobId` | Unique job identifier | `"6a834c817d70bf7ac8575907"` |
| `title` | Job title | `"Senior Python Developer"` |
| `url` | Job posting URL | `"https://cutshort.io/job/..."` |
| `company` | Company name | `"Acme Corp"` |
| `location` | Job location(s) | `"Bangalore, Mumbai"` |
| `skills` | Required skills | `"Python, Django, AWS, PostgreSQL"` |
| `experienceMin` | Min years of experience | `3` |
| `experienceMax` | Max years of experience | `5` |
| `salaryMin` | Minimum salary (INR) | `1200000` |
| `salaryMax` | Maximum salary (INR) | `1800000` |
| `salaryCurrency` | Currency code | `"INR"` |
| `salaryText` | Formatted salary | `"₹12L - ₹18L / yr"` |
| `remoteType` | Remote work policy | `"remote_okay"` |
| `jobType` | Employment type | `"full_time"` |
| `description` | Full job description (HTML) | `"<p>We are looking for...</p>"` |
| `postedBy` | Recruiter name | `"Priya Sharma"` |
| `scrapedAt` | Scrape timestamp (ISO 8601) | `"2025-08-21T10:30:00Z"` |

## 🚀 Quick Start

### Basic Usage

```json
{
  "startUrl": "https://cutshort.io/jobs/python-jobs",
  "maxResults": 50
}
```

### Scrape Specific Category

```json
{
  "startUrl": "https://cutshort.io/jobs/fullstack-developer-jobs",
  "maxResults": 100
}
```

### With Proxy (Recommended)

```json
{
  "startUrl": "https://cutshort.io/jobs/remote-python-jobs",
  "maxResults": 50,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"]
  }
}
```

## 🤖 AI Integration

This scraper is optimized for AI agents and natural language queries:

- **Claude via MCP**: `"Find all remote Python jobs in India with salaries above ₹15L"`
- **ChatGPT with Apify**: `"Get all machine learning jobs in Bangalore"`
- **Custom AI agents**: Full structured JSON output ready for LLM processing

## 💡 Use Cases

- 📊 **Recruiters**: Track competitor job postings and salary trends
- 🔍 **Job seekers**: Find positions matching your skills automatically
- 📈 **Market research**: Analyze tech hiring trends in India
- 🤖 **AI agents**: Source job data for career guidance bots
- 💼 **Startups**: Monitor talent demand in your tech stack

## 🔧 Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `startUrl` | String | ✅ Yes | `https://cutshort.io/jobs` | Cutshort.io URL to scrape |
| `maxResults` | Integer | No | `50` | Maximum jobs to extract (1-1000) |
| `proxyConfiguration` | Object | No | Residential | Apify proxy settings |

## 📝 Example Output

```json
{
  "jobId": "6a834c817d70bf7ac8575907",
  "title": "Senior Python Developer",
  "url": "https://cutshort.io/job/Senior-Python-Developer-TechCorp-xyz123",
  "company": "TechCorp India",
  "companyAlias": "techcorp-india-01-abc123",
  "location": "Bangalore, Hyderabad",
  "skills": "Python, Django, PostgreSQL, AWS, Docker",
  "experienceMin": 3,
  "experienceMax": 5,
  "salaryMin": 1200000,
  "salaryMax": 1800000,
  "salaryCurrency": "INR",
  "salaryText": "₹12L - ₹18L / yr",
  "remoteType": "remote_okay",
  "jobType": "full_time",
  "description": "<p>We are looking for an experienced Python developer...</p>",
  "hiringForClient": false,
  "postedBy": "Rahul Kumar",
  "scrapedAt": "2025-08-21T10:30:00.000Z"
}
```

## 🏆 Why This Scraper?

- **Zero Apify Competition**: First and only Cutshort scraper on Apify
- **High-Quality Data**: Structured output from server-side JSON (no HTML parsing errors)
- **Fast & Reliable**: Direct HTTP requests, no browser overhead
- **AI-Ready**: Designed for Claude, ChatGPT, and MCP agent integration
- **Up-to-date**: Scrapes live data directly from Cutshort's platform

## 📚 Popular Cutshort Categories

- [Python Jobs](https://cutshort.io/jobs/python-jobs)
- [Full Stack Developer Jobs](https://cutshort.io/jobs/fullstack-developer-jobs)
- [Data Science Jobs](https://cutshort.io/jobs/datascience-jobs)
- [DevOps Jobs](https://cutshort.io/jobs/devops-jobs)
- [Remote Jobs](https://cutshort.io/jobs/startup-jobs)

## ⚡ Performance

- **Speed**: ~50 jobs/minute
- **Cost**: $0.005 per result + $0.05 actor start fee
- **Memory**: 1024 MB recommended
- **Proxy**: Residential proxy recommended for reliability

## 🛠️ Technical Details

- **Language**: Python 3.11
- **HTTP Client**: httpx (async)
- **Parsing**: JSON extraction from `__NEXT_DATA__` (Next.js SSR)
- **Platform**: Apify Actor SDK 2.0+
- **No browser**: Pure HTTP for maximum speed

## 🌐 Data Source

All data is scraped from publicly available job listings on Cutshort.io. Respect the platform's terms of service and use responsibly.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/roshtarg-cpu/cutshort-scraper/issues)
- **Apify Store**: [Actor Page](https://apify.com/fervent_bus/cutshort-scraper)

## 🏷️ Tags

`jobs` `cutshort` `india` `tech-jobs` `job-board` `python` `ai-agents` `claude` `chatgpt` `mcp` `lead-generation` `recruitment`
