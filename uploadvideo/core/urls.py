from django.urls import path
from .views import upload_video, store_video

urlpatterns = [
    path('upload-backblaze/', upload_video), # --> Endpoint for Backblaze upload
    path('upload-bunny/', store_video), # --> Endpoint for Bunny CDN storage
]
