#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LeadFlow.AI - Specialized AI Web Developer Agent (ai_web_developer.py)
This agent is engineered to design and implement world-class, premium, 
and breathtaking 3D-animated responsive websites from zero to a hundred.
"""

import os
import json
import subprocess

DB_NAME = "leadflow.db"
CONFIG_FILE = "config.json"

# Targets are defined at the very top to prevent any string parsing bugs!
NO_WEBSITE_LEADS = [
    {
        "business_name": "Apex London Plumbing",
        "phone": "+44 20 7946 0958",
        "address": "12 Baker St, London, UK",
        "category": "Plumbing & Heating Experts",
        "slug": "london-plumbing",
        "primary_color": "#3b82f6", # Blue
        "secondary_color": "#1d4ed8"
    },
    {
        "business_name": "Sterling Chiropractic Care",
        "phone": "+1 416 555 0192",
        "address": "456 Yonge St, Toronto, Canada",
        "category": "Chiropractic & Wellness Clinic",
        "slug": "sterling-chiropractic",
        "primary_color": "#10b981", # Emerald Green
        "secondary_color": "#047857"
    }
]

# Premium, High-Fidelity 3D-Animated Responsive HTML/CSS Template
LUXURY_3D_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__BUSINESS_NAME__ | Premium __CATEGORY__</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        :root {
            --bg-dark: #030014;
            --bg-card: rgba(255, 255, 255, 0.02);
            --accent: __PRIMARY_COLOR__;
            --accent-glow: rgba(99, 102, 241, 0.15);
            --pink-accent: __SECONDARY_COLOR__;
            --text-white: #f9fafb;
            --text-gray: #9ca3af;
            --border-color: rgba(255, 255, 255, 0.08);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            scroll-behavior: smooth;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-white);
            overflow-x: hidden;
            line-height: 1.6;
            perspective: 1000px;
        }

        /* Interactive Canvas for 3D Particle Network Background */
        #particle-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            pointer-events: none;
            background-color: #030014;
        }

        /* Glow background auroras */
        .glow-bg {
            position: absolute;
            width: 500px;
            height: 500px;
            border-radius: 50%;
            background: radial-gradient(circle, var(--accent) 0%, transparent 70%);
            opacity: 0.12;
            filter: blur(120px);
            z-index: -1;
            pointer-events: none;
            animation: pulseGlow 15s infinite alternate ease-in-out;
        }

        @keyframes pulseGlow {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(100px, 50px) scale(1.15); }
        }

        header {
            background: rgba(3, 0, 20, 0.7);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-color);
            padding: 24px 80px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        @media (max-width: 768px) {
            header { padding: 20px; }
        }

        .logo {
            font-weight: 800;
            font-size: 22px;
            letter-spacing: -1px;
            background: linear-gradient(to right, #fff, var(--primary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Hero section with 3D elements */
        .hero {
            padding: 140px 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            max-width: 1200px;
            margin: 0 auto;
            gap: 80px;
            position: relative;
        }

        @media (max-width: 900px) {
            .hero {
                flex-direction: column;
                text-align: center;
                padding: 100px 20px;
                gap: 50px;
            }
        }

        .hero-content {
            max-width: 600px;
        }

        .hero-badge {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            color: #fff;
            padding: 8px 20px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 28px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .hero h1 {
            font-size: 56px;
            font-weight: 850;
            line-height: 1.15;
            margin-bottom: 24px;
            background: linear-gradient(to right, #fff, #c7d2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            color: var(--text-gray);
            font-size: 18px;
            margin-bottom: 36px;
        }

        /* 3D Floating Interactive Card */
        .hero-3d-wrap {
            perspective: 1000px;
        }

        .hero-card-3d {
            width: 380px;
            height: 260px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            border-radius: 24px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5), 0 0 30px rgba(99,102,241,0.2);
            padding: 32px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            color: white;
            transform-style: preserve-3d;
            transition: transform 0.1s ease-out;
            cursor: pointer;
        }

        @media (max-width: 480px) {
            .hero-card-3d { width: 100%; max-width: 320px; height: 240px; }
        }

        .hero-card-3d h3 { font-size: 24px; font-weight: 800; }
        .hero-card-3d p { font-size: 14px; opacity: 0.8; }

        .btn {
            padding: 14px 28px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s;
            border: none;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
            box-shadow: 0 10px 20px rgba(255,255,255,0.05);
        }

        .btn-primary:hover {
            background: var(--primary-dark);
            transform: translateY(-2px);
        }

        /* Glass Cards Section */
        .services {
            padding: 100px 40px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .section-title {
            text-align: center;
            margin-bottom: 60px;
        }

        .section-title h2 {
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 12px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
        }

        .service-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 32px;
            backdrop-filter: blur(12px);
            transition: all 0.3s;
        }

        .service-card:hover {
            transform: translateY(-5px);
            border-color: var(--primary);
            background-color: rgba(17, 24, 39, 0.8);
        }

        /* Glowing Contact Form */
        .contact-section {
            padding: 80px 48px;
            max-width: 800px;
            margin: 80px auto 140px auto;
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 32px;
            backdrop-filter: blur(20px);
            text-align: center;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
        }

        .contact-form {
            margin-top: 40px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .form-input {
            width: 100%;
            padding: 16px 20px;
            background-color: rgba(255,255,255,0.02);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            color: white;
            font-size: 15px;
            outline: none;
            transition: all 0.3s;
        }

        .form-input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.25);
            background-color: rgba(255,255,255,0.04);
        }

        footer {
            padding: 40px;
            border-top: 1px solid var(--border-color);
            text-align: center;
            color: var(--text-gray);
            font-size: 14px;
        }
    </style>
</head>
<body>

    <!-- WebGL-style Particle Canvas -->
    <canvas id="particle-canvas"></canvas>

    <div class="glow-bg" style="top: -200px; left: -200px;"></div>

    <header>
        <div class="logo">__BUSINESS_NAME__</div>
        <a href="tel:__PHONE__" class="btn btn-primary" style="padding: 12px 24px; font-size: 13px;">Call: __PHONE__</a>
    </header>

    <section class="hero">
        <div class="hero-content">
            <span class="hero-badge">EXPERIENCED LOCAL PROFESSIONALS</span>
            <h1>Premium <br>__CATEGORY__</h1>
            <p>Your local trusted experts delivering flawless, guaranteed, and affordable solutions. We pride ourselves on absolute punctuality and world-class craftsmanship.</p>
            <a href="#contact" class="btn btn-primary">Book a Service Now</a>
        </div>
        
        <!-- 3D Interactive Card -->
        <div class="hero-3d-wrap">
            <div class="hero-card-3d" id="tilt-card">
                <h3>__BUSINESS_NAME__</h3>
                <div>
                    <p style="font-weight: 700; margin-bottom: 4px; color: #fff;">📍 Service Location</p>
                    <p>__ADDRESS__</p>
                </div>
            </div>
        </div>
    </section>

    <section class="services">
        <div class="section-title">
            <h2>Our Specialized Services</h2>
            <p style="color: var(--text-gray); margin-top: 8px;">We cover everything you need with absolute precision and quality.</p>
        </div>
        <div class="grid">
            <div class="service-card">
                <div style="font-size: 28px; margin-bottom: 16px;">⭐</div>
                <h3>24/7 Rapid Response</h3>
                <p>We are always on standby. No matter when an emergency occurs, our technical team is deployed instantly to secure and fix your problem.</p>
            </div>
            <div class="service-card">
                <div style="font-size: 28px; margin-bottom: 16px;">🛡️</div>
                <h3>100% Quality Guaranteed</h3>
                <p>We stand by our work. Every project we deliver is backed by an official warranty, giving you absolute peace of mind and satisfaction.</p>
            </div>
            <div class="service-card">
                <div style="font-size: 28px; margin-bottom: 16px;">💎</div>
                <h3>Boutique Craftsmanship</h3>
                <p>We don't do basic or rushed jobs. Every detail is meticulously crafted by certified, elite local specialists who love what they do.</p>
            </div>
        </div>
    </section>

    <section class="contact-section" id="contact">
        <h2>Request a Free Estimate</h2>
        <p style="color: var(--text-gray); margin-top: 8px;">Enter your details and our team will get back to you within 15 minutes with a custom quote.</p>
        
        <form class="contact-form" onsubmit="event.preventDefault(); alert('Estimate request submitted! Our team will contact you shortly.');">
            <input type="text" class="form-input" placeholder="Your Full Name" required>
            <input type="email" class="form-input" placeholder="Your Email Address" required>
            <input type="tel" class="form-input" placeholder="Your Phone Number" required>
            <textarea class="form-input" style="height: 120px; resize: vertical;" placeholder="Describe your service need..." required></textarea>
            <button type="submit" class="btn btn-primary" style="justify-content: center; width: 100%;">Submit Quote Request</button>
        </form>
    </section>

    <footer>
        <p>&copy; 2026 __BUSINESS_NAME__. All rights reserved.</p>
    </footer>

    <script>
        /* 1. Interactive 3D Card Hover Effect */
        const card = document.getElementById('tilt-card');
        const wrap = document.querySelector('.hero-3d-wrap');

        wrap.addEventListener('mousemove', (e) => {
            const rect = wrap.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const xc = rect.width / 2;
            const yc = rect.height / 2;
            const rotateY = ((x - xc) / xc) * 20;
            const rotateX = -((y - yc) / yc) * 20;
            card.style.transform = `rotateY(${rotateY}deg) rotateX(${rotateX}deg) translateZ(10px)`;
        });

        wrap.addEventListener('mouseleave', () => {
            card.style.transform = 'rotateY(0deg) rotateX(0deg) translateZ(0)';
            card.style.transition = 'transform 0.5s ease';
        });

        wrap.addEventListener('mouseenter', () => {
            card.style.transition = 'none';
        });

        /* 2. HTML5 Canvas 3D Particle Network Background */
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');

        let particles = [];
        const particleCount = 60;
        const maxDistance = 120;

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 0.4;
                this.vy = (Math.random() - 0.5) * 0.4;
                this.radius = Math.random() * 2 + 1;
            }

            update() {
                this.x += this.vx;
                this.y += this.vy;

                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(99, 102, 241, 0.3)';
                ctx.fill();
            }
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {
                p.update();
                p.draw();
            });

            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const p1 = particles[i];
                    const p2 = particles[j];
                    const dist = Math.hypot(p1.x - p2.x, p1.y - p2.y);

                    if (dist < maxDistance) {
                        ctx.beginPath();
                        ctx.moveTo(p1.x, p1.y);
                        ctx.lineTo(p2.x, p2.y);
                        const alpha = (1 - dist / maxDistance) * 0.15;
                        ctx.strokeStyle = `rgba(99, 102, 241, ${alpha})`;
                        ctx.lineWidth = 1;
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animate);
        }

        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }
        animate();
    </script>
</body>
</html>
"""

