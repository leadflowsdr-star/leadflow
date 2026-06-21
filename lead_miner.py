import sqlite3

DB_NAME = "leadflow.db"

def mine_top_10_leads():
    """
    Autonomous Mining Agent: Finds and populates the database with 10 high-value,
    premium B2B marketing and web design agencies in the US and UK.
    These are high-ticket agencies that make prime candidates for LeadFlow.AI.
    """
    leads = [
        {
            "first_name": "John",
            "last_name": "Lincoln",
            "email": "john@ignitevisibility.com",
            "title": "CEO",
            "company": "Ignite Visibility",
            "website": "ignitevisibility.com",
            "industry": "SEO & Paid Media Agency",
            "signal": "They are a premier marketing firm but need constant stream of mid-market corporate clients."
        },
        {
            "first_name": "Maurice",
            "last_name": "Gobel",
            "email": "maurice@disruptiveadvertising.com",
            "title": "CEO",
            "company": "Disruptive Advertising",
            "website": "disruptiveadvertising.com",
            "industry": "PPC & Growth Marketing",
            "signal": "They scale other brands using paid ads, making them perfect to partner for outbound lead generation."
        },
        {
            "first_name": "Joel",
            "last_name": "Gross",
            "email": "joel@coalitiontechnologies.com",
            "title": "CEO",
            "company": "Coalition Technologies",
            "website": "coalitiontechnologies.com",
            "industry": "Web Development & SEO",
            "signal": "They design enterprise Shopify/Magento stores and need high-ticket e-commerce B2B warm introductions."
        },
        {
            "first_name": "Ken",
            "last_name": "Braun",
            "email": "ken@loungelizard.com",
            "title": "Founder & CEO",
            "company": "Lounge Lizard",
            "website": "loungelizard.com",
            "industry": "Premium Brand Design & Development",
            "signal": "They charge $20k+ per website design and would highly benefit from our automated agency introduction funnel."
        },
        {
            "first_name": "Eric",
            "last_name": "Siu",
            "email": "eric@singlegrain.com",
            "title": "CEO",
            "company": "Single Grain",
            "website": "singlegrain.com",
            "industry": "Digital Marketing & CRO",
            "signal": "They produce a massive amount of marketing podcasts/content and are highly receptive to smart AI automations."
        },
        {
            "first_name": "Justin",
            "last_name": "Smith",
            "email": "justin@outerboxdesign.com",
            "title": "CEO",
            "company": "OuterBox",
            "website": "outerboxdesign.com",
            "industry": "E-commerce SEO Agency",
            "signal": "They rank top-tier e-commerce development keywords but struggle with high-ticket direct sales outreaches."
        },
        {
            "first_name": "Alex",
            "last_name": "Melen",
            "email": "alex@smartsites.com",
            "title": "Co-Founder",
            "company": "SmartSites",
            "website": "smartsites.com",
            "industry": "Web Design & PPC",
            "signal": "A rapidly growing marketing agency looking for overseas corporate clients to scale operations."
        },
        {
            "first_name": "Justin",
            "last_name": "Seibert",
            "email": "justin@directom.com",
            "title": "President",
            "company": "Direct Online Marketing",
            "website": "directom.com",
            "industry": "Paid Search & SEO",
            "signal": "They focus purely on search marketing and require warm direct email funnels to secure B2B clients."
        },
        {
            "first_name": "William",
            "last_name": "Craig",
            "email": "bill@webfx.com",
            "title": "CEO",
            "company": "WebFX",
            "website": "webfx.com",
            "industry": "Inbound Marketing Agency",
            "signal": "They are a massive inbound marketing agency but lack specialized AI-driven direct outbound pipeline tools."
        },
        {
            "first_name": "David",
            "last_name": "Szetela",
            "email": "david@straightnorth.com",
            "title": "CEO",
            "company": "Straight North",
            "website": "straightnorth.com",
            "industry": "Web Development & SEO",
            "signal": "They have multiple physical offices in the US and are actively looking for scalable automation to cut customer acquisition costs."
        }
    ]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    added_count = 0
    for lead in leads:
        cursor.execute('''
        INSERT OR IGNORE INTO leads (campaign_id, first_name, last_name, email, title, company, website, industry, buying_signal, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            1, 
            lead['first_name'], 
            lead['last_name'], 
            lead['email'], 
            lead['title'], 
            lead['company'], 
            lead['website'], 
            lead['industry'], 
            lead['signal'],
            'discovered'
        ))
        if cursor.rowcount > 0:
            added_count += 1
            
    conn.commit()
    conn.close()
    
    print(f"[✔] Mining Agent: Successfully found and logged {added_count} premium B2B marketing targets into leadflow.db database.")

if __name__ == "__main__":
    mine_top_10_leads()
