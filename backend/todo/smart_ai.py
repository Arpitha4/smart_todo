import datetime
import os
from collections import Counter
import google.generativeai as genai

# === Gemini API Setup ===
genai.configure(api_key="your_gemini_api_key")  # Replace with your actual key or use an env var

model = genai.GenerativeModel("gemini-pro")

# === Task Category & Priority Setup ===

CATEGORY_KEYWORDS = {
    "Frontend": ["ui", "interface", "component", "button", "form", "layout", "css", "tailwind", "react", "html"],
    "Backend": ["api", "database", "server", "django", "logic", "auth", "model", "query", "view", "endpoint"],
}

CATEGORY_CHOICES = [
    ("Frontend", "Frontend"),
    ("Backend", "Backend"),
]

PRIORITY_CHOICES = [
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
]

# === Replace SpaCy with Gemini for keyword extraction ===
def extract_keywords(text):
    prompt = f"""
    Extract the 10 most important keywords from the following text. 
    Only return lowercase words, separated by commas. Do not include stopwords like "the", "is", etc.

    Text:
    {text}
    """

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        keywords = [word.strip() for word in content.lower().split(",") if word.strip().isalpha()]
        return keywords
    except Exception as e:
        print("Gemini error:", e)
        return []

# === Core AI-assisted Logic ===

def analyze_context(context_data):
    all_text = " ".join([entry["content"] for entry in context_data])
    keywords = extract_keywords(all_text)
    freq = Counter(keywords)
    urgency_score = sum(
        3 if word in ["urgent", "asap", "immediately"] else 1
        for word in keywords
    )
    return {
        "keywords": [word for word, _ in freq.most_common(10)],
        "urgency_score": urgency_score,
    }

def suggest_category(keywords):
    scores = {
        category: sum(1 for word in keywords if word in category_keywords)
        for category, category_keywords in CATEGORY_KEYWORDS.items()
    }
    return max(scores, key=scores.get) if scores else "Frontend"

def suggest_priority(urgency_score):
    if urgency_score >= 15:
        return "High"
    elif urgency_score >= 8:
        return "Medium"
    else:
        return "Low"

def suggest_deadline(priority):
    days_map = {"High": 1, "Medium": 3, "Low": 5}
    days = days_map.get(priority, 3)
    return str(datetime.date.today() + datetime.timedelta(days=days))

def enhance_description(desc, context):
    context_summary = " ".join([entry["content"] for entry in context[:2]])
    return f"{desc.strip()} (Context: {context_summary.strip()})"

def auto_create_task_from_context(context_data):
    analysis = analyze_context(context_data)
    keywords = analysis["keywords"]
    urgency_score = analysis["urgency_score"]

    category = suggest_category(keywords)
    priority = suggest_priority(urgency_score)
    deadline = suggest_deadline(priority)
    title = f"{category} Task"
    description = enhance_description("Auto-created task", context_data)

    return {
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "deadline": deadline,
    }
