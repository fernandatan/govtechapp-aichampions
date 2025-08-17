import subprocess
import os

print("🚀 Running GovTech Assistant Backend Pipeline...\n")

# Step 1: Scrape product URLs
print("🔍 Step 1: Scraping product URLs...")
subprocess.run(["python", "ingest/scrape_product_urls.py"], check=True)

# Step 2: Ingest pages into ChromaDB
print("\n📚 Step 2: Ingesting product pages into vector DB...")
subprocess.run(["python", "ingest/ingest_docs.py"], check=True)

# (Optional) Step 3: Launch Streamlit app
launch_ui = input("\n💬 Launch Streamlit chatbot now? (y/n): ").strip().lower()
if launch_ui == "y":
    print("\n🖥️  Launching Streamlit UI...")
    subprocess.run(["streamlit", "run", "app/app.py"], check=True)
else:
    print("✅ Backend pipeline complete.")
