# generate_audio.py — Génère le podcast audio final à partir du script texte

import os
import re
import time
import requests
from pydub import AudioSegment
from dotenv import load_dotenv

# Charger les clés et IDs de voix depuis .env
load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_NOE_ID = os.getenv("VOICE_NOE_ID")
VOICE_LINA_ID = os.getenv("VOICE_LINA_ID")

API_URL = "https://api.elevenlabs.io/v1/text-to-speech/"
HEADERS = {
    "xi-api-key": ELEVEN_API_KEY,
    "Content-Type": "application/json"
}

# Associer les noms aux voix
SPEAKER_MAP = {
    "Noé": VOICE_NOE_ID,
    "Lina": VOICE_LINA_ID
}

# Répertoire de sortie audio
os.makedirs("output/audio_parts", exist_ok=True)

def parse_script(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    dialogue = []
    for line in lines:
        match = re.match(r"\*\*(.*?)\*\*.*?:\s*(.*)", line.strip())
        if match:
            speaker, text = match.groups()
            if speaker in SPEAKER_MAP:
                dialogue.append({"speaker": speaker, "text": text})
    return dialogue

def generate_audio_snippet(speaker, text, index):
    voice_id = SPEAKER_MAP[speaker]
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.8}
    }
    print(f"🎙️ Génération : {speaker} (ligne {index})")

    response = requests.post(
        API_URL + voice_id,
        headers=HEADERS,
        json=payload
    )
    response.raise_for_status()
    filename = f"output/audio_parts/{index:02d}_{speaker}.mp3"
    with open(filename, "wb") as f:
        f.write(response.content)
    time.sleep(1.2)  # Évite les limites d'API
    return filename

def assemble_audio(snippet_paths, output_path="output/final_podcast.mp3"):
    final_audio = AudioSegment.empty()
    for path in snippet_paths:
        segment = AudioSegment.from_mp3(path)
        final_audio += segment + AudioSegment.silent(duration=300)  # petite pause entre répliques
    final_audio.export(output_path, format="mp3")
    print(f"✅ Podcast final exporté : {output_path}")

def run_audio_pipeline():
    print("🔍 Parsing du script...")
    dialogue = parse_script("output/podcast_ready.txt")
    if not dialogue:
        print("❌ Aucun dialogue trouvé dans le fichier.")
        return

    snippet_paths = []
    for i, entry in enumerate(dialogue):
        path = generate_audio_snippet(entry["speaker"], entry["text"], i)
        snippet_paths.append(path)

    print("🔊 Assemblage de l'audio...")
    assemble_audio(snippet_paths)

if __name__ == "__main__":
    run_audio_pipeline()