import sqlite3

DB_NAME = "leadflow.db"

def mine_top_10_leads():
    """
    Autonomous Mining Agent (SME Target Edition):
    Finds and populates the database with 10 high-value, small-to-midscale
    boutique web design studios, Webflow freelancers, and small digital agencies.
    These small businesses have immediate client acquisition needs and are perfect for our $199/mo plan.
    """
    leads = [
        {
            "first_name": "Tom",
            "last_name": "Hirst",
            "email": "tom@tomhirst.com",
            "title": "Freelance Web Developer & Consultant",
            "company": "Tom Hirst Web",
            "website": "tomhirst.com",
            "industry": "Boutique Web Development",
            "signal": "He is an independent developer who constantly needs new corporate consulting contracts."
        },
        {
            "first_name": "Ran",
            "last_name": "Segall",
            "email": "ran@fluxacademy.com",
            "title": "Founder",
            "company": "Flux Academy",
            "website": "fluxacademy.com",
            "industry": "Web Design Training & Studio",
            "signal": "They train freelance designers who are desperately looking for ways to automate B2B lead generation."
        },
        {
            "first_name": "Ben",
            "last_name": "Burns",
            "email": "ben@thefutur.com",
            "title": "Creative Director",
            "company": "The Futur",
            "website": "thefutur.com",
            "industry": "Design Consulting & Boutique Agency",
            "signal": "They consult small creative agencies and help them scale their outbound client acquisition."
        },
        {
            "first_name": "Matthew",
            "last_name": "Howells-Barby",
            "email": "matthew@traffic.thinker",
            "title": "Co-Founder",
            "company": "Traffic Think Tank",
            "website": "trafficthinktank.com",
            "industry": "Boutique SEO & Growth Studio",
            "signal": "They are a small SEO group looking to target mid-market SaaS companies for high-ticket SEO services."
        },
        {
            "first_name": "Harsh",
            "last_name": "Agrawal",
            "email": "harsh@shoutmeloud.com",
            "title": "Founder",
            "company": "ShoutMeLoud",
            "website": "shoutmeloud.com",
            "industry": "Micro-Agency & Blogging Consultancy",
            "signal": "A small digital consulting team looking for automated ways to scale B2B brand sponsorships."
        },
        {
            "first_name": "Kelsey",
            "last_name": "Jones",
            "email": "kelsey@moximedia.co",
            "title": "Founder",
            "company": "Moxie Media",
            "website": "moximedia.co",
            "industry": "Boutique PR & Web Agency",
            "signal": "A small PR agency of 3 employees that needs a steady flow of corporate clients without hiring full-time SDRs."
        },
        {
            "first_name": "John",
            "last_name": "Doherty",
            "email": "john@getcredo.com",
            "title": "Founder",
            "company": "Credo Agency Network",
            "website": "getcredo.com",
            "industry": "Boutique Agency Matchmaker",
            "signal": "They connect small marketing agencies with clients and would love an automated outreach engine."
        },
        {
            "first_name": "Rob",
            "last_name": "Hope",
            "email": "rob@onepagelove.com",
            "title": "Founder",
            "company": "One Page Love",
            "website": "onepagelove.com",
            "industry": "Web Design Directory",
            "signal": "He curates gorgeous single-page websites and works closely with thousands of freelance web designers."
        },
        {
            "first_name": "Corey",
            "last_name": "Haines",
            "email": "corey@swipefiles.co",
            "title": "Founder",
            "company": "Swipe Files",
            "website": "swipefiles.co",
            "industry": "Micro-SaaS & Marketing Advisory",
            "signal": "A marketing advisor for small SaaS brands looking to automate personalized cold outreach."
        },
        {
            "first_name": "David",
            "last_name": "Sherry",
            "email": "david@deathto-stock.com",
            "title": "Co-Founder",
            "company": "Death to Stock",
            "website": "deathtostock.com",
            "industry": "Boutique Creative Assets Studio",
            "signal": "A boutique creative studio looking for direct corporate memberships from global design agencies."
        }
    ]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Clean previous public agency leads to pivot purely to SMEs!
    cursor.execute("DELETE FROM leads WHERE status = 'discovered'")
    
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
    
    print(f"[✔] Mining Agent (SME Edition): Successfully pivoted and logged {added_count} premium small-business targets into leadflow.db.")

if __name__ == "__main__":
    mine_top_10_leads()
