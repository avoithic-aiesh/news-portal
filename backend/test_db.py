import sys
from database import connect_to_mongodb, get_news_collection

print("=" * 50)
print("TESTING MONGODB CONNECTION")
print("=" * 50)

# Test connection
db = connect_to_mongodb()

if db is not None:  # ← CHANGED: was "if db:", now "if db is not None:"
    print("\n✅ Step 1: Database connected successfully!")
    
    # Get news collection
    news_collection = get_news_collection()
    print("✅ Step 2: Got news collection")
    
    # Insert a test document
    test_article = {
        "title": "Test Article - MongoDB Works!",
        "content": "This is a test article to verify MongoDB connection",
        "source": "Test Source",
        "category": "test"
    }
    
    print("\n📝 Step 3: Inserting test article...")
    result = news_collection.insert_one(test_article)
    print(f"✅ Test article inserted with ID: {result.inserted_id}")
    
    # Retrieve it
    print("\n🔍 Step 4: Retrieving test article...")
    found = news_collection.find_one({"title": "Test Article - MongoDB Works!"})
    if found:
        print(f"✅ Found article: '{found['title']}'")
        print(f"   Content: {found['content']}")
        print(f"   Source: {found['source']}")
    
    # Count documents
    count = news_collection.count_documents({})
    print(f"\n📊 Total articles in database: {count}")
    
    # Clean up test article
    print("\n🧹 Step 5: Cleaning up test article...")
    news_collection.delete_one({"_id": result.inserted_id})
    print("✅ Test article deleted")
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED! MongoDB is working perfectly!")
    print("=" * 50)
else:
    print("\n❌ Failed to connect to database")
    print("\nTroubleshooting:")
    print("1. Check your .env file exists in the news-portal folder")
    print("2. Verify MONGODB_URL in .env has your correct password")
    print("3. Make sure you replaced <password> with actual password")
    print("4. Check MongoDB Atlas Network Access allows your IP")
    sys.exit(1)