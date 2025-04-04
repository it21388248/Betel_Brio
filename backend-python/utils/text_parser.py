def extract_features_from_text(text):
    # Dummy example – in real case, use NLP or keyword mapping
    # Expecting something like: "Season is Yala, type is premium, price is 2.5"
    features = []

    if "kuliyapitiya" in text.lower():
        features.append(1)
    else:
        features.append(0)

    if "premium" in text.lower():
        features.append(1)
    else:
        features.append(0)

    if "yala" in text.lower():
        features.append(1)
    else:
        features.append(0)

    if "2.5" in text:
        features.append(2.5)
    else:
        features.append(1.5)

    return [features]  # Wrapped in list for sklearn predict
