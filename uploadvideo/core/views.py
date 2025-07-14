from django.http import JsonResponse
from .utils import upload_video_to_b2, upload_video_bunny, create_video_space, generate_url_bunny
import os
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests

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

@csrf_exempt # Use it in development only
def store_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']
        temp_path = f"/tmp/{video.name}"

        with open(temp_path, 'wb+') as f:
            for chunk in video.chunks():
                f.write(chunk)

        try:
            video_id = create_video_space(video.name)
            upload_video_bunny(video_id, temp_path)
            os.remove(temp_path)
            url = generate_url_bunny(video_id)
            return JsonResponse({'url': url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'No se recibió ningún archivo'}, status=400)


        
