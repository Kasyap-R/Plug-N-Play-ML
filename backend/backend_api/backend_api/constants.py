# Worker Endpoints
TRAIN_TABULAR_MODEL = "http://localhost:5000/worker/v1/train_model/tabular"

# Request Body Keys
# NOTE: KEEP THESE IN SYNC WITH THE KEYS DEFINED IN THE FRONT-END AND WORKER
MODEL_NAME_KEY = 'model_type'
TARGET_COLUMN_NAME_KEY = 'target_column'
FILE_KEY = 'file'
PROBLEM_TYPE_KEY = 'problem_type'

# Problem Types
# NOTE: KEEP THESE IN SYNC WITH THE KEYS DEFINED IN THE FRONT-END AND WORKER
REGRESSION = 'Regression'
CLASSIFICATOIN = 'Classification'