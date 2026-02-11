from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from models import NewsArticle, ChatMessage, ChatResponse, ScrapeRequest
from database import connect_to_mongodb, get_news_collection
from typing import List
from datetime import datetime
from bson import ObjectId


# Lifespan context manager (replaces deprecated on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("🚀 Starting FastAPI...")
    connect_to_mongodb()
    print("✅ FastAPI started and connected to MongoDB")
    print("📡 Server running at http://localhost:8000")
    yield
    # Shutdown code (if needed)
    print("🛑 FastAPI shutting down")


app = FastAPI(
    title="AI News Portal API",
    description="API for fetching, scraping, and chatting about news",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HOME ENDPOINT
@app.get("/")
def read_root():
    return {
        "message": "Welcome to AI News Portal API!",
        "endpoints": {
            "docs": "/docs",
            "get_news": "GET /news",
            "add_news": "POST /news",
            "delete_all": "DELETE /news",
            "delete_one": "DELETE /news/{id}",
            "scrape": "POST /scrape",
            "chat": "POST /chat"
        },
        "database": "MongoDB (Persistent Storage)"
    }

# GET ALL NEWS
@app.get("/news")
def get_news():
    """
    Returns all news articles from MongoDB
    """
    collection = get_news_collection()
    
    # Get all articles from database
    articles = list(collection.find())
    
    # Convert MongoDB _id to string for JSON serialization
    for article in articles:
        article['_id'] = str(article['_id'])
    
    return articles

# ADD NEWS
@app.post("/news")
def add_news(article: NewsArticle):
    """
    Add a news article to MongoDB
    """
    collection = get_news_collection()
    
    # Convert Pydantic model to dictionary
    article_dict = article.dict()  # Changed from model_dump() to dict()
    
    # Insert into MongoDB
    result = collection.insert_one(article_dict)
    
    # Don't return ObjectId directly - convert to string
    return {
        "status": "success",
        "message": "Article added to database",
        "id": str(result.inserted_id),  # Convert ObjectId to string
        "article": {
            **article_dict,
            "_id": str(result.inserted_id)  # Add the ID as string
        }
    }

# DELETE ALL NEWS
@app.delete("/news")
def delete_all_news():
    """
    Delete all news articles from MongoDB
    """
    collection = get_news_collection()
    
    # Count before deletion
    count = collection.count_documents({})
    
    # Delete all documents
    collection.delete_many({})
    
    return {
        "status": "success",
        "message": f"Deleted {count} articles from database",
        "remaining": 0
    }

# DELETE SINGLE NEWS BY ID
@app.delete("/news/{article_id}")
def delete_news_by_id(article_id: str):
    """
    Delete a specific news article by MongoDB ID
    """
    collection = get_news_collection()
    
    try:
        # Convert string ID to MongoDB ObjectId
        obj_id = ObjectId(article_id)
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid article ID format"
        )
    
    # Find and delete
    result = collection.delete_one({"_id": obj_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Article with ID {article_id} not found"
        )
    
    return {
        "status": "success",
        "message": f"Deleted article with ID {article_id}",
        "remaining_count": collection.count_documents({})
    }


# SCRAPE NEWS - Now actually works!
@app.post("/scrape")
def scrape_news(request: ScrapeRequest):
    """
    Trigger news scraping and save to database
    """
    from scraper import scrape_multiple_sources
    
    # Scrape articles
    articles = scrape_multiple_sources(request.category)
    
    if not articles:
        return {
            "status": "error",
            "message": f"No articles found for category: {request.category}",
            "articles_scraped": 0
        }
    
    # Save to MongoDB
    collection = get_news_collection()
    
    # Insert all articles
    result = collection.insert_many(articles)
    
    return {
        "status": "success",
        "message": f"Scraped and saved {len(articles)} articles",
        "articles_scraped": len(articles),
        "category": request.category,
        "inserted_ids": [str(id) for id in result.inserted_ids]
    }
# CHAT ENDPOINT (placeholder - we'll implement later)
@app.post("/chat", response_model=ChatResponse)
def chat_with_bot(message: ChatMessage):
    """
    Chat with AI about news (to be implemented)
    """
    return ChatResponse(
        bot_message=f"You said: {message.user_message}. AI chatbot coming soon!",
        timestamp=datetime.now()
    )