from pyairtable import Table
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "Reports"

table = Table(API_KEY, BASE_ID, TABLE_NAME)

def save_report(query=None, response=None, prediction=None):
    """
    Saves a chatbot interaction or a price prediction to Airtable.
    
    :param query: Optional user query text
    :param response: Optional chatbot response text
    :param prediction: Either a dict of prediction fields, or a single price (float/int)
    """
    record = {}

    if query and response:
        record["Query"] = query
        record["Response"] = response

    if isinstance(prediction, dict):
        clean_prediction = {}
        for key, value in prediction.items():
            if key == "No_of_Leaves":
                clean_prediction[key] = int(value)  # ensure it's int
            elif key == "Predicted_Price":
                clean_prediction[key] = float(value)  # ensure it's float
            else:
                clean_prediction[key] = str(value).strip()  # keep as string
        record.update(clean_prediction)

    elif isinstance(prediction, (int, float)):
        record["Predicted_Price"] = float(prediction)

    # ✅ Optional: Log the payload for debugging
    print("📤 Airtable payload:", record)

    return table.create(record)
