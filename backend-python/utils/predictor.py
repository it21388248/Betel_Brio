import pandas as pd
import joblib
import os

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Price Prediction Resources ---
PRICE_MODEL_PATH = os.path.join(BASE_DIR, "kavindi", "price", "betal_price_prediction_model.pkl")
PRICE_ENCODER_PATH = os.path.join(BASE_DIR, "kavindi", "price", "betel_label_encoders.pkl")
PRICE_PREPROCESSOR_PATH = os.path.join(BASE_DIR, "kavindi", "price", "betel_preprocessing.pkl")

# --- Demand Prediction Resources ---
DEMAND_MODEL_PATH = os.path.join(BASE_DIR, "kavindi", "demand", "betel_location_prediction_model.pkl")
DEMAND_ENCODER_PATH = os.path.join(BASE_DIR, "kavindi", "demand", "betel_label_encoders.pkl")
DEMAND_SCALER_PATH = os.path.join(BASE_DIR, "kavindi", "demand", "demand_preprocessor.pkl")

# --- Load Price Prediction Components ---
try:
    price_model = joblib.load(PRICE_MODEL_PATH)
    price_encoders = joblib.load(PRICE_ENCODER_PATH)
    price_preprocessor = joblib.load(PRICE_PREPROCESSOR_PATH)
except Exception as e:
    raise RuntimeError(f"❌ Error loading price prediction resources: {str(e)}")

# --- Load Demand Prediction Components ---
try:
    demand_model = joblib.load(DEMAND_MODEL_PATH)
    demand_encoders = joblib.load(DEMAND_ENCODER_PATH)
    demand_scaler = joblib.load(DEMAND_SCALER_PATH)
    numeric_columns = ['Month', 'No_of_Leaves']  # update this if your scaler uses more/less
except Exception as e:
    raise RuntimeError(f"❌ Error loading demand prediction resources: {str(e)}")

# --- Price Prediction Function ---
def predict_price(date, leaf_type, leaf_size, quality_grade, no_of_leaves, location, season):
    try:
        month = pd.to_datetime(date).month

        encoded_leaf_type = price_encoders['Leaf_Type'].transform([leaf_type])[0]
        encoded_leaf_size = price_encoders['Leaf_Size'].transform([leaf_size])[0]
        encoded_quality_grade = price_encoders['Quality_Grade'].transform([quality_grade])[0]
        encoded_location = price_encoders['Location'].transform([location])[0]
        encoded_season = price_encoders['Season'].transform([season])[0]

        features = [[
            month,
            encoded_leaf_type,
            encoded_leaf_size,
            encoded_quality_grade,
            no_of_leaves,
            encoded_location,
            encoded_season
        ]]

        predicted_price = price_model.predict(features)[0]
        rounded_price = round(predicted_price * 2) / 2
        return f"{rounded_price:.2f}"

    except Exception as e:
        print("❌ Error inside predict_price:", str(e))
        raise

# --- Demand Location Prediction Function ---
def predict_demand_location(date, no_of_leaves, leaf_type, leaf_size, quality_grade):
    try:
        month = pd.to_datetime(date).month

        encoded_leaf_type = demand_encoders['Leaf_Type'].transform([leaf_type])[0]
        encoded_leaf_size = demand_encoders['Leaf_Size'].transform([leaf_size])[0]
        encoded_quality_grade = demand_encoders['Quality_Grade'].transform([quality_grade])[0]

        features = pd.DataFrame([[month, no_of_leaves, encoded_leaf_type, encoded_leaf_size, encoded_quality_grade]],
                                columns=['Month', 'No_of_Leaves', 'Leaf_Type', 'Leaf_Size', 'Quality_Grade'])

        # Scale numeric columns
        features[numeric_columns] = demand_scaler.transform(features[numeric_columns])

        # Predict encoded location and inverse transform
        location_encoded = demand_model.predict(features)[0]
        location = demand_encoders['Location'].inverse_transform([location_encoded])[0]

        return location

    except Exception as e:
        print("❌ Error inside predict_demand_location:", str(e))
        raise
