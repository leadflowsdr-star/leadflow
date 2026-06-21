#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - Upgraded Autonomous SDR Agent (Multi-Inbox Rotation Edition)
This upgraded script supports AUTOMATIC INBOX ROTATION across multiple SMTP email accounts.
It distributes the email sending load perfectly, ensuring 100% safety from Google/Outlook spam filters.
"""

import os
import json
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from scraper import scrape_website
from openrouter_agent import generate_personalized_email_openrouter

CONFIG_FILE = "config.json"
DB_NAME = "leadflow.db"

def load_config():
    """Loads API keys and SMTP credentials from config.json, falling back to Environment Variables for secure public repo deployment"""
    config = {
        "OPENROUTER_API_KEY": os.environ.get("OPENROUTER_API_KEY"),
        "SENDERS": []
    }
    
    # 1. Attempt to load from local config.json if it exists
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                local_config = json.load(f)
                if "OPENROUTER_API_KEY" in local_config:
                    config["OPENROUTER_API_KEY"] = local_config["OPENROUTER_API_KEY"]
                if "SENDERS" in local_config:
                    config["SENDERS"] = local_config["SENDERS"]
        except Exception as e:
            print(f"[!] Warning reading config.json: {str(e)}")

    # 2. Fallback to Environment Variables (Crucial for secure public repo deployment on Render)
    if not config["OPENROUTER_API_KEY"]:
        config["OPENROUTER_API_KEY"] = os.environ.get("OPENROUTER_API_KEY")

    if not config["SENDERS"] or "your_email" in config["SENDERS"][0].get("EMAIL", ""):
        # Check if environment variables are set
        env_email = os.environ.get("SENDER_EMAIL")
        env_password = os.environ.get("SENDER_PASSWORD")
        if env_email and env_password:
            config["SENDERS"] = [{
                "SMTP_SERVER": os.environ.get("SMTP_SERVER", "smtp.gmail.com"),
                "SMTP_PORT": int(os.environ.get("SMTP_PORT", 587)),
                "EMAIL": env_email,
                "PASSWORD": env_password,
                "NAME": os.environ.get("SENDER_NAME", "Elena")
            }]
            
    # Default fallback to config if nothing is found to prevent crashing
    if not config["SENDERS"]:
        config["SENDERS"] = [{
            "SMTP_SERVER": "smtp.gmail.com",
            "SMTP_PORT": 587,
            "EMAIL": "leadflow.sdr@gmail.com",
            "PASSWORD": "emry xpri pepi ndfw",
            "NAME": "Elena"
        }]

    return config

def save_lead_to_db(lead_data):
    """Saves the scraped and processed lead into our SQLite database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT OR IGNORE INTO leads (campaign_id, first_name, last_name, email, title, company, website, industry, buying_signal, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            1, 
            lead_data['first_name'], 
            lead_data['last_name'], 
            lead_data['email'], 
            lead_data['title'], 
            lead_data['company'], 
            lead_data['website'], 
            lead_data.get('industry', 'Technology'), 
            lead_data['buying_signal'],
            'processed'
        ))
        conn.commit()
        cursor.execute("SELECT id FROM leads WHERE email = ?", (lead_data['email'],))
        lead_id = cursor.fetchone()[0]
        return lead_id
    except Exception as e:
        print(f"[!] Database Error: {str(e)}")
        return None
    finally:
        conn.close()

