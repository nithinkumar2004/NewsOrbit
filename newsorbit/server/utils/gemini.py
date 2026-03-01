import json
from typing import Any

import google.generativeai as genai

from config import settings


genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel(settings.gemini_model)

PROMPT_TEMPLATE = """
You are an AI news analyst.

For the given article:
1. Summarize in 3 simple lines.
2. Extract 5 topic tags.
3. Detect sentiment (positive/negative/neutral).
4. Give importance score (1-10).
5. Rewrite headline professionally.
6. Output strictly in JSON with keys: summary,tags,sentiment,importance,rewrittenHeadline.

ARTICLE TITLE: {title}
ARTICLE DESCRIPTION: {description}
ARTICLE CONTENT: {content}
""".strip()


async def analyze_article(article: dict[str, Any]) -> dict[str, Any]:
    prompt = PROMPT_TEMPLATE.format(
        title=article.get("title", ""),
        description=article.get("description", ""),
        content=article.get("content", ""),
    )
    response = await model.generate_content_async(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "")
    data = json.loads(text)
    data["importance"] = int(data.get("importance", 0))
    data["tags"] = data.get("tags", [])[:5]
    return data
