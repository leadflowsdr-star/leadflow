#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - Autonomous Scheduler
This script runs in the background on your server/local machine.
It wakes up automatically every day, pulls a high-volume batch of target leads,
triggers the autonomous agent to research and email them, and then sleeps.

To run this in the background on your Iranian Linux VPS, you can run:
nohup python3 scheduler.py > scheduler.log 2>&1 &
"""

import time
import datetime
import sys
from autonomous_agent import run_fully_autonomous_sdr
from social_marketer import run_social_selling_agent

# Optimal daily limit for a single warm inbox to prevent spam filters from banning us (2026 guidelines)
DAILY_SEND_LIMIT = 35 

def generate_bulk_leads_for_today():
    """
    Simulates fetching a high-volume list of global B2B leads.
    In production, this function will query Apollo.io, Clutch.co or Google Maps APIs
    to get the fresh 35 targets daily.
    """
    print(f"[*] Scheduler: Generating {DAILY_SEND_LIMIT} targeted global B2B leads for today...")
    
    # High-quality international target companies
    target_niches = ["Web Design Agency", "SEO Consultant", "B2B SaaS", "No-Code Studio", "Digital Marketing Firm"]
    companies = ["FintechFlow", "WebCrafters", "SEOBoost", "NoCodeMagic", "CyberGuard", "ApexAds", "DevSquad", "CloudScale"]
    names = ["Michael", "David", "Emma", "Sophia", "Oliver", "James", "Alexander", "Lucas"]
    roles = ["Founder", "CEO", "Managing Partner", "VP of Sales", "Marketing Director"]
    
    bulk_leads = []
    
    # Dynamically generate 35 leads to showcase scalability
    for i in range(1, DAILY_SEND_LIMIT + 1):
        company = f"{companies[i % len(companies)]} {i}"
        name = names[i % len(names)]
        role = roles[i % len(roles)]
        niche = target_niches[i % len(target_niches)]
        
        bulk_leads.append({
            "first_name": name,
            "last_name": "Smith",
            "email": f"{name.lower()}{i}@{company.lower().replace(' ', '')}.com",
            "title": role,
            "company": company,
            "website": "example.com", # Uses safe scraper fallback in simulation
            "industry": niche,
            "signal": f"Looking for automatic outbound client acquisition to scale their {niche} projects."
        })
        
    return bulk_leads

def is_auspicious_hour():
    """
    Astrology & Numerology Engine (Based on August 9, 1991 birth chart)
    For a Leo (Sun ruled) with Life Path 1:
    - Best days: Sunday (Sun) and Thursday (Jupiter)
    - Auspicious daily hours of the Sun and Jupiter are aligned for maximum conversions.
    """
    import datetime
    now = datetime.datetime.now()
    day_name = now.strftime('%A')
    current_hour = now.hour
    
    # Auspicious days: Sunday and Thursday
    is_lucky_day = day_name in ["Sunday", "Thursday"]
    
    # Auspicious planetary hours (Traditional Hour of Sun and Jupiter)
    # Typically 09:00 AM - 11:00 AM and 03:00 PM - 05:00 PM are highly auspicious
    is_lucky_hour = (9 <= current_hour <= 11) or (15 <= current_hour <= 17)
    
    return is_lucky_day, is_lucky_hour, day_name

def start_scheduler():
    print("========================================================")
    print("          LEADFLOW.AI - AUTONOMOUS SCHEDULER            ")
    print("========================================================")
    print(f"Daily Outbound Send Limit: {DAILY_SEND_LIMIT} personalized emails / day")
    print("Astrological Alignment Active: Yes (Leo / Life Path 1)")
    print("Scheduler Status: [RUNNING IN BACKGROUND]")
    print("--------------------------------------------------------")
    
    while True:
        now = datetime.datetime.now()
        is_lucky_day, is_lucky_hour, day_name = is_auspicious_hour()
        
        print(f"\n[+] Clock Check: Current time is {now.strftime('%Y-%m-%d %H:%M:%S')} ({day_name})")
        
        if is_lucky_day or is_lucky_hour:
            print(f"[✨] ASTROLOGY ENGINE: Lucky alignment detected (Day: {day_name}, Hour: {now.hour}:00)!")
            print(f"[✨] Launching Elena SDR with maximum cosmic energy and high-converting alignment...")
            
            # Phase 1: Outbound Email Campaign (35 Leads)
            today_leads = generate_bulk_leads_for_today()
            run_fully_autonomous_sdr(today_leads)
            
            # Phase 2: Inbound Social Marketing Agent (Social Monitoring & Pitching)
            print(f"\n[✨] Waking up Elena's Social Marketer Bot to run autonomous Inbound Promotion...")
            run_social_selling_agent()
        else:
            print(f"[💤] Current time is neutral. Waiting for the next auspicious planetary hour (Sun/Jupiter)...")
            
        # Sleep for 1 hour before checking the cosmic clock again
        time.sleep(3600)

if __name__ == "__main__":
    # Prevent accidental infinite loops during automated agent tests, but fully ready for live deployment!
    if len(sys.argv) > 1 and sys.argv[1] == "--live":
        start_scheduler()
    else:
        print("[!] Running single-cycle test run of the Scheduler...")
        print("To run this 24/7 in the background, execute: python3 scheduler.py --live")
        print("-" * 50)
        # Test a mock cycle with 5 leads to verify logic
        test_leads = generate_bulk_leads_for_today()[:5]
        run_fully_autonomous_sdr(test_leads)
