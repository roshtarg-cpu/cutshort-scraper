"""Cutshort.io job scraper"""
import asyncio
import json
import re
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from urllib.parse import urljoin

import httpx
from apify import Actor
from bs4 import BeautifulSoup


async def fetch_page(url: str, proxy_url: Optional[str] = None) -> Optional[str]:
    """Fetch a page with optional proxy"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    client_kwargs = {
        'timeout': 30.0,
        'follow_redirects': True,
    }
    if proxy_url:
        client_kwargs['proxy'] = proxy_url
    
    async with httpx.AsyncClient(**client_kwargs) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            Actor.log.error(f'Failed to fetch {url}: {e}')
            return None


def extract_jobs_from_html(html: str) -> list[Dict[str, Any]]:
    """Extract job listings from __NEXT_DATA__ JSON in HTML"""
    try:
        # Find __NEXT_DATA__ script tag
        match = re.search(
            r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>',
            html,
            re.DOTALL
        )
        if not match:
            Actor.log.warning('No __NEXT_DATA__ found in HTML')
            return []
        
        data = json.loads(match.group(1))
        
        # Navigate to jobs array: queries[0].state.data.data.pageData.jobs
        queries = data.get('props', {}).get('pageProps', {}).get('dehydratedState', {}).get('queries', [])
        
        if queries:
            # Try the nested structure first
            state_data = queries[0].get('state', {}).get('data', {})
            if 'data' in state_data:
                inner_data = state_data['data']
                if 'pageData' in inner_data:
                    page_data = inner_data['pageData']
                    jobs = page_data.get('jobs', [])
                    if jobs:
                        Actor.log.info(f'Found {len(jobs)} jobs in pageData')
                        return jobs
            
            # Fallback: try direct jobs array
            for query in queries:
                state_data = query.get('state', {}).get('data', {})
                if isinstance(state_data, dict) and 'jobs' in state_data:
                    jobs = state_data.get('jobs', [])
                    if jobs:
                        Actor.log.info(f'Found {len(jobs)} jobs in direct state')
                        return jobs
        
        Actor.log.warning('No jobs array found in __NEXT_DATA__')
        return []
        
    except Exception as e:
        Actor.log.error(f'Error extracting jobs: {e}')
        return []


def parse_job(job_data: dict) -> dict:
    """Parse job data into clean output format"""
    try:
        # Extract basic fields
        result = {
            'scrapedAt': datetime.now(timezone.utc).isoformat(),
            'jobId': job_data.get('_id'),
            'title': job_data.get('headline'),
            'url': job_data.get('publicUrl'),
            'company': None,
            'companyAlias': None,
            'location': ', '.join(job_data.get('locations', [])) if job_data.get('locations') else None,
            'skills': ', '.join(job_data.get('allSkills', [])) if job_data.get('allSkills') else None,
            'experienceMin': None,
            'experienceMax': None,
            'salaryMin': None,
            'salaryMax': None,
            'salaryCurrency': None,
            'salaryText': job_data.get('salaryRangeText'),
            'remoteType': job_data.get('remoteType'),
            'jobType': ', '.join(job_data.get('roleTypes', [])) if job_data.get('roleTypes') else None,
            'description': job_data.get('sanitizedComment'),
            'hiringForClient': job_data.get('hiringForClient', False),
            'postedBy': None,
        }
        
        # Company details
        company_details = job_data.get('companyDetails', {})
        if company_details:
            result['company'] = company_details.get('name')
            result['companyAlias'] = company_details.get('alias')
        
        # Experience range
        exp_range = job_data.get('expRange', {})
        if exp_range:
            result['experienceMin'] = exp_range.get('min')
            result['experienceMax'] = exp_range.get('max')
        
        # Salary range
        salary_range = job_data.get('salaryRange', {})
        if salary_range:
            result['salaryMin'] = salary_range.get('min')
            result['salaryMax'] = salary_range.get('max')
            result['salaryCurrency'] = salary_range.get('currency')
        
        # Posted by
        created_by = job_data.get('createdBy', {})
        if created_by:
            result['postedBy'] = created_by.get('name')
        
        return result
        
    except Exception as e:
        Actor.log.error(f'Error parsing job: {e}')
        return {}


async def main():
    """Main actor entry point"""
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        max_results = actor_input.get('maxResults', 50)
        search_query = actor_input.get('searchQuery', 'python')
        location = actor_input.get('location', 'bangalore')
        
        # Build URL from search params
        # Cutshort URL format: /jobs/{query}-jobs-in-{location}
        query_slug = search_query.lower().replace(' ', '-')
        location_slug = location.lower().replace(' ', '-')
        start_url = f'https://cutshort.io/jobs/{query_slug}-jobs-in-{location_slug}'
        
        # Proxy configuration
        proxy_config = await Actor.create_proxy_configuration(
            actor_proxy_input=actor_input.get('proxyConfiguration')
        )
        proxy_url = await proxy_config.new_url() if proxy_config else None
        
        Actor.log.info(f'Starting scrape from: {start_url}')
        Actor.log.info(f'Max results: {max_results}')
        Actor.log.info(f'Using proxy: {bool(proxy_url)}')
        
        total_scraped = 0
        page = 1
        
        while total_scraped < max_results:
            # Build URL with pagination
            if '?' in start_url:
                url = f'{start_url}&page={page}'
            else:
                url = f'{start_url}?page={page}'
            
            Actor.log.info(f'Fetching page {page}: {url}')
            
            html = await fetch_page(url, proxy_url)
            if not html:
                Actor.log.error(f'Failed to fetch page {page}, stopping')
                break
            
            jobs = extract_jobs_from_html(html)
            if not jobs:
                Actor.log.info(f'No jobs found on page {page}, stopping')
                break
            
            Actor.log.info(f'Found {len(jobs)} jobs on page {page}')
            
            for job_data in jobs:
                if total_scraped >= max_results:
                    break
                
                parsed_job = parse_job(job_data)
                if parsed_job.get('jobId'):
                    await Actor.push_data(parsed_job)
                    total_scraped += 1
                    
                    if total_scraped % 10 == 0:
                        Actor.log.info(f'Progress: {total_scraped}/{max_results} jobs scraped')
            
            if total_scraped >= max_results:
                break
            
            page += 1
            await asyncio.sleep(1)  # Polite delay between pages
        
        Actor.log.info(f'Scraping complete. Total jobs scraped: {total_scraped}')
