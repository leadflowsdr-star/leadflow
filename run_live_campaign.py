#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - Production Live Campaign Execution Engine
This script runs the actual, live, automated outbound campaign.
It reads leads with 'discovered' status from the leadflow.db database,
scrapes their websites, calls OpenRouter (Gemma 4 31B) to write custom pitches,
sends the real emails via leadflow.sdr@gmail.com, and logs the results.
"""

import sqlite3
import time
from autonomous_agent import run_fully_autonomous_sdr, load_config

DB_NAME = "leadflow.db"

def run_production_campaign(limit=10):
    print("========================================================")
    print("        🚀 LEADFLOW.AI - LIVE CAMPAIGN LAUNCH 🚀        ")
    print("========================================================")
    
    # 1. Fetch leads from database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, first_name, last_name, email, title, company, website, industry, buying_signal 
    FROM leads 
    WHERE status = 'discovered'
    LIMIT ?
    ''', (limit,))
    
    db_leads = cursor.fetchall()
    conn.close()
    
    if not db_leads:
        print("[!] No new 'discovered' leads found in the database. Please run 'lead_miner.py' to add more.")
        return
        
    print(f"[*] Found {len(db_leads)} new leads ready for autonomous outbound outreach.")
    print("--------------------------------------------------------")
    
    # Format database rows into structured dictionary list for our SDR agent
    target_leads = []
    for row in db_leads:
        target_leads.append({
            "db_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "email": row[3],
            "title": row[4],
            "company": row[5],
            "website": row[6],
            "industry": row[7],
            "signal": row[8]
        })
        
    # 2. Run the SDR Agent on these leads
    # This will scrape, call OpenRouter (Gemma-4-31B), and send actual emails!
    run_fully_autonomous_sdr(target_leads)
    
    # 3. Update status of processed leads in database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for lead in target_leads:
        cursor.execute('''
        UPDATE leads 
        SET status = 'sent' 
        WHERE id = ?
        ''', (lead['db_id'],))
        
    conn.commit()
    conn.close()
    
    print("\n========================================================")
    print("🎉 SUCCESS: Live outreach campaign complete!")
    print(f"All {len(target_leads)} leads have been successfully processed, pitched and updated to 'sent'.")
    print("========================================================")

if __name__ == "__main__":
    run_production_campaign(limit=10)
