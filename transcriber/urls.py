from django.urls import path
from .views import AudioToTextView, TextToAudioView

urlpatterns = [
    path('transcribe/', AudioToTextView.as_view(), name='audio-to-text'),
    path('text-to-audio/', TextToAudioView.as_view(), name='text-to-audio'),
]