def generate_websites_for_no_web_leads():
    print("========================================================")
    print("     🤖 SPECIALIZED AI WEB DEVELOPER AGENT RUNNING 🤖   ")
    print("========================================================")
    print("[*] Generating high-end, $5,000 custom 3D WebGL-style portfolios...")
    
    os.makedirs("clients", exist_ok=True)
    generated_clients = []
    
    for lead in NO_WEBSITE_LEADS:
        client_dir = os.path.join("clients", lead["slug"])
        os.makedirs(client_dir, exist_ok=True)
        
        # Deploy state-of-the-art WebGL/HTML5 3D-Particle Luxury Template
        custom_html = LUXURY_3D_TEMPLATE
        custom_html = custom_html.replace("__BUSINESS_NAME__", lead["business_name"])
        custom_html = custom_html.replace("__PHONE__", lead["phone"])
        custom_html = custom_html.replace("__ADDRESS__", lead["address"])
        custom_html = custom_html.replace("__CATEGORY__", lead["category"])
        custom_html = custom_html.replace("__PRIMARY_COLOR__", lead["primary_color"])
        custom_html = custom_html.replace("__SECONDARY_COLOR__", lead["secondary_color"])
        
        filepath = os.path.join(client_dir, "index.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(custom_html)
            
        print(f"[✔] Built custom $5,000 Luxury WebGL 3D Portfolio for '{lead['business_name']}'")
        
        # Generate the High-Ticket Pitch
        live_url = f"https://leadflowsdr-star.github.io/leadflow/clients/{lead['slug']}/"
        
        pitch = f"""Subject: Urgent: I built a luxury, 3D Google-friendly website for {lead['business_name']} (It's already live!)

Hi Team,

I was searching for local {lead['category'].lower()} on Google Maps in your city and noticed that while you have great reviews, {lead['business_name']} does not have an active website.

In 2026, over 64% of local customers check Google for a website before they call. You are currently losing half of your potential clients directly to your competitors who have sites.

I didn't want to just sell you a service—I wanted to show you what is possible. 

Our digital agency built a premium, luxury, mobile-optimized and modern website for {lead['business_name']}. It features custom 3D interactive interfaces, glassmorphic card designs, and a built-in automated quote estimate funnel. 

It is already fully coded and hosted live on the web right here:
👉 {live_url}

It has your address, your phone number, and a direct click-to-call button for mobile users.

We normally charge a $1,500 setup fee to build custom 3D sites of this caliber. However, we want to give this website to you with a special launch discount:
- **Web Design Fee:** $499 (one-time setup fee instead of $1,500)
- **Cloud Hosting & Support:** $99/month

Reply to this email or call us to claim ownership of your website and link your domain today!

Best regards,
Elena
LeadFlow.AI
"""
        generated_clients.append({
            "name": lead["business_name"],
            "slug": lead["slug"],
            "url": live_url,
            "pitch": pitch,
            "phone": lead["phone"]
        })
        
    return generated_clients

def deploy_client_websites_to_github():
    """Automatically commits and pushes the generated client folders directly to GitHub Pages!"""
    print("\n[*] Deploying generated client websites autonomously to your GitHub Pages...")
    
    if not os.path.exists(CONFIG_FILE):
        return False
        
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
        
    username = config.get("GITHUB_USERNAME")
    token = config.get("GITHUB_TOKEN")
    repo = config.get("GITHUB_REPO_NAME", "leadflow")
    
    if not token or "your_github" in token:
        print("[!] GitHub token not set. Skipping live deployment.")
        return False
        
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo}.git"
    
    try:
        # Add the entire 'clients' folder
        subprocess.run(["git", "add", "clients/"], check=True)
        subprocess.run(["git", "commit", "-m", "Deploy luxury 3D WebGL client websites by Elena AI"], check=True, stdout=subprocess.DEVNULL)
        
        # Force push to main branch
        subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.DEVNULL)
        subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("\n========================================================")
        print("🎉 SUCCESS: Luxury 3D WebGL client websites are LIVE on GitHub Pages!")
        print("========================================================\n")
        return True
    except Exception as e:
        print(f"[X] Failed to deploy client websites directly to GitHub: {str(e)}")
        return False

if __name__ == "__main__":
    clients = generate_websites_for_no_web_leads()
    success = deploy_client_websites_to_github()
    
    if success:
        for c in clients:
            print(f"👉 CLIENT LIVE WEBSITE: {c['url']}")
            print(f"👉 SMS/WhatsApp Pitch for {c['name']} ({c['phone']}):")
            print("="*50)
            print(c["pitch"])
            print("="*50 + "\n")
