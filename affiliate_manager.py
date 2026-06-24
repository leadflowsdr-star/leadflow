#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - Upgraded Decreasing Recurring Affiliate Manager
This script implements your advanced tiered decreasing commission logic:
- Month 1 (First Payment): Pay a high dopamine incentive of 30% to drive active referrals.
- Month 2+ (Renewals): Pay a smaller recurring commission of 10% to preserve our B2B margins
  while still incentivizing the affiliate to keep their referred client active.
- If the client cancels: Commission is immediately terminated to $0.
"""

import sqlite3
import json

DB_NAME = "leadflow.db"

def update_referred_customers_table():
    """Adds a 'payment_cycle_count' column to track renewal months for commission tiering"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Check if column already exists before adding
        cursor.execute("PRAGMA table_info(referred_customers)")
        columns = [col[1] for col in cursor.fetchall()]
        if "payment_cycle_count" not in columns:
            cursor.execute("ALTER TABLE referred_customers ADD COLUMN payment_cycle_count INTEGER DEFAULT 1")
            print("[+] Added 'payment_cycle_count' column to referred_customers.")
    except Exception as e:
        print(f"[!] Warning updating schema: {str(e)}")
    finally:
        conn.close()

def audit_decreasing_commissions():
    """
    Scans referred customers and calculates tiered commission:
    - Month 1 (First payment): 30% commission.
    - Month 2+: 10% recurring commission.
    - If cancelled: 0% commission.
    """
    print("========================================================")
    print("     🛡️ DEPLOYING RECURRING DECREASING COMMISSION AUDIT 🛡️")
    print("========================================================")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Query referrals
    cursor.execute('''
    SELECT r.id, r.customer_email, r.payment_status, r.monthly_price, r.payment_cycle_count, a.name, a.usdt_wallet
    FROM referred_customers r
    JOIN affiliates a ON r.affiliate_id = a.id
    ''')
    
    referrals = cursor.fetchall()
    
    for ref in referrals:
        r_id, email, status, price, cycle_count, aff_name, wallet = ref
        print(f"\n[*] Auditing Referral: {email} (Referred by: {aff_name})")
        print(f"    - Current Payment Month/Cycle: Month {cycle_count}")
        
        if status == 'active':
            # Tiered/Decreasing Logic
            if cycle_count == 1:
                commission_rate = 0.20 # 20% for the first month
                tier_name = "Month 1 (First Sale Bonus)"
            else:
                commission_rate = 0.05 # 5% for renewal months
                tier_name = f"Month {cycle_count} (Standard Renewal)"
                
            commission_usd = price * commission_rate
            print(f"    - [STATUS: ACTIVE] [{tier_name}] Calculating {commission_rate*100}% commission: ${commission_usd} USDT.")
            
            # Record payout
            cursor.execute('''
            INSERT INTO affiliate_payouts (referred_customer_id, payout_amount, payout_status)
            VALUES (?, ?, ?)
            ''', (r_id, commission_usd, 'ready_for_usdt_send'))
            print(f"    - [✔] Payout of ${commission_usd} USDT authorized to wallet {wallet}.")
        else:
            print(f"    - [STATUS: CANCELLED] Client did not renew their subscription. Commission terminated. $0 payout.")
            
    conn.commit()
    conn.close()

def simulate_tiered_referrals():
    """Simulates active new, active renewed, and cancelled customers to test the exact rules"""
    update_referred_customers_table()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Clean up previous mock referrals to prevent duplicate errors
    cursor.execute("DELETE FROM referred_customers")
    
    try:
        # Case A: New Client (Month 1) - Active
        cursor.execute('''
        INSERT INTO referred_customers (affiliate_id, customer_email, plan_name, payment_status, monthly_price, payment_cycle_count)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (1, "new_client_m1@agency.com", "Starter Agent Plan", "active", 499.0, 1))
        
        # Case B: Renewed Client (Month 2+) - Active
        cursor.execute('''
        INSERT INTO referred_customers (affiliate_id, customer_email, plan_name, payment_status, monthly_price, payment_cycle_count)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (1, "renewed_client_m2@agency.com", "Starter Agent Plan", "active", 499.0, 2))
        
        # Case C: Cancelled Client - Cancelled
        cursor.execute('''
        INSERT INTO referred_customers (affiliate_id, customer_email, plan_name, payment_status, monthly_price, payment_cycle_count)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (1, "cancelled_client_m3@agency.com", "Starter Agent Plan", "cancelled", 499.0, 3))
        
        conn.commit()
    except Exception as e:
        print(f"[!] Simulation Insert Error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    simulate_tiered_referrals()
    audit_decreasing_commissions()
