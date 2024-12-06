from rest_framework import serializers
from .models import AudioFile

class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['id', 'audio', 'transcription', 'created_at']



def validate_audio(self, value):
    if not value.name.endswith(('.wav', '.flac')):
        raise serializers.ValidationError("Somente arquivos .wav ou .flac são permitidos.")
    return value


class TextToAudioSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500)
    language = serializers.ChoiceField(choices=[('en', 'English'), ('pt', 'Portuguese')], default='pt')