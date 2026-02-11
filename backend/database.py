from tinydb import TinyDB, Query
from datetime import datetime
import os

# Use file-based database (no server needed!)
DB_PATH = os.path.join(os.path.dirname(__file__), 'news_database.json')

# Global database instance
db = None
news_table = None
chat_table = None

def connect_to_mongodb():
    """
    Connect to TinyDB database (file-based, no server needed)
    """
    global db, news_table, chat_table
    
    try:
        print(f"🔌 Connecting to database...")
        
        # Create or open database file
        db = TinyDB(DB_PATH)
        
        # Get tables
        news_table = db.table('news_articles')
        chat_table = db.table('chat_history')
        
        print(f"✅ Connected to database: {DB_PATH}")
        print(f"📊 Current articles: {len(news_table)}")
        return db
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def close_mongodb_connection():
    """
    Close database connection
    """
    global db
    if db:
        db.close()
        print("🔌 Database connection closed")

def get_news_collection():
    """
    Get the news articles collection
    """
    global news_table
    if news_table is None:
        connect_to_mongodb()
    
    # Return wrapped version for compatibility
    class CollectionWrapper:
        def __init__(self, table):
            self.table = table
        
        def find(self):
            """Return all documents as a cursor-like object"""
            class Cursor:
                def __init__(self, docs):
                    self.docs = docs
                
                def sort(self, field, direction):
                    # For TinyDB, we'll just return as-is (newest first by default)
                    return self
                
                def limit(self, n):
                    return self.docs[:n] if n > 0 else self.docs
                
                def __iter__(self):
                    return iter(self.docs)
            
            all_docs = self.table.all()
            # Add doc_id as _id for compatibility
            for doc in all_docs:
                if '_id' not in doc:
                    doc['_id'] = str(doc.doc_id)
            return Cursor(all_docs[::-1])  # Reverse to show newest first
        
        def insert_one(self, document):
            """Insert a single document"""
            class Result:
                def __init__(self, doc_id):
                    self.inserted_id = str(doc_id)
            
            doc_id = self.table.insert(document)
            return Result(doc_id)
        
        def insert_many(self, documents):
            """Insert multiple documents"""
            class Result:
                def __init__(self, doc_ids):
                    self.inserted_ids = [str(id) for id in doc_ids]
            
            doc_ids = self.table.insert_multiple(documents)
            return Result(doc_ids)
        
        def delete_one(self, query):
            """Delete one document by _id"""
            class Result:
                def __init__(self, count):
                    self.deleted_count = count
            
            if '_id' in query:
                try:
                    doc_id = int(query['_id'])
                    self.table.remove(doc_ids=[doc_id])
                    return Result(1)
                except:
                    return Result(0)
            return Result(0)
        
        def delete_many(self, query):
            """Delete all documents"""
            count = len(self.table)
            self.table.truncate()
            
            class Result:
                def __init__(self, count):
                    self.deleted_count = count
            
            return Result(count)
        
        def count_documents(self, query):
            """Count documents"""
            return len(self.table)
    
    return CollectionWrapper(news_table)

def get_chat_collection():
    """
    Get the chat history collection
    """
    global chat_table
    if chat_table is None:
        connect_to_mongodb()
    return chat_table