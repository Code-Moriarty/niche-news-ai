# core/ai_service.py
import google.generativeai as genai
from django.conf import settings

def generate_newsletter_content(niche_name):
    """
    Generates newsletter content for a given niche using the Gemini API.
    """
    try:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        prompt = f"""
        You are an expert newsletter creator specializing in engaging, niche content.
        Your task is to generate a short newsletter draft for the topic: "{niche_name}".

        The newsletter must include:
        1.  A catchy, compelling title.
        2.  A brief, one-paragraph introduction that hooks the reader.
        3.  Two or three distinct sections with interesting recent developments, news, or fun facts related to the topic. Each section should have a sub-heading.
        4.  A short, friendly closing paragraph.

        Format the entire output in Markdown.
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # In a real app, you'd want more sophisticated logging/error handling
        print(f"Error generating content: {e}")
        return "Error: Could not generate newsletter content. Please check the API key and configuration."
