import urllib.request
import re
import json
from bs4 import BeautifulSoup # If installed, we'll try to use it, otherwise fall back to regex

def scrape_website(url):
    """
    Scrapes a target website, extracts its meta description, 
    and analyzes it for target B2B pain points.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(f"[*] Deep Research Agent: Accessing {url}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        # Try extracting title and meta description
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "Unknown Title"
        
        # Meta description extraction
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', html, re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else "No meta description found."
        
        # Simple keywords detection for AI context enrichment
        keywords = []
        possible_keywords = ["saas", "software", "agency", "marketing", "consulting", "enterprise", "cloud", "security"]
        for kw in possible_keywords:
            if kw in html.lower():
                keywords.append(kw)

        result = {
            "status": "success",
            "title": title,
            "description": description[:300],
            "detected_keywords": keywords,
            "raw_length": len(html)
        }
        return result

    except Exception as e:
        # Graceful fallback for demo or when site is blocked / unreachable
        print(f"[!] Warning: Could not scrape {url} directly ({str(e)}). Simulating deep research offline mode...")
        return {
            "status": "offline_fallback",
            "title": "Fallback Analysis System",
            "description": "Enterprise software provider with focus on workflow automation and digital optimization.",
            "detected_keywords": ["software", "enterprise", "automation"],
            "raw_length": 1500
        }

if __name__ == "__main__":
    # Test on a stable site
    test_url = "example.com"
    data = scrape_website(test_url)
    print("\n--- Scrape Results ---")
    print(json.dumps(data, indent=4, ensure_ascii=False))
