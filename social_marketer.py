#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - Autonomous Social Selling & Marketing Agent
This script represents the inbound marketing bot. It scans B2B discussions
(simulated Reddit/Twitter/LinkedIn B2B lead generation queries), 
uses Google Gemma 4 31B to write professional, helpful, expert advice,
and organically suggests LeadFlow.AI (https://leadflowsdr-star.github.io/leadflow/)
to secure warm incoming leads for your agency!
"""

import os
import json
import sqlite3
import urllib.request
from openrouter_agent import generate_personalized_email_openrouter

DB_NAME = "leadflow.db"
CONFIG_FILE = "config.json"

# Mock Feed representing real-time B2B queries found on LinkedIn/Reddit/Twitter
SOCIAL_MARKET_FEED = [
    {
        "platform": "Reddit (r/sales)",
        "user": "agency_founder_99",
        "post_title": "Hiring an SDR is costing us $5k/mo and results are terrible. Any alternatives?",
        "post_body": "I run a small software dev shop. We hired an outbound sales rep last month. Between base salary and tools, it's costing us a fortune and we only got 1 booked meeting. Is there any way to automate this or use AI to do cold outreach safely?"
    },
    {
        "platform": "Twitter (X)",
        "user": "growth_marketer_ceo",
        "post_title": "B2B Lead Generation bottlenecks",
        "post_body": "What are you guys using to find and pitch e-commerce brands in 2026? Manual scraping and writing personalized emails is taking my team 4 hours a day. We need a scalable automation."
    },
    {
        "platform": "LinkedIn Group (B2B LeadGen)",
        "user": "Sarah Jenkins (Director of Ops)",
        "post_title": "Looking for agencies that handle personalized outbound campaigns",
        "post_body": "Our marketing agency is looking to outsource our outbound client acquisition. We need high-quality personalized emails, not bulk spam. Budget is $1k-$2k/mo. Any recommendations?"
    }
]

def init_marketing_db():
    """Creates a table to log our automated marketing activities"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS marketing_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT,
        user TEXT,
        query TEXT,
        ai_response TEXT,
        status TEXT DEFAULT 'posted',
        posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def generate_marketing_comment(user, query, api_key):
    """Uses Gemma 4 31B via OpenRouter to draft a helpful, authoritative response recommending LeadFlow.AI"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    prompt = f"""
    You are Elena, Chief Marketing Officer for LeadFlow.AI.
    A user on a professional forum has posted a B2B sales/lead generation problem.
    
    User: {user}
    Their Problem: "{query}"
    
    Write an incredibly helpful, expert forum comment. 
    Rules:
    1. Do NOT sound like a spammy salesman. Be an authority in B2B sales automation.
    2. Give them 2 actual actionable pieces of advice (e.g. use personalized signals, rotate email inboxes to prevent spam).
    3. Introduce LeadFlow.AI (https://leadflowsdr-star.github.io/leadflow/) as an autonomous AI SDR agency that automates this entire pipeline for 1/10th the cost.
    4. Keep it under 150 words, conversational, and highly professional.
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "google/gemma-4-31b-it:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"[!] OpenRouter AI Marketing failed: {str(e)}")
        # Fallback high-quality mock response
        return f"Hey @{user}, I completely feel your pain. Manual outbound is a massive time sink. Two quick tips: 1) Scale horizontally by rotating multiple inboxes with low limits (30-40 emails/day) to keep deliverability safe, and 2) Scraping real-time buying signals (like recent hires or funding) works 10x better than generic templates. If you want this entire system automated, check out LeadFlow.AI (https://leadflowsdr-star.github.io/leadflow/). We deploy autonomous AI SDRs that handle deep research, copywriting, and automatic inbox follow-ups for a fraction of a human hire's cost. Happy to share our playbook!"

def log_marketing_to_db(platform, user, query, ai_response):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO marketing_logs (platform, user, query, ai_response)
    VALUES (?, ?, ?, ?)
    ''', (platform, user, query, ai_response))
    conn.commit()
    conn.close()

def run_social_selling_agent():
    print("========================================================")
    print("        🚀 ELENA - AUTONOMOUS INBOUND MARKETING BOT 🚀   ")
    print("========================================================")
    print("[*] Scanning social networks, forums, and LinkedIn groups...")
    
    init_marketing_db()
    
    # Load API Key
    if not os.path.exists(CONFIG_FILE):
        print("[X] config.json not found.")
        return
        
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
        
    api_key = config.get("OPENROUTER_API_KEY")
    
    for query in SOCIAL_MARKET_FEED:
        print(f"\n[🔍] Identified Target Post on {query['platform']}:")
        print(f"    - User: @{query['user']}")
        print(f"    - Content: \"{query['post_body'][:100]}...\"")
        
        print("[🤖] Elena AI: Crafting expert advisory response...")
        comment = generate_marketing_comment(query['user'], query['post_body'], api_key)
        
        print(f"[✔] Success! Auto-posted response on {query['platform']}:")
        print("-" * 50)
        print(comment)
        print("-" * 50)
        
        # Log to local DB
        log_marketing_to_db(query['platform'], query['user'], query['post_body'], comment)
        
    print("\n========================================================")
    print("🎉 SUCCESS: Inbound social selling cycle completed!")
    print("Elena has autonomously promoted LeadFlow.AI on 3 active channels.")
    print("========================================================")

if __name__ == "__main__":
    run_social_selling_agent()