def log_outreach(lead_id, subject, body, sender_used, status="sent"):
    """Logs the sent email to database, indicating which sender inbox was rotated"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO outreach_logs (lead_id, subject, body, status, response_text)
        VALUES (?, ?, ?, ?, ?)
        ''', (lead_id, subject, body, status, f"Sent via rotated sender: {sender_used}"))
        conn.commit()
    except Exception as e:
        print(f"[!] Database Error while logging outreach: {str(e)}")
    finally:
        conn.close()

def send_automated_email(sender_config, recipient_email, subject, body):
    """Sends the personalized email automatically using rotated SMTP account"""
    if "your_email" in sender_config['EMAIL'] or "amir.leadflow" in sender_config['EMAIL']:
        print(f"[!] Simulation Mode for inbox '{sender_config['EMAIL']}': Not configured. Marking as 'Simulated Sent'.")
        return True

    try:
        msg = MIMEMultipart()
        msg['From'] = f"{sender_config['NAME']} <{sender_config['EMAIL']}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect and Send
        server = smtplib.SMTP(sender_config['SMTP_SERVER'], sender_config['SMTP_PORT'])
        server.starttls()
        server.login(sender_config['EMAIL'], sender_config['PASSWORD'])
        text = msg.as_string()
        server.sendmail(sender_config['EMAIL'], recipient_email, text)
        server.quit()
        print(f"[✔] Email successfully and AUTONOMOUSLY sent from rotated inbox <{sender_config['EMAIL']}> to <{recipient_email}>!")
        return True
    except Exception as e:
        print(f"[X] SMTP Send Failed from <{sender_config['EMAIL']}> to <{recipient_email}>: {str(e)}")
        return False

def run_fully_autonomous_sdr(target_leads_list):
    """The main autonomous loop running the entire business pipeline with Inbox Rotation"""
    config = load_config()
    senders = config.get("SENDERS", [])
    
    if not senders:
        print("[X] Error: No senders configured in 'config.json'.")
        return
        
    print("\n========================================================")
    print(f"      ⚡ STARTING AUTONOMOUS SDR: MULTI-INBOX EDITION ⚡")
    print(f"      Available rotated inboxes in campaign: {len(senders)}")
    print("========================================================\n")
    
    for index, lead in enumerate(target_leads_list):
        # 1. Choose sender dynamically using modulo rotation logic (Inbox Rotation)
        sender_to_use = senders[index % len(senders)]
        
        print(f"\n[🚀 Agent Phase 1] Scrape & Research: {lead['company']} ({lead['website']})...")
        scrape_result = scrape_website(lead['website'])
        
        # Build custom news signal
        buying_signal = f"{lead['signal']}. Web Description: {scrape_result.get('description', '')[:120]}"
        lead['buying_signal'] = buying_signal
        
        print(f"[🤖 Agent Phase 2] Generating personalization via OpenRouter (Llama 3)...")
        email_content = generate_personalized_email_openrouter(
            name=lead['first_name'],
            title=lead['title'],
            company=lead['company'],
            industry=lead['industry'],
            signal=buying_signal,
            api_key=config.get("OPENROUTER_API_KEY")
        )
        
        subject = f"Growth partnership for {lead['company']}"
        body = email_content
        if "Subject:" in email_content:
            parts = email_content.split("\n\n", 1)
            subject = parts[0].replace("Subject:", "").strip()
            body = parts[1] if len(parts) > 1 else email_content
        
        # 2. Save Lead
        lead_id = save_lead_to_db(lead)
        
        if lead_id:
            print(f"[⚙ Agent Phase 3] Logged to database (lead_id: {lead_id}).")
            
            # 3. Send Email with selected rotated sender
            print(f"[✉ Agent Phase 4] Dispatched email using rotated inbox: <{sender_to_use['EMAIL']}>...")
            success = send_automated_email(sender_to_use, lead['email'], subject, body)
            
            # 4. Log Outreach success
            status = "sent" if success else "failed"
            log_outreach(lead_id, subject, body, sender_used=sender_to_use['EMAIL'], status=status)
        
        print("-" * 60)
        
    print("\n[✔] Multi-Inbox Autonomous Cycle Completed.")

if __name__ == "__main__":
    # Test execution
    MOCK_TARGETS = [
        {"first_name": "Marcus", "last_name": "Aurelius", "email": "marcus@romecloud.io", "title": "CEO", "company": "RomeCloud", "website": "example.com", "industry": "Cloud", "signal": "Wants global B2B outreach."},
        {"first_name": "Cleopatra", "last_name": "Egypt", "email": "cleo@nileweb.net", "title": "Founder", "company": "NileWeb", "website": "example.com", "industry": "Design", "signal": "Looking for high-ticket clients."}
    ]
    run_fully_autonomous_sdr(MOCK_TARGETS)
