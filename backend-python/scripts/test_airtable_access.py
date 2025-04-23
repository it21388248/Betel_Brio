import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set variables
API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")  # e.g., "apppmI2UdPvmRgqO4"
TABLE_NAME = "Reports"  # Make sure this matches exactly

# Airtable API endpoint
url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# Set headers
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Send GET request to test access
response = requests.get(url, headers=headers)

# Output result
if response.status_code == 200:
    print("✅ Success! Token has access to the base and table.")
else:
    print(f"❌ Error: {response.status_code}")
    try:
        print("📨 Message:", response.json())
    except Exception:
        print("⚠️ Could not parse JSON response.")
