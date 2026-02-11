#!/usr/bin/env python3
import pymongo
import certifi

# Your connection string
MONGO_URL = "mongodb+srv://news-admin:portal123@news-portal-cluster.wewfhkc.mongodb.net/?retryWrites=true&w=majority"

print("Testing MongoDB Atlas connection...\n")
print(f"Python version: {__import__('sys').version}")
print(f"PyMongo version: {pymongo.__version__}")
print(f"Certifi location: {certifi.where()}\n")

print("=" * 60)

# Test 1: Basic connection
print("\n🧪 TEST 1: Basic connection...")
try:
    client = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ PASSED: Basic connection works!")
    client.close()
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 2: With certifi
print("\n🧪 TEST 2: Connection with certifi SSL...")
try:
    client = pymongo.MongoClient(
        MONGO_URL,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )
    client.admin.command('ping')
    print("✅ PASSED: Certifi SSL works!")
    client.close()
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 3: With SSL disabled (insecure but tests connectivity)
print("\n🧪 TEST 3: Connection with TLS verification disabled...")
try:
    client = pymongo.MongoClient(
        MONGO_URL + "&tlsAllowInvalidCertificates=true",
        serverSelectionTimeoutMS=5000
    )
    client.admin.command('ping')
    print("✅ PASSED: Connection works with TLS disabled!")
    
    # Try to actually use it
    db = client['news_portal']
    collection = db['test']
    collection.insert_one({"test": "data"})
    print("✅ PASSED: Can insert data!")
    collection.delete_one({"test": "data"})
    print("✅ PASSED: Can delete data!")
    
    client.close()
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n" + "=" * 60)
print("\n📊 DIAGNOSIS:")