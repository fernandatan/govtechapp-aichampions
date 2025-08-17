import subprocess
import os

print("🚀 Running GovTech Assistant Backend Pipeline...\n")

# Step 1: Scrape product URLs
print("🔍 Step 1: Scraping product URLs...")
subprocess.run(["python", "ingest/scrape_product_urls.py"], check=True)

# Step 2: Ingest pages into ChromaDB
print("\n📚 Step 2: Ingesting product pages into vector DB...")
subprocess.run(["python", "ingest/ingest_docs.py"], check=True)

# Step 3: Launch Streamlit app directly
print("\n🖥️  Launching Streamlit UI...")

# Get PORT from environment
port = os.environ.get("PORT", "3000")

subprocess.run([
    "streamlit", "run", "app/app.py",
    "--server.port", port,
    "--server.address", "0.0.0.0",
    "--server.headless", "true"
], check=True)
