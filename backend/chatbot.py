import os
from dotenv import load_dotenv
from database import get_news_collection
import random

# Load environment variables
load_dotenv()

def get_recent_news_context(limit=5):
    """
    Get recent news articles to provide context to the chatbot
    """
    try:
        collection = get_news_collection()
        if collection is None:
            return []
        
        # Get latest articles
        articles = list(collection.find().sort("_id", -1).limit(limit))
        return articles
    except Exception as e:
        print(f"Error getting news: {e}")
        return []

def chat_with_ai(user_message: str) -> str:
    """
    Mock chatbot that responds intelligently based on news in database
    (No OpenAI API needed - perfect for demo!)
    """
    try:
        # Get news articles
        articles = get_recent_news_context(limit=10)
        
        if not articles:
            return "I don't have any news articles in the database yet. Please scrape some news first using the /scrape endpoint!"
        
        # Convert message to lowercase for matching
        message_lower = user_message.lower()
        
        # Response logic based on user question
        
        # 1. If asking about "latest" or "recent" news
        if any(word in message_lower for word in ["latest", "recent", "new", "today", "current"]):
            response = "Here are the latest news articles:\n\n"
            for i, article in enumerate(articles[:5], 1):
                response += f"{i}. **{article.get('title', 'N/A')}**\n"
                response += f"   Source: {article.get('source', 'N/A')}\n"
                response += f"   {article.get('content', 'N/A')[:150]}...\n\n"
            return response
        
        # 2. If asking about specific category
        elif any(word in message_lower for word in ["technology", "tech", "ai", "computer"]):
            tech_articles = [a for a in articles if a.get('category') == 'technology']
            if tech_articles:
                response = "Here are the technology news:\n\n"
                for i, article in enumerate(tech_articles[:3], 1):
                    response += f"{i}. **{article.get('title', 'N/A')}**\n"
                    response += f"   {article.get('content', 'N/A')[:150]}...\n\n"
                return response
            else:
                return "I don't have any technology news yet. Try scraping tech news first!"
        
        # 3. If asking for summary
        elif any(word in message_lower for word in ["summar", "brief", "overview", "top"]):
            response = "📰 **News Summary**\n\n"
            for i, article in enumerate(articles[:3], 1):
                response += f"{i}. **{article.get('title', 'N/A')}** ({article.get('source', 'N/A')})\n"
                response += f"   {article.get('content', 'N/A')[:100]}...\n\n"
            response += f"\nI have {len(articles)} articles to show you. Would you like to know more about any specific topic?"
            return response
        
        # 4. If asking about count
        elif any(word in message_lower for word in ["how many", "count", "number"]):
            collection = get_news_collection()
            total = collection.count_documents({})
            return f"📊 I currently have {total} news articles in the database. They cover topics like technology, business, and general news. What would you like to know about them?"
        
        # 5. If asking about sources
        elif any(word in message_lower for word in ["source", "from where", "which website"]):
            sources = list(set([a.get('source', 'Unknown') for a in articles]))
            return f"📰 My news comes from these sources: {', '.join(sources)}. I can provide more details about any of these sources!"
        
        # 6. Generic greeting
        elif any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            return f"👋 Hello! I'm your AI news assistant. I have {len(articles)} news articles ready for you. You can ask me about:\n- Latest news\n- Technology news\n- News summaries\n- Specific topics\n\nWhat would you like to know?"
        
        # 7. Help request
        elif any(word in message_lower for word in ["help", "what can you do", "commands"]):
            return """🤖 **I can help you with:**

1. **Latest News**: Ask "What are the latest news?"
2. **Category News**: Ask "Tell me about technology news"
3. **Summaries**: Ask "Summarize the top articles"
4. **Counts**: Ask "How many articles do you have?"
5. **Sources**: Ask "What are your news sources?"

Just ask me anything about the news!"""
        
        # 8. Default - show relevant articles
        else:
            response = "I found some relevant news for you:\n\n"
            for i, article in enumerate(articles[:3], 1):
                response += f"{i}. **{article.get('title', 'N/A')}**\n"
                response += f"   Source: {article.get('source', 'N/A')}\n"
                response += f"   {article.get('content', 'N/A')[:120]}...\n\n"
            response += "\n💡 Try asking: 'latest news', 'tech news', or 'summarize articles'"
            return response
        
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# For testing
if __name__ == "__main__":
    print("🤖 Testing Mock AI Chatbot...\n")
    
    # Test 1: Ask about latest news
    print("User: What are the latest tech news?")
    response = chat_with_ai("What are the latest tech news?")
    print(f"Bot: {response}\n")
    
    print("-" * 80)
    
    # Test 2: Ask for summary
    print("\nUser: Summarize the top 3 news articles")
    response = chat_with_ai("Summarize the top 3 news articles")
    print(f"Bot: {response}")
    
    print("\n" + "-" * 80)
    
    # Test 3: Greeting
    print("\nUser: Hello!")
    response = chat_with_ai("Hello!")
    print(f"Bot: {response}")