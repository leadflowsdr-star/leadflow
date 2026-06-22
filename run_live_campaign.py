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
    print("[⚠️ OUTBOUND PAUSED] Outbound email sending has been PAUSED by the Owner until further notice.")
    print("Zero emails will be dispatched. Elena is standing by.")
    print("========================================================")
    return

if __name__ == "__main__":
    run_production_campaign(limit=10)
