import os
import re
import random
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

# Charger les variables d'environnement
load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_NOE_ID = os.getenv("VOICE_NOE_ID")
VOICE_LINA_ID = os.getenv("VOICE_LINA_ID")

if not ELEVEN_API_KEY:
    raise ValueError("Clé ElevenLabs non trouvée dans .env (ELEVENLABS_API_KEY)")

client = ElevenLabs(api_key=ELEVEN_API_KEY)

SPEAKER_MAP = {
    "Noé": VOICE_NOE_ID,
    "Lina": VOICE_LINA_ID
}

os.makedirs("output/audio_parts", exist_ok=True)

def parse_script(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    dialogue = []
    for line in lines:
        match = re.match(r"\*\*(.*?)\*\*.*?:\s*<speak>(.*?)</speak>", line.strip())
        if match:
            speaker, ssml_text = match.groups()
            if speaker in SPEAKER_MAP:
                dialogue.append({"speaker": speaker, "text": f"<speak>{ssml_text}</speak>"})
    return dialogue

def generate_audio_snippet(speaker, ssml_text, index):
    voice_id = SPEAKER_MAP[speaker]
    print(f"🎙️ Génération : {speaker} (ligne {index})")

    audio_stream = client.text_to_speech.convert(
        text=ssml_text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )

    filename = f"output/audio_parts/{index:02d}_{speaker}.mp3"
    with open(filename, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)
    return filename

def assemble_audio(snippet_paths, output_path="output/final_podcast.mp3"):
    final_audio = AudioSegment.empty()
    for i, path in enumerate(snippet_paths):
        segment = AudioSegment.from_mp3(path)
        final_audio += segment

        if i < len(snippet_paths) - 1:
            pause_duration = random.randint(300, 600)
            final_audio += AudioSegment.silent(duration=pause_duration)

    final_audio.export(output_path, format="mp3")
    print(f"✅ Podcast final exporté : {output_path}")

def run_audio_pipeline():
    print("🚀 Lancement du pipeline de génération audio...")
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
