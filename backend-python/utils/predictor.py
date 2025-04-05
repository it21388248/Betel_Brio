import pandas as pd
import joblib
import os

# --- Model Paths (adjust paths to your environment if needed) ---
PRICE_MODEL_PATH = "./kavindi/price/betal_price_prediction_model.pkl"
PRICE_ENCODER_PATH = "./kavindi/price/betel_label_encoders.pkl"
PRICE_PREPROCESSOR_PATH = "./kavindi/price/betel_preprocessing.pkl"

DEMAND_MODEL_PATH = "./kavindi/demand/betel_location_prediction_model.pkl"
DEMAND_ENCODER_PATH = "./kavindi/demand/betel_label_encoders.pkl"
DEMAND_SCALER_PATH = "./kavindi/demand/demand_preprocessor.pkl"

MARKET_MODEL_PATH = "./kavindi/market/betel_insights_model_enhanced.pkl"
MARKET_ENCODER_PATH = "./kavindi/market/betel_insights_encoders.pkl"

# --- Load Models ---
try:
    price_model = joblib.load(PRICE_MODEL_PATH)
    price_encoders = joblib.load(PRICE_ENCODER_PATH)
    price_preprocessor = joblib.load(PRICE_PREPROCESSOR_PATH)
except Exception as e:
    raise RuntimeError(f"❌ Error loading price prediction resources: {str(e)}")

try:
    demand_model = joblib.load(DEMAND_MODEL_PATH)
    demand_encoders = joblib.load(DEMAND_ENCODER_PATH)
    demand_scaler = joblib.load(DEMAND_SCALER_PATH)
    numeric_columns = ['Month', 'No_of_Leaves']
except Exception as e:
    raise RuntimeError(f"❌ Error loading demand prediction resources: {str(e)}")

try:
    market_model = joblib.load(MARKET_MODEL_PATH)
    market_encoders = joblib.load(MARKET_ENCODER_PATH)
except Exception as e:
    raise RuntimeError(f"❌ Error loading market prediction resources: {str(e)}")


# --- Predict Price per Leaf ---
def predict_price(date, leaf_type, leaf_size, quality_grade, no_of_leaves, location, season):
    try:
        month = pd.to_datetime(date).month
        features = [[
            month,
            price_encoders['Leaf_Type'].transform([leaf_type])[0],
            price_encoders['Leaf_Size'].transform([leaf_size])[0],
            price_encoders['Quality_Grade'].transform([quality_grade])[0],
            no_of_leaves,
            price_encoders['Location'].transform([location])[0],
            price_encoders['Season'].transform([season])[0]
        ]]
        price = price_model.predict(features)[0]
        return f"{round(price * 2) / 2:.2f}"
    except Exception as e:
        print("❌ Error in predict_price:", str(e))
        raise


# --- Predict Best Demand Location ---
def predict_demand_location(date, no_of_leaves, leaf_type, leaf_size, quality_grade):
    try:
        month = pd.to_datetime(date).month
        features = pd.DataFrame([[
            month,
            no_of_leaves,
            demand_encoders['Leaf_Type'].transform([leaf_type])[0],
            demand_encoders['Leaf_Size'].transform([leaf_size])[0],
            demand_encoders['Quality_Grade'].transform([quality_grade])[0]
        ]], columns=['Month', 'No_of_Leaves', 'Leaf_Type', 'Leaf_Size', 'Quality_Grade'])
        features[numeric_columns] = demand_scaler.transform(features[numeric_columns])
        pred = demand_model.predict(features)[0]
        return demand_encoders['Location'].inverse_transform([pred])[0]
    except Exception as e:
        print("❌ Error in predict_demand_location:", str(e))
        raise


# --- Predict Best Market (NEW) ---
def predict_best_market(date, no_of_leaves, leaf_type, leaf_size, quality_grade):
    try:
        month = pd.to_datetime(date).month
        features = pd.DataFrame([[
            month,
            no_of_leaves,
            market_encoders['Leaf_Type'].transform([leaf_type])[0],
            market_encoders['Leaf_Size'].transform([leaf_size])[0],
            market_encoders['Quality_Grade'].transform([quality_grade])[0]
        ]], columns=['Month', 'No_of_Leaves', 'Leaf_Type', 'Leaf_Size', 'Quality_Grade'])
        location_encoded = market_model.predict(features)[0]
        return market_encoders['Location'].inverse_transform([location_encoded])[0]
    except Exception as e:
        print("❌ Error in predict_best_market:", str(e))
        raise
