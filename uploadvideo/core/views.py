from django.http import JsonResponse
from .utils import upload_video_to_b2
import os
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt # Use it in development only
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']
        temp_path = f"/tmp/{video.name}"

        with open(temp_path, 'wb+') as f:
            for chunk in video.chunks():
                f.write(chunk)

        object_name = f"videos/{video.name}"
        url = upload_video_to_b2(temp_path, object_name)

        os.remove(temp_path)
        return JsonResponse({'url': url})
    
    return JsonResponse({'error': 'No se recibió ningún archivo'}, status=400)
