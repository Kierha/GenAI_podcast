# test_generate.py — Lance la génération audio complète du podcast

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generate_audio import run_audio_pipeline

if __name__ == "__main__":
    print("🚀 Lancement du pipeline de génération audio...")
    run_audio_pipeline()
    print("🎧 Fichier final prêt dans output/final_podcast.mp3")