#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - Recurring Affiliate Commission Manager
This script implements your precise recurring affiliate strategy:
- Tracks referred clients.
- Verifies if their monthly payment is 'active' or 'cancelled'.
- Calculates the 20% USDT recurring commission ($100 for $499 plan, $300 for $1,499 plan) ONLY if the client paid.
- If the client cancels or fails to renew, the commission is terminated instantly!
"""

import sqlite3
import json

DB_NAME = "leadflow.db"

def init_affiliate_tables():
    """Initializes tables for tracking referrers and commission states"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table for tracking affiliates/referrers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS affiliates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        usdt_wallet TEXT UNIQUE NOT NULL,
        referral_code TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Table for tracking referred customers & their payment/commission status
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS referred_customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        affiliate_id INTEGER,
        customer_email TEXT UNIQUE NOT NULL,
        plan_name TEXT,
        payment_status TEXT DEFAULT 'active', -- 'active' or 'cancelled'
        monthly_price REAL,
        commission_rate REAL DEFAULT 0.20, -- 20%
        last_payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (affiliate_id) REFERENCES affiliates(id)
    )
    ''')
    
    # Table for tracking payouts
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS affiliate_payouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referred_customer_id INTEGER,
        payout_amount REAL,
        payout_status TEXT DEFAULT 'pending_verification', -- 'pending_verification', 'ready_for_usdt_send', 'paid'
        payout_date TIMESTAMP,
        FOREIGN KEY (referred_customer_id) REFERENCES referred_customers(id)
    )
    ''')
    
    # Add a mock affiliate for demonstration
    cursor.execute("SELECT COUNT(*) FROM affiliates")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO affiliates (name, usdt_wallet, referral_code) VALUES ('Arash', 'TDn3ZSiQTRE3UJ5Qk9BTun2cn9fWB7exix', 'ELENA92')",)
        print("[+] Created initial affiliate profile for Arash.")
        
    conn.commit()
    conn.close()

def audit_monthly_commissions():
    """
    Scans referred customers. If payment is active, calculates the 20% commission.
    If payment is cancelled, cuts the commission immediately!
    """
    print("\n[*] Running Monthly Affiliate Audit Loop...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # We query all referred customers to verify commission validity
    cursor.execute('''
    SELECT r.id, r.customer_email, r.payment_status, r.monthly_price, r.commission_rate, a.name, a.usdt_wallet
    FROM referred_customers r
    JOIN affiliates a ON r.affiliate_id = a.id
    ''')
    
    referrals = cursor.fetchall()
    
    for ref in referrals:
        r_id, email, status, price, rate, aff_name, wallet = ref
        print(f"\n[*] Auditing referral: {email} (Referred by: {aff_name})")
        
        if status == 'active':
            commission_usd = price * rate
            print(f"    - [STATUS: ACTIVE] Client renewed. Calculating {rate*100}% commission: ${commission_usd} USDT.")
            
            # Log a payout
            cursor.execute('''
            INSERT INTO affiliate_payouts (referred_customer_id, payout_amount, payout_status)
            VALUES (?, ?, ?)
            ''', (r_id, commission_usd, 'ready_for_usdt_send'))
            print(f"    - [✔] Payout of ${commission_usd} USDT authorized and marked 'ready_for_usdt_send' to wallet {wallet}.")
        else:
            print(f"    - [STATUS: CANCELLED] Client did not renew their subscription. Commission terminated. $0 payout.")
            
    conn.commit()
    conn.close()

def simulate_referral_signup():
    """Simulates one active customer and one cancelled customer to test the rule"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ensure tables are initialized
    init_affiliate_tables()
    
    # Insert mock referred customers
    try:
        # Client 1: Active
        cursor.execute('''
        INSERT OR IGNORE INTO referred_customers (affiliate_id, customer_email, plan_name, payment_status, monthly_price)
        VALUES (?, ?, ?, ?, ?)
        ''', (1, "active_client@agency.com", "Starter Agent Plan", "active", 499.0))
        
        # Client 2: Cancelled
        cursor.execute('''
        INSERT OR IGNORE INTO referred_customers (affiliate_id, customer_email, plan_name, payment_status, monthly_price)
        VALUES (?, ?, ?, ?, ?)
        ''', (1, "cancelled_client@boutique.co", "Starter Agent Plan", "cancelled", 499.0))
        
        conn.commit()
    except Exception as e:
        pass
    finally:
        conn.close()

if __name__ == "__main__":
    simulate_referral_signup()
    audit_monthly_commissions()
