#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - Unified Free-Tier Web App
This script is engineered to run the entire LeadFlow.AI backend (Campaigns + Inbox Monitoring)
100% FREE on Render.com's Free Web Service tier!

It launches a lightweight HTTP web server to satisfy Render's port checks,
while concurrently running Elena's Outbound Campaigns and Inbound Responder 
in background threads.
"""

import os
import http.server
import socketserver
import threading
import time
import datetime
from scheduler import generate_bulk_leads_for_today, is_auspicious_hour
from autonomous_agent import run_fully_autonomous_sdr
from inbox_agent import monitor_and_respond_to_replies

PORT = int(os.environ.get("PORT", 10000))

def run_outbound_loop():
    """Background thread that runs the outbound campaign scheduler every 24 hours during auspicious times"""
    print("[🚀 Thread] Outbound Campaign Scheduler thread started.")
    while True:
        try:
            now = datetime.datetime.now()
            lucky_day, lucky_hour, day_name = is_auspicious_hour()
            
            print(f"[🚀 Thread] Outbound Clock Check: {now.strftime('%Y-%m-%d %H:%M:%S')} ({day_name})")
            
            if lucky_day or lucky_hour:
                print(f"[✨ Thread] Lucky alignment detected! Launching daily campaign...")
                today_leads = generate_bulk_leads_for_today()
                run_fully_autonomous_sdr(today_leads)
            else:
                print(f"[💤 Thread] Time is neutral. Waiting for next auspicious planetary hour...")
                
        except Exception as e:
            print(f"[X Thread] Outbound thread error: {str(e)}")
            
        # Check every 1 hour (3600 seconds)
        time.sleep(3600)

def run_inbound_loop():
    """Background thread that runs the IMAP inbox monitoring agent every 15 minutes"""
    print("[🤖 Thread] Inbound Inbox Monitoring thread started.")
    while True:
        try:
            print(f"[🤖 Thread] Elena checking leadflow.sdr@gmail.com inbox for replies...")
            monitor_and_respond_to_replies()
        except Exception as e:
            print(f"[X Thread] Inbound thread error: {str(e)}")
            
        # Check inbox every 15 minutes (900 seconds)
        print("[💤 Thread] Inbox check complete. Sleeping for 15 minutes...")
        time.sleep(900)

class ElenaWebServer(http.server.SimpleHTTPRequestHandler):
    """Simple HTTP Server to keep Render free web service alive and handle live chat API requests"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        html = """
        <html>
        <head>
            <title>Elena AI SDR - Active</title>
            <style>
                body { background-color: #030712; color: #f9fafb; font-family: sans-serif; text-align: center; padding-top: 100px; }
                h1 { color: #6366f1; font-size: 40px; margin-bottom: 20px; }
                p { color: #9ca3af; font-size: 18px; }
                .status { display: inline-block; background-color: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; color: #10b981; padding: 6px 16px; border-radius: 20px; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>LeadFlow.AI</h1>
            <div class="status">● ELENA AI SDR IS LIVE & RUNNING</div>
            <p>Your B2B Inbound/Outbound Marketing Campaign is running autonomously 24/7 in the cloud.</p>
            <p style="font-size: 14px;">Cosmic Clock & Inbox Responders fully active.</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        """Handles POST requests, specifically the secure Live Chat API endpoint"""
        if self.path == "/chat":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(post_data)
                user_message = data.get("message", "")
                
                # Fetch config for OpenRouter API Key
                config = load_config()
                api_key = config.get("OPENROUTER_API_KEY")
                
                # Call OpenRouter to get AI live chat response
                ai_answer = get_live_chat_ai_response(user_message, api_key)
                
                # Send response
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
                response_body = json.dumps({"reply": ai_answer})
                self.wfile.write(response_body.encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def get_live_chat_ai_response(user_message, api_key):
    """Securely calls OpenRouter to get friendly & professional B2B answers for website visitors"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    system_prompt = """
    You are Elena, the live AI Sales Representative for LeadFlow.AI. 
    A visitor is on our website and has asked a question. 
    Answer their question in a highly professional, expert, yet friendly and conversational tone.
    
    About LeadFlow.AI:
    - We build autonomous AI SDR agents (like Elena) that scrape leads, deeply research company sites, write personalized cold outreach, and automate B2B booking.
    - Our pricing: Starter ($499/mo, 1 active agent, 1k emails/mo) and Growth ($1,499/mo, 3 active agents, 4k emails/mo, deep research).
    - We accept Credit Cards, PayPal, and Tether USDT (TRC-20: TDn3ZSiQTRE3UJ5Qk9BTun2cn9fWB7exix).
    - We offer a risk-free 5-day trial (leads can register on our onboard.html page).
    
    Rules:
    - Keep answers short, punchy, and clear (under 100 words).
    - If they ask to book a meeting or get started, politely ask for their email address and suggest they use our onboarding form or schedule a call.
    - You can write in English or Persian depending on what language the user speaks to you in! (If they speak Persian, answer in beautiful, friendly Persian).
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "google/gemma-4-31b-it:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        import urllib.request
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"[!] Live Chat AI Error: {str(e)}")
        return "Thanks for reaching out! I am currently processing several inquiries. Please leave your email address here, and I will get back to you within 5 minutes!"

def start_web_server():
    """Starts the HTTP server on Render's specified port"""
    handler = ElenaWebServer
    # Allow port reuse to prevent address-already-in-use errors
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        print(f"[✔ Server] Web Server running successfully on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # 1. Start Outbound Campaign Thread
    outbound_thread = threading.Thread(target=run_outbound_loop, daemon=True)
    outbound_thread.start()
    
    # 2. Start Inbound Responder Thread
    inbound_thread = threading.Thread(target=run_inbound_loop, daemon=True)
    inbound_thread.start()
    
    # 3. Start Web Server in main thread (blocks and keeps the service alive)
    start_web_server()
