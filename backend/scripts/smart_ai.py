import datetime
import os
import logging
from collections import Counter
import google.generativeai as genai

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/ai_processor.log')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Configure Gemini API with your API key
genai.configure(api_key="your_gemini_api_key")  # Replace with actual key or use os.getenv()

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")


class TaskAIProcessor:
    # Define keywords for task categorization
    CATEGORY_KEYWORDS = {
        "Frontend": ["ui", "interface", "component", "button", "form", "layout", "css", "tailwind", "react", "html"],
        "Backend": ["api", "database", "server", "django", "logic", "auth", "model", "query", "view", "endpoint"],
    }

    # Define choices for priority and category (optional use)
    CATEGORY_CHOICES = [
        ("Frontend", "Frontend"),
        ("Backend", "Backend"),
    ]

    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    def extract_keywords(self, text):
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
            logger.info("Keywords extracted: %s", keywords)
            return keywords
        except Exception as e:
            logger.exception("Gemini error while extracting keywords: %s", e)
            return []

    def analyze_context(self, context_data):
        all_text = " ".join([entry["content"] for entry in context_data])
        keywords = self.extract_keywords(all_text)
        freq = Counter(keywords)

        urgency_score = sum(
            3 if word in ["urgent", "asap", "immediately"] else 1
            for word in keywords
        )

        result = {
            "keywords": [word for word, _ in freq.most_common(10)],
            "urgency_score": urgency_score,
        }

        logger.info("Context analyzed: %s", result)
        return result

    def suggest_category(self, keywords):
        scores = {
            category: sum(1 for word in keywords if word in category_keywords)
            for category, category_keywords in self.CATEGORY_KEYWORDS.items()
        }
        category = max(scores, key=scores.get) if scores else "Frontend"
        logger.info("Suggested category: %s", category)
        return category

    def suggest_priority(self, urgency_score):
        if urgency_score >= 15:
            return "High"
        elif urgency_score >= 8:
            return "Medium"
        else:
            return "Low"

    def suggest_deadline(self, priority):
        days_map = {"High": 1, "Medium": 3, "Low": 5}
        days = days_map.get(priority, 3)
        deadline = str(datetime.date.today() + datetime.timedelta(days=days))
        logger.info("Suggested deadline: %s", deadline)
        return deadline

    def enhance_description(self, desc, context):
        context_summary = " ".join([entry["content"] for entry in context[:2]])
        return f"{desc.strip()} (Context: {context_summary.strip()})"

    def auto_create_task_from_context(self, context_data):
        try:
            analysis = self.analyze_context(context_data)
            keywords = analysis["keywords"]
            urgency_score = analysis["urgency_score"]

            category = self.suggest_category(keywords)
            priority = self.suggest_priority(urgency_score)
            deadline = self.suggest_deadline(priority)
            title = f"{category} Task"
            description = self.enhance_description("Auto-created task", context_data)

            task_data = {
                "title": title,
                "description": description,
                "category": category,
                "priority": priority,
                "deadline": deadline,
            }

            logger.info("Task auto-created: %s", task_data)
            return task_data

        except Exception as e:
            logger.exception("Error while auto-creating task from context: %s", e)
            return {}
