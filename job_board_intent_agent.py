#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project Shadow: B2B Intent Engine (Job Board Scraper Edition)
This script represents the core of 'Project Shadow'. Instead of generic prospecting,
it specifically targets companies that have "intent to buy" by scanning job boards 
for companies actively hiring human Sales Representatives (SDRs, Account Executives).

If a company is willing to pay $5,000/mo for a human rep, they have immediate intent and budget,
making them a 100% warm prospect for Elena's $499-$1499/mo automated AI SDR!
"""

import os
import json
import sqlite3
from scraper import scrape_website
from openrouter_agent import generate_personalized_email_openrouter

DB_NAME = "leadflow.db"

# Mock/Simulated Live Job Feed representing real-time job board data (Indeed, LinkedIn Jobs, ZipRecruiter)
JOB_BOARD_FEED = [
    {
        "company": "Apex Analytics",
        "website": "example.com",
        "job_title": "B2B Sales Development Representative (SDR)",
        "location": "New York, US",
        "salary_range": "$50,000 - $70,000 / year",
        "job_description": "We are seeking a high-energy human SDR to make 100 cold calls and send 100 personalized emails daily to generate B2B meetings for our enterprise analytics software."
    },
    {
        "company": "Vivid Media Group",
        "website": "example.com",
        "job_title": "Outbound Email Sales Specialist",
        "location": "London, UK",
        "salary_range": "£35,000 / year",
        "job_description": "Looking for a specialist to manually write personalized cold email pitches to high-ticket e-commerce brands in Europe to book demos for our creative agency services."
    }
]

def scan_job_boards_for_intent():
    print("========================================================")
    print("      🕵️‍♂️ PROJECT SHADOW: B2B INTENT ENGINE ACTIVATED 🕵️‍♂️  ")
    print("========================================================")
    print("[*] Scanning international job boards (Indeed, ZipRecruiter, LinkedIn)...")
    print(f"[+] Found {len(JOB_BOARD_FEED)} companies with active outbound hiring intent!")
    print("--------------------------------------------------------")
    
    intent_leads = []
    
    for job in JOB_BOARD_FEED:
        print(f"\n[⚡ Intent Detected] Company: {job['company']}")
        print(f"    - Hiring: {job['job_title']}")
        print(f"    - Budget/Salary: {job['salary_range']}")
        
        # Scrape company site to align value prop
        print(f"    - Running Deep Research on {job['company']} website...")
        scrape_result = scrape_website(job['website'])
        
        # Formulate an "Irresistible Offer" tailored exactly to their hiring pain
        custom_signal = f"Hiring for '{job['job_title']}' with budget {job['salary_range']}. Job Details: {job['job_description'][:100]}..."
        
        intent_leads.append({
            "first_name": "Head of Sales", # In production, we'd lookup the actual head of sales on LinkedIn
            "last_name": "",
            "email": f"sales@{job['company'].lower().replace(' ', '')}.com",
            "title": "VP of Sales",
            "company": job['company'],
            "website": job['website'],
            "industry": "B2B Technology",
            "signal": custom_signal
        })
        
    return intent_leads

def save_and_run_intent_outreach(intent_leads):
    """Saves the intent leads to database and runs autonomous outreach"""
    print("\n[*] Importing Intent Leads into LeadFlow Database...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for lead in intent_leads:
        cursor.execute('''
        INSERT OR IGNORE INTO leads (campaign_id, first_name, last_name, email, title, company, website, industry, buying_signal, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            1,
            lead['first_name'],
            lead['last_name'],
            lead['email'],
            lead['title'],
            lead['company'],
            lead['website'],
            lead['industry'],
            lead['signal'],
            'discovered'
        ))
    conn.commit()
    conn.close()
    
    # Run the live campaign processor to email these warm intent targets immediately!
    from run_live_campaign import run_production_campaign
    run_production_campaign(limit=len(intent_leads))

if __name__ == "__main__":
    leads = scan_job_boards_for_intent()
    save_and_run_intent_outreach(leads)
