import urllib.request
import urllib.error
import json
import os

def generate_personalized_email_openrouter(name, title, company, industry, signal, api_key=None):
    """
    Generates a personalized cold email using OpenRouter's FREE models
    (such as Google Gemma 4 31B It).
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # If no API key is provided, check config.json or environment
    if not api_key:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key and os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                    api_key = config.get("OPENROUTER_API_KEY")
            except:
                pass
        if not api_key:
            api_key = "MOCK_KEY_FOR_TESTING"

    # Prompt engineering designed to be ultra-effective for B2B cold outreach
    prompt = f"""
    You are an expert B2B copywriter. Write a highly personalized cold email from "Elena" to a prospect.
    
    Prospect Details:
    - Name: {name}
    - Title: {title}
    - Company: {company}
    - Industry: {industry}
    - Recent News/Signal: {signal}
    
    Offer of LeadFlow.AI: We build autonomous AI SDR agents that find leads and book sales meetings for 1/5th the cost of a human hire.
    
    Writing Rules:
    1. Keep it under 100 words.
    2. Write in a friendly, professional, casual tone (no corporate fluff, no "hope you are well").
    3. The first 1-2 sentences MUST mention their recent news/signal to prove we researched them.
    4. Propose a low-friction 5-minute call as the call to action.
    5. Write only the email text, starting with the Subject line.
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://leadflow.ai",
        "X-Title": "LeadFlow.AI SDR Agent"
    }

    data = {
        # Using Google Gemma 4 31B IT which is 100% FREE on OpenRouter and has high rate-limits!
        "model": "google/gemma-4-31b-it:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    print(f"[*] Copywriter Agent: Sending prompt to OpenRouter (Gemma-4-31B-IT)...")
    
    # If the key is a mock placeholder, simulate the response
    if api_key == "MOCK_KEY_FOR_TESTING":
        print("[!] Using simulation mode (No OpenRouter API key found. Set OPENROUTER_API_KEY env variable to run live).")
        mock_output = "Subject: Helping SaaSify scale...\n\nHi Sarah,\n\nI saw that SaaSify recently launched your new AI chatbot on Product Hunt. Congrats!\n\nAs VP of Growth, keeping the pipeline full is tough. We build AI-powered SDR agents that automate prospecting and book meetings, at 1/5th the cost of a human team.\n\nAre you open to a quick 5-minute chat next Tuesday?\n\nBest,\nElena\nLeadFlow.AI"
        return mock_output

    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            email_draft = res_data['choices'][0]['message']['content']
            return email_draft
    except urllib.error.HTTPError as e:
        try:
            err_content = e.read().decode('utf-8')
            print(f"[!] OpenRouter API Error Body: {err_content}")
        except:
            pass
        print(f"[!] OpenRouter API Error Code: {e.code} - {e.reason}")
        return "Error generating email. Please check your API key or internet connection."
    except Exception as e:
        print(f"[!] General Error: {str(e)}")
        return "Error generating email. Please check your API key or internet connection."

if __name__ == "__main__":
    # Test execution with mock key
    print("--- Testing OpenRouter API integration ---")
    email = generate_personalized_email_openrouter(
        name="Sarah Jenkins",
        title="VP of Growth",
        company="SaaSify",
        industry="SaaS",
        signal="Product Hunt Launch of AI Chatbot"
    )
    print("\nGenerated Output:")
    print(email)
