import datetime
from collections import Counter
import google.generativeai as genai
from .logging.ai_processor_logger import logger

genai.configure(api_key="AIzaSyAY2lnQkS70ECLLu20Dfvxa1GFmwu26GkE")
model = genai.GenerativeModel(model_name="gemini-2.5-pro")
response = model.generate_content("Extract 5 keywords from: Build a Django REST API with context.")


class TaskAIProcessor:
    CATEGORY_KEYWORDS = {
        "Frontend": ["ui", "interface", "component", "button", "form", "layout", "css", "tailwind", "react", "html"],
        "Backend": ["api", "database", "server", "django", "logic", "auth", "model", "query", "view", "endpoint"],
    }

    def extract_keywords(self, text):
        prompt = f"""
        Extract 10 important keywords (lowercase, comma-separated) from the following:
        {text}
        """
        try:
            response = model.generate_content(prompt)
            content = response.text.strip()
            keywords = [w.strip() for w in content.lower().split(",") if w.strip().isalpha()]
            logger.info("Keywords: %s", keywords)
            return keywords
        except Exception as e:
            logger.exception("Gemini error: %s", e)
            return []

    def analyze_context(self, context_data):
        all_text = " ".join([
            entry["content"] if isinstance(entry, dict) and "content" in entry else str(entry)
            for entry in context_data
        ])
        keywords = self.extract_keywords(all_text)
        freq = Counter(keywords)
        urgency_score = sum(
            3 if word in ["urgent", "asap", "immediately"] else 1
            for word in keywords
        )
        return {
            "keywords": [word for word, _ in freq.most_common(10)],
            "urgency_score": urgency_score
        }

    def suggest_category(self, keywords):
        scores = {
            cat: sum(1 for word in keywords if word in words)
            for cat, words in self.CATEGORY_KEYWORDS.items()
        }
        return max(scores, key=scores.get)

    def suggest_priority(self, urgency_score):
        return "High" if urgency_score >= 15 else "Medium" if urgency_score >= 8 else "Low"

    def suggest_deadline(self, priority):
        days = {"High": 1, "Medium": 3, "Low": 5}.get(priority, 3)
        return str(datetime.date.today() + datetime.timedelta(days=days))

    def enhance_description(self, desc, context):
        summary = " ".join([
            entry["content"] if isinstance(entry, dict) and "content" in entry else str(entry)
            for entry in context[:2]
        ])
        return f"{desc.strip()} (Context: {summary.strip()})"

    def auto_create_task_from_context(self, context_data):
        try:
            analysis = self.analyze_context(context_data)
            category = self.suggest_category(analysis["keywords"])
            priority = self.suggest_priority(analysis["urgency_score"])
            deadline = self.suggest_deadline(priority)
            description = self.enhance_description("Auto-created task", context_data)

            task_data = {
                "title": f"{category} Task",
                "description": description,
                "category": category,
                "priority": priority,
                "deadline": deadline,
            }

            logger.info("Generated Task: %s", task_data)
            return task_data
        except Exception as e:
            logger.exception("Auto-create error: %s", e)
            return {}
