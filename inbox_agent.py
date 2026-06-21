#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - Autonomous Inbox Agent (IMAP Responder Edition)
This script allows Elena to monitor your leadflow.sdr@gmail.com inbox, 
automatically download replies, analyze their sentiment with AI (Gemma 4 31B),
and AUTONOMOUSLY send high-converting replies or book meetings without you doing anything!
"""

import imaplib
import email
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openrouter_agent import generate_personalized_email_openrouter

CONFIG_FILE = "config.json"

def monitor_and_respond_to_replies():
    print("========================================================")
    print("       ⚡ ELENA INBOX AGENT - AUTONOMOUS RESPONDER ⚡     ")
    print("========================================================")
    
    # 1. Load config
    if not os.path.exists(CONFIG_FILE):
        print("[X] Error: config.json not found.")
        return
        
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
        
    sender = config["SENDERS"][0]
    email_addr = sender["EMAIL"]
    password = sender["PASSWORD"]
    
    # Check if credentials are default
    if "your_email" in email_addr or "app_password" in password:
        print("[!] Simulation Mode: Active. Real credentials not set.")
        simulate_incoming_reply()
        return

    print(f"[*] Accessing Gmail inbox for <{email_addr}> via secure IMAP...")
    
    try:
        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_addr, password)
        mail.select("inbox")
        
        # Search for unread emails from prospects (excluding ourselves)
        # Search criteria: UNSEEN
        status, response = mail.search(None, 'UNSEEN')
        mail_ids = response[0].split()
        
        print(f"[+] Connected! Found {len(mail_ids)} new unread emails.")
        
        for m_id in mail_ids:
            status, data = mail.fetch(m_id, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            
            # Extract sender and body
            prospect_email = email.utils.parseaddr(msg['From'])[1]
            subject = msg['Subject']
            
            # Ignore auto-replies or emails from ourselves
            if prospect_email.lower() == email_addr.lower() or "no-reply" in prospect_email.lower():
                continue
                
            print(f"\n[*] Processing unread reply from: {prospect_email}")
            print(f"[*] Subject: {subject}")
            
            # Extract email body text
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                
            print(f"[*] Message content: \"{body[:120].strip()}...\"")
            
            # 2. Analyze sentiment and generate reply via OpenRouter AI
            print("[🤖] Analyzing prospect intent with Gemma 4 31B...")
            ai_reply = generate_ai_response_handling(prospect_email, body, config.get("OPENROUTER_API_KEY"))
            
            # 3. Automatically send the response via SMTP
            if ai_reply:
                print(f"[✉] Autonomously replying to <{prospect_email}>...")
                send_autonomous_smtp_reply(sender, prospect_email, f"Re: {subject}", ai_reply)
                
                # Mark email as read/seen in Gmail
                mail.store(m_id, '+FLAGS', '\\Seen')
                
        mail.logout()
        print("\n[✔] Inbox scan complete. Elena is resting.")
        
    except Exception as e:
        print(f"[X] IMAP Inbox Monitor Failed: {str(e)}")
        print("[!] Attempting offline simulation fallback...")
        simulate_incoming_reply()

def generate_ai_response_handling(prospect_email, reply_body, api_key):
    """Uses OpenRouter AI to analyze the incoming reply and draft the perfect response"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    prompt = f"""
    You are Elena, an autonomous AI SDR for LeadFlow.AI.
    A prospective client just responded to our cold outreach email.
    
    Prospect Email: {prospect_email}
    Their Response: "{reply_body}"
    
    Analyze their response:
    1. If they are INTERESTED or asking for a meeting:
       Draft a warm, polite reply. Share our Calendly booking link: "https://calendly.com/leadflow-elena/15min" to schedule a 15-minute Google Meet call.
    2. If they have an OBJECTION (e.g. "We don't have budget", "How does it work?"):
       Politely handle the objection. Explain that we have a 100% free pilot to prove results.
    3. If they want to UNSUBSCRIBE (e.g. "Stop emailing me", "Not interested"):
       Write: "UNSUBSCRIBE" on the first line, then a polite one-line confirmation: "Got it, I will remove you from our list. Have a great day!"
       
    Write only your actual reply to the prospect. Keep it short (under 80 words) and professional.
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
        import urllib.request
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"[!] AI Response Generation failed: {str(e)}")
        return None

def send_autonomous_smtp_reply(sender_config, recipient_email, subject, body):
    """Sends the drafted reply directly to the client"""
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{sender_config['NAME']} <{sender_config['EMAIL']}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(sender_config['SMTP_SERVER'], sender_config['SMTP_PORT'])
        server.starttls()
        server.login(sender_config['EMAIL'], sender_config['PASSWORD'])
        server.sendmail(sender_config['EMAIL'], recipient_email, msg.as_string())
        server.quit()
        print(f"[✔] Autonomous reply successfully delivered to <{recipient_email}>!")
    except Exception as e:
        print(f"[X] Failed to send SMTP reply: {str(e)}")

def simulate_incoming_reply():
    """Simulates how the inbox agent handles an incoming positive response"""
    print("\n[--- RUNNING INBOX AGENT SIMULATION ---]")
    mock_reply = "Hey Elena, I saw your email regarding Ignite Visibility. Outbound lead gen is a bottleneck for us. Do you have a booking link so we can schedule a call?"
    print(f"[*] Simulated Reply Received: \"{mock_reply}\"")
    print("[🤖] Elena's AI brain: Detecting intent... [Intent: MEETING_REQUESTED]")
    print("[✉] Elena's AI brain: Drafting response autonomously...")
    
    mock_draft = """Hi John,

Thanks for the quick reply! I'd love to show you how we automate this.

You can easily pick a time that works best for you on my calendar here:
👉 https://calendly.com/leadflow-elena/15min

Looking forward to our chat and helping Ignite Visibility scale!

Best,
Elena
LeadFlow.AI"""
    
    print("\n[✔] Elena's Autonomous Response Ready:")
    print(mock_draft)
    print("========================================================\n")

if __name__ == "__main__":
    monitor_and_respond_to_replies()
