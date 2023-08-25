from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UploadedFile

@api_view(['POST'])
def train_model(request):
    if not request.FILES:
        return Response({'error': 'No files were uploaded'}, status=400)
    
    model_name = request.POST.get('model')
    for file in request.FILES.getlist('file'):
        UploadedFile.objects.create(file=file)

    return Response({'message': f'Your {model_name} is being trained!'})
