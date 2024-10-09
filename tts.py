from google.cloud import texttospeech
import os

# Google의 Cloud Text-to-Speech API 사용 설정
credential_path = "./blissful-link-416007-68047a1d5003.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def tts(text):
    client = texttospeech.TextToSpeechClient()

    max_length = 400    

    # 문장 단위로 나누기
    words = text.split('. ')
    sentences = []
    current_sentence = ''
    for word in words:
        if len(current_sentence + word) <= max_length:
            current_sentence += word + ' '
        else:
            sentences.append(current_sentence.strip() + '.')
            current_sentence = word + ' '
    if current_sentence:
        sentences.append(current_sentence.strip() + '.')

    
    audio_data = []

    # 각각의 문장에 대해 payload 설정 후 전송
    for sentence in sentences:
        input_text = texttospeech.SynthesisInput(text=sentence)

        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Neural2-C",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        audio_data.append(response.audio_content)
  
    audio_data = b"".join(audio_data)
    
    print("tts ready")
    return audio_data