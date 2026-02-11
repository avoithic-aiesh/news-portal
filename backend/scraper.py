import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import feedparser

def scrape_rss_feed(feed_url: str, source_name: str, category: str = "general") -> List[Dict]:
    """
    Scrape articles from an RSS feed
    """
    articles = []
    
    try:
        # Parse the RSS feed
        feed = feedparser.parse(feed_url)
        
        # Extract articles from feed entries
        for entry in feed.entries[:10]:  # Get latest 10 articles
            article = {
                "title": entry.get("title", "No title"),
                "content": entry.get("summary", entry.get("description", "No content available")),
                "source": source_name,
                "url": entry.get("link", ""),
                "published_date": None,
                "category": category,
                "image_url": None
            }
            
            # Try to get published date (convert to string for JSON compatibility)
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    dt = datetime(*entry.published_parsed[:6])
                    article["published_date"] = dt.isoformat()  # ← FIXED: Convert to string
                except:
                    pass
            
            # Try to get image
            if hasattr(entry, 'media_content') and entry.media_content:
                article["image_url"] = entry.media_content[0].get('url', None)
            elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                article["image_url"] = entry.media_thumbnail[0].get('url', None)
            
            # Clean the content (remove HTML tags)
            article["content"] = clean_html(article["content"])
            
            articles.append(article)
        
        print(f"✅ Scraped {len(articles)} articles from {source_name}")
        return articles
        
    except Exception as e:
        print(f"❌ Error scraping {source_name}: {e}")
        return []

def clean_html(html_text: str) -> str:
    """
    Remove HTML tags and clean text
    """
    if not html_text:
        return ""
    
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    
    # Limit content to 500 characters for summary
    if len(text) > 500:
        text = text[:497] + "..."
    
    return text

def scrape_multiple_sources(category: str = "all") -> List[Dict]:
    """
    Scrape from multiple news sources
    """
    all_articles = []
    
    # Define RSS feeds for different sources
    feeds = {
        "technology": [
            ("https://techcrunch.com/feed/", "TechCrunch"),
            ("https://www.theverge.com/rss/index.xml", "The Verge"),
        ],
        "general": [
            ("http://rss.cnn.com/rss/cnn_topstories.rss", "CNN"),
            ("http://feeds.bbci.co.uk/news/rss.xml", "BBC News"),
        ],
        "business": [
            ("https://feeds.bloomberg.com/markets/news.rss", "Bloomberg"),
        ]
    }
    
    # Determine which feeds to scrape
    if category == "all":
        sources_to_scrape = []
        for cat_feeds in feeds.values():
            sources_to_scrape.extend([(url, name, "general") for url, name in cat_feeds])
    elif category in feeds:
        sources_to_scrape = [(url, name, category) for url, name in feeds[category]]
    else:
        print(f"❌ Unknown category: {category}")
        return []
    
    # Scrape each source
    for feed_url, source_name, cat in sources_to_scrape:
        articles = scrape_rss_feed(feed_url, source_name, cat)
        all_articles.extend(articles)
    
    print(f"🎉 Total articles scraped: {len(all_articles)}")
    return all_articles

# For testing
if __name__ == "__main__":
    print("Testing scraper...")
    articles = scrape_multiple_sources("technology")
    
    if articles:
        print(f"\n📰 Sample article:")
        print(f"Title: {articles[0]['title']}")
        print(f"Source: {articles[0]['source']}")
        print(f"Content: {articles[0]['content'][:100]}...")