from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Model for a News Article
class NewsArticle(BaseModel):
    title: str                          # Required field
    content: str                        # Required field
    source: str                         # Required field (CNN, BBC, etc.)
    url: Optional[str] = None          # Optional field (can be empty)
    published_date: Optional[datetime] = None
    category: Optional[str] = "general"  # Default value
    image_url: Optional[str] = None
    
    class Config:
        # This allows the model to work with MongoDB's _id field
        json_schema_extra = {
            "example": {
                "title": "AI Breakthrough in 2024",
                "content": "Scientists announce new AI model...",
                "source": "TechCrunch",
                "url": "https://techcrunch.com/ai-news",
                "published_date": "2024-02-09T10:30:00",
                "category": "technology",
                "image_url": "https://example.com/image.jpg"
            }
        }

# Model for Chat Messages
class ChatMessage(BaseModel):
    user_message: str                   # What the user asks
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_message": "What are the latest tech news?"
            }
        }

# Model for Chat Response
class ChatResponse(BaseModel):
    bot_message: str                    # What the bot replies
    timestamp: datetime

# Model for scraping request
class ScrapeRequest(BaseModel):
    source: Optional[str] = "all"      # Which news site to scrape
    category: Optional[str] = "general"