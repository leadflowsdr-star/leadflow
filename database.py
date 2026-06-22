import sqlite3
import os

DB_NAME = "leadflow.db"

def init_db():
    """Initializes the SQLite database with essential tables for LeadFlow.AI"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table for storing client campaigns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        target_icp TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Table for storing onboarded clients
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS onboarded_clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        website TEXT NOT NULL,
        value_prop TEXT,
        target_industry TEXT,
        target_title TEXT,
        target_geo TEXT,
        mailbox_preference TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Table for storing prospects/leads
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER,
        first_name TEXT NOT NULL,
        last_name TEXT,
        email TEXT UNIQUE,
        title TEXT,
        company TEXT,
        website TEXT,
        industry TEXT,
        buying_signal TEXT,
        enrichment_notes TEXT,
        sentiment TEXT DEFAULT 'none',
        status TEXT DEFAULT 'discovered',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
    )
    ''')

    # Table for storing sent emails and tracking
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS outreach_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER,
        subject TEXT,
        body TEXT,
        status TEXT DEFAULT 'sent',
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        response_text TEXT,
        responded_at TIMESTAMP,
        FOREIGN KEY (lead_id) REFERENCES leads(id)
    )
    ''')

    # Add a mock campaign if database is empty
    cursor.execute("SELECT COUNT(*) FROM campaigns")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO campaigns (name, target_icp) VALUES ('LeadFlow.AI Outreach Campaign', 'B2B SaaS Founders & Growth Directors')")
        print("[+] Created initial outbound campaign.")

    conn.commit()
    conn.close()
    print(f"[+] SQLite database '{DB_NAME}' initialized successfully with tables: campaigns, leads, outreach_logs.")

if __name__ == "__main__":
    init_db()
