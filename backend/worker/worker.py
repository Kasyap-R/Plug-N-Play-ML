from flask import Flask, request, jsonify
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle
import base64

from constants import TARGET_COLUMN_NAME_KEY, MODEL_NAME_KEY, FILE_KEY

app = Flask(__name__)

@app.route('/worker/v1/train_model/tabular/', methods=['POST'])
def process_training():
    file = request.files[FILE_KEY]
    model_type = request.form.get(MODEL_NAME_KEY)
    target_column = request.form.get(TARGET_COLUMN_NAME_KEY)

    X_train, y_train, X_test, y_test = load_data(file, target_column)
    model = train_model(X_train, y_train, model_type)
    accuracy = validate_model(model, X_test, y_test)

    binary_model = pickle.dumps(model)  # Serialize the model to a binary format
    encoded_model = base64.b64encode(binary_model).decode('utf-8')  # Encode to base64 for easy JSON serialization

    result = {
        MODEL_NAME_KEY: model_type,
        'message': f"Trained {model_type} model successfully",
        "model": encoded_model,  # sending the encoded model as a string
        'accuracy': accuracy
    }

    return jsonify(result), 200


def load_data(file, target_column):
    data = pd.read_excel(file)
    X = data.drop(columns=[target_column])
    y = data.loc[:, target_column]

    # Use LabelEncoder to convert string labels to integers
    le = LabelEncoder()
    y = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, y_train, X_test, y_test

def train_model(X_train, y_train, model_type):
    if model_type == 'xgboost':
        model = xgb.XGBClassifier()
        model.fit(X_train, y_train)
        return model
    else:
        raise ValueError("Unsupported model type!")

def validate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)