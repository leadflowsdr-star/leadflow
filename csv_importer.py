#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - CSV Lead Importer
This tool allows you to upload any list of target leads (exported from Clutch.co, LinkedIn, or Apollo)
via a standard CSV file. The AI agents will automatically import them into the leadflow.db database
so they can be researched and emailed autonomously by the scheduler.
"""

import csv
import os
import sqlite3

DB_NAME = "leadflow.db"

def create_sample_csv():
    """Generates a sample template CSV file for the user to fill out"""
    sample_filename = "import_template.csv"
    headers = ["first_name", "last_name", "email", "title", "company", "website", "industry", "signal"]
    
    sample_data = [
        ["John", "Doe", "john@growthagency.com", "CEO", "Growth Agency", "example.com", "Marketing", "Looking to double client meetings this quarter."],
        ["Alice", "Smith", "alice@saascorp.io", "VP of Sales", "SaaS Corp", "example.com", "Software", "Recently hired a new sales team and needs outbound support."]
    ]
    
    with open(sample_filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(sample_data)
        
    print(f"[+] Created a blank template CSV: '{sample_filename}'. You can open it in Excel, enter your leads, and save it.")

def import_leads_from_csv(csv_path):
    """Imports leads from a CSV file into the local SQLite database"""
    if not os.path.exists(csv_path):
        print(f"[X] Error: The file '{csv_path}' does not exist.")
        return False
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    imported_count = 0
    duplicate_count = 0
    
    print(f"[*] Reading leads from '{csv_path}'...")
    
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Insert into the database, ignoring duplicates based on UNIQUE email field
                cursor.execute('''
                INSERT OR IGNORE INTO leads (campaign_id, first_name, last_name, email, title, company, website, industry, buying_signal, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    1, # Default Campaign ID
                    row['first_name'].strip(),
                    row['last_name'].strip(),
                    row['email'].strip(),
                    row['title'].strip(),
                    row['company'].strip(),
                    row['website'].strip(),
                    row.get('industry', 'B2B Services').strip(),
                    row.get('signal', 'Manual CSV Import').strip(),
                    'discovered' # Discovered state ready for processing
                ))
                
                # Check if it was successfully inserted or ignored
                if cursor.rowcount > 0:
                    imported_count += 1
                else:
                    duplicate_count += 1
                    
            except Exception as e:
                print(f"[!] Warning: Skipping invalid row in CSV. Error: {str(e)}")
                
    conn.commit()
    conn.close()
    
    print(f"[✔] Import complete! Successfully loaded {imported_count} new leads into LeadFlow database.")
    if duplicate_count > 0:
        print(f"[!] Skipped {duplicate_count} duplicate emails already existing in database.")
    return True

if __name__ == "__main__":
    create_sample_csv()
    # Test importing from the newly created template
    import_leads_from_csv("import_template.csv")
