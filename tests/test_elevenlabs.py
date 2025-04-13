import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Chargement des clés API
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
voice_id = os.getenv("VOICE_NOE_ID")

if not api_key or not voice_id:
    raise ValueError("❌ Clé API ou Voice ID manquant dans le .env")

print(f"Clé API : {api_key}")  # Ajout de cette ligne
print(f"Voice ID : {voice_id}") # Ajout de cette ligne

# Initialiser le client
client = ElevenLabs(api_key=api_key)

# Génération audio (flux audio streamé)
audio_stream = client.text_to_speech.convert(
    text="Bonjour, ceci est un test avec la voix ElevenLabs.",
    voice_id=voice_id,
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128"
)

# Écrire le flux audio dans un fichier
os.makedirs("output", exist_ok=True)
audio_path = "output/test_voice.mp3"

with open(audio_path, "wb") as audio_file:
    for chunk in audio_stream:
        if chunk:
            audio_file.write(chunk)

print(f"✅ Audio généré avec succès : {audio_path}")
