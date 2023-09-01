from flask import Flask, request, jsonify
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler

import pickle
import base64

from constants import TARGET_COLUMN_NAME_KEY, MODEL_NAME_KEY, FILE_KEY, PROBLEM_TYPE_KEY, REGRESSION, CLASSIFICATION

app = Flask(__name__)

@app.route('/worker/v1/train_model/tabular/', methods=['POST'])
def process_training():
    file = request.files[FILE_KEY]
    model_type = request.form.get(MODEL_NAME_KEY)
    target_column = request.form.get(TARGET_COLUMN_NAME_KEY)
    problem_type = request.form.get(PROBLEM_TYPE_KEY)
    print(problem_type)
    X, y = load_data(file, target_column)
    X, y = process_data(X, y, problem_type) 
    X_train, y_train, X_test, y_test = split_data(X, y)
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
    
    return X, y


def process_data(X, y, problem_type):
    X = remove_duplicate_rows(X, y)
    X = remove_unique_columns(X)
    X, y = remove_rows_with_missing_target(X, y)
    X = imputate_data(X)
    
    X = encode_categorical_cols(X)
    X = normalize_data(X)
    y = encode_target_column(y, problem_type)
    return X, y


def imputate_data(X):
    # Impute numerical columns with mean
    num_cols = X.select_dtypes(include=['number']).columns
    imputer_num = SimpleImputer(strategy='mean')
    X[num_cols] = imputer_num.fit_transform(X[num_cols])

    # Impute categorical columns with mode
    cat_cols = X.select_dtypes(include=['object']).columns
    imputer_cat = SimpleImputer(strategy='most_frequent')
    if len(cat_cols) >= 1:
        X[cat_cols] = imputer_cat.fit_transform(X[cat_cols])
    return X


def remove_duplicate_rows(X, y):
    before_rows = len(X)
    X = X.drop_duplicates()
    after_rows = len(X)
    # If rows were dropped, we should drop the corresponding labels as well
    if before_rows != after_rows:
        y = y.loc[X.index]
        
    return X, y


def remove_unique_columns(X):
    """
    Removes columns where each row has a unique value.
    """
    columns_to_remove = []
    for column in X.columns:
        if X[column].nunique() == len(X):
            columns_to_remove.append(column)
    return X.drop(columns=columns_to_remove)


def remove_rows_with_missing_target(X, y):
    mask = y.isna()
    X = X.loc[~mask]
    y = y.dropna()
    return X, y


def normalize_data(X):
    num_cols = X.select_dtypes(include=['number']).columns
    scaler = MinMaxScaler()
    X[num_cols] = scaler.fit_transform(X[num_cols])
    return X


def encode_categorical_cols(X):
    categorical_cols = X.select_dtypes(include=['object']).columns
    X = pd.get_dummies(X, columns=categorical_cols)
    return X

def encode_target_column(y, problem_type):
    le = LabelEncoder()
    if problem_type == REGRESSION:
        #No encoding is needed for regression problems
        return y
    
    if problem_type == CLASSIFICATION:
        # Encode string labels into integers for classification problems
        y = le.fit_transform(y)
        return y
    
    raise ValueError("Invalid problem_type: Must be either 'regression' or 'classification'")

def split_data(X, y):
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