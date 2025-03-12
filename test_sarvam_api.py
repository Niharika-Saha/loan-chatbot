import os
import requests

# Load API key from environment variable
api_key = os.getenv("SARVAM_API_KEY")  # ✅ Ensure this is set in your environment

def speech_to_text(api_key, file_path, language_code="hi-IN"):
    url = "https://api.sarvam.ai/speech-to-text"
    payload = {
        'model': 'saarika:v1',
        'language_code': language_code,
        'with_timesteps': 'false'
    }
    
    headers = {'api-subscription-key': api_key}
    
    with open(file_path, 'rb') as audio_file:
        files = {'file': ('sample_audio1.wav', audio_file, 'audio/wav')}
        response = requests.post(url, headers=headers, data=payload, files=files)
    
    try:
        data = response.json()
        print("Speech-to-Text Response:", data)
        return data.get("transcript", "No transcription found")
    except Exception as e:
        print("Error parsing Speech-to-Text response:", e)
        return None

def speech_to_text_translate(api_key, file_path, model="saaras:v1", prompt=""):
    url = "https://api.sarvam.ai/speech-to-text-translate"
    payload = {'model': model, 'prompt': prompt}
    
    headers = {'api-subscription-key': api_key}
    
    with open(file_path, 'rb') as audio_file:
        files = {'file': ('sample_audio1.wav', audio_file, 'audio/wav')}
        response = requests.post(url, headers=headers, data=payload, files=files)
    
    try:
        data = response.json()
        print("Speech-to-Text-Translate Response:", data)
        
        # ✅ Check for "transcript" instead of "translated_text"
        translated_text = data.get("transcript") or data.get("translated_text")
        
        if not translated_text:
            return "No translation found"
        
        return translated_text  # ✅ This should now return the English translation correctly
    except Exception as e:
        print("Error parsing Speech-to-Text-Translate response:", e)
        return None


def text_to_speech(api_key, text, target_language_code="hi-IN", speaker="meera", speech_sample_rate=8000, enable_preprocessing=True):
    url = "https://api.sarvam.ai/text-to-speech"
    payload = {
        "inputs": [text],
        "target_language_code": target_language_code,
        "speaker": speaker,
        "speech_sample_rate": speech_sample_rate,
        "enable_preprocessing": enable_preprocessing,
        "model": "bulbul:v1"
    }
    
    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": api_key
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        output_file = "generated_speech.wav"
        with open(output_file, "wb") as f:
            f.write(response.content)  # ✅ Save the audio response as a file
        
        print(f"Generated Speech saved as: {output_file}")
        return output_file  # ✅ Return the file path instead of raw binary
    else:
        print(f"Error in Text-to-Speech API: {response.status_code}, {response.text}")
        return None

# ✅ Example Usage
file_path = "sample_audio1.wav"

# ✅ Ensure API key is correctly loaded
if not api_key:
    raise ValueError("SARVAM_API_KEY is not set. Please set it in your environment.")

# ✅ Process speech-to-text
transcribed_text = speech_to_text(api_key, file_path)
if transcribed_text:
    print("Transcribed Text:", transcribed_text)

# ✅ Process speech-to-text translation
translated_text = speech_to_text_translate(api_key, file_path)
if translated_text:
    print("Translated Text:", translated_text)

# ✅ Process text-to-speech
audio_output = text_to_speech(api_key, "Hello, how are you?")
if audio_output:
    print("Generated Speech File:", audio_output)
