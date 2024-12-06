from rest_framework.views import APIView
from rest_framework.response import Response
from gtts import gTTS
import speech_recognition as sr
from .serializers import TextToAudioSerializer, AudioFileSerializer
import os

class AudioToTextView(APIView):
    def post(self, request):
        serializer = AudioFileSerializer(data=request.data)
        if serializer.is_valid():
            audio_file = serializer.save()
            recognizer = sr.Recognizer()
            audio_path = audio_file.audio.path
            try:
                with sr.AudioFile(audio_path) as source:
                    audio_data = recognizer.record(source)
                    transcription = recognizer.recognize_google(audio_data, language='pt-BR')
                    audio_file.transcription = transcription
                    audio_file.save()
                return Response({'transcription': transcription}, status=200)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)

class TextToAudioView(APIView):
    def post(self, request):
        serializer = TextToAudioSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            language = serializer.validated_data['language']
            try:
                tts = gTTS(text=text, lang=language)
                file_path = f"media/audio_output.mp3"
                tts.save(file_path)
                return Response({'message': 'Áudio gerado!', 'file_url': f'/{file_path}'})
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        return Response(serializer.errors, status=400)
