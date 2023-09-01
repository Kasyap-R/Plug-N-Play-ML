from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UploadedFile
import requests
from backend_api.constants import TRAIN_TABULAR_MODEL, MODEL_NAME_KEY, TARGET_COLUMN_NAME_KEY, FILE_KEY, PROBLEM_TYPE_KEY

# TODO: MAKE BACKEND SEND RESPONSE IMMEDIATELY AND WAIT UPON COMPLETION FROM WORKER
@api_view(['POST'])
def train_model(request):
    if not request.FILES:
        return Response({'error': 'No files were uploaded'}, status=400)
    
    model_name = request.POST.get(MODEL_NAME_KEY)
    target_column_name = request.POST.get(TARGET_COLUMN_NAME_KEY)
    problem_type = request.POST.get(PROBLEM_TYPE_KEY)
    
    uploaded_file = UploadedFile.objects.create(file=request.FILES[FILE_KEY])
    uploaded_file_path = uploaded_file.file.path

    with open(uploaded_file_path, 'rb') as f:
        response = requests.post(TRAIN_TABULAR_MODEL,
                                 files = {FILE_KEY: f},
                                 data={MODEL_NAME_KEY: model_name, TARGET_COLUMN_NAME_KEY: target_column_name, PROBLEM_TYPE_KEY: problem_type})
        
    flask_response = response.json()

    return Response(flask_response, status=200)
