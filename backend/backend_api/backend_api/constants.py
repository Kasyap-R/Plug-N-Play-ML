# Worker Endpoints
TRAIN_TABULAR_MODEL = "http://localhost:5000/worker/v1/train_model/tabular"

# Request Body Keys
# NOTE: KEEP THESE IN SYNC WITH THE KEYS DEFINED IN THE FRONT-END AND WORKER
MODEL_NAME_KEY = 'model_type'
TARGET_COLUMN_NAME_KEY = 'target-column'
FILE_KEY = 'file'
