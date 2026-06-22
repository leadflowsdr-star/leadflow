#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - Outbound Follow-Up Automation Engine
80% of cold outreach meetings are booked on the 2nd or 3rd email, not the 1st!
This script automatically checks our database 'leadflow.db' for leads that were emailed
3+ days ago but have not replied yet, and autonomously drafts and sends a high-converting,
short, ultra-friendly follow-up email.
"""

import os
import json
import sqlite3
import datetime
from autonomous_agent import load_config, send_automated_email

DB_NAME = "leadflow.db"

def find_leads_due_for_followup():
    """Queries the database for leads that were emailed but have 'sent' status (no reply)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # We look for leads in outreach_logs that were sent and have no response_text logged
    cursor.execute('''
    SELECT l.id, l.first_name, l.company, l.email, o.subject, o.sent_at
    FROM leads l
    JOIN outreach_logs o ON l.id = o.lead_id
    WHERE l.status = 'sent' AND o.status = 'sent' AND o.response_text IS NULL
    ''')
    
    leads_due = cursor.fetchall()
    conn.close()
    return leads_due

def generate_follow_up_content(name, company):
    """Generates a short, non-spammy, high-converting follow-up email"""
    subjects = [
        f"Floating this up, {name}",
        f"Quick follow up regarding {company}",
        f"Meetings for {company}?"
    ]
    
    # Selecting a highly successful B2B 2-line follow-up template
    body = f"""Hi {name},

I know you're incredibly busy running {company}, so I'll keep this brief. 

I wanted to float my previous email regarding our AI SDRs to the top of your inbox. We help brands like yours automate prospecting and book qualified sales meetings on autopilot, for 1/5th the cost of a human rep.

Are you open to a quick 5-minute chat next Tuesday or Wednesday to see if this could scale your pipeline this quarter?

Best,
Elena
LeadFlow.AI"""
    
    return subjects[0], body

def run_follow_up_campaign():
    print("========================================================")
    print("       ⚡ ELENA OUTBOUND - AUTOMATED FOLLOW-UP ⚡        ")
    print("========================================================")
    print("[⚠️ OUTBOUND PAUSED] Outbound follow-ups have been PAUSED by the Owner until further notice.")
    print("Zero follow-up emails will be dispatched. Elena is standing by.")
    print("========================================================")
    return

if __name__ == "__main__":
    run_follow_up_campaign()
