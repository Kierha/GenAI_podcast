# format_podcast.py — Réécriture orale adaptée au podcast 🎙️ + debug logging

import os
from openai import OpenAI
from dotenv import load_dotenv

# Charger la clé OpenRouter depuis .env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

# Prompt de reformulation podcast
PROMPT_TEMPLATE = """
Tu es un assistant éditorial spécialisé dans l'adaptation de scripts en version podcast immersif et naturel.

Voici un débat entre deux intervenants, Noé (rationnel, sarcastique) et Lina (créative, provocante).

Ta mission :
- Réécris ce débat dans un style **oral, dynamique et fluide**, comme s'il était **joué par deux vraies voix dans un podcast francophone**.
- Garde **exactement les mêmes idées**, mais améliore **le rythme, les relances, les émotions**.
- Utilise des phrases **plus courtes**, des expressions familières si pertinent, et ajoute **des respirations, des relances**, voire des réactions entre les deux (soupirs, sarcasmes, interruptions polies, etc).
- Tu peux ajouter des touches **d’humour ou d’ironie**, en cohérence avec les personnalités.
- Termine après la dernière réplique sans ajouter de résumé ni de conclusion automatique.

Voici le débat à reformuler :

---
{debate_text}
---

Réécris maintenant le script dans ce format fluide et immersif :
"""

def format_podcast_script(debate_text: str) -> str:
    full_prompt = PROMPT_TEMPLATE.format(debate_text=debate_text)
    # print("🔍 full_prompt : " + full_prompt)

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": full_prompt}
            ],
            extra_headers={
                "HTTP-Referer": "https://yourapp.com",
                "X-Title": "GenAI Podcast"
            },
            extra_body={}
        )

        # Debug brut
        # print(" Contenu brut de la réponse:")
        # print(completion)

        if not completion.choices or not completion.choices[0].message.content:
            print("⚠️ Réponse vide ou invalide.")
            return ""

        final_script = completion.choices[0].message.content.strip()

        os.makedirs("output", exist_ok=True)
        with open("output/podcast_ready.txt", "w", encoding="utf-8") as f:
            f.write(final_script)

        print("✅ Script podcast généré et sauvegardé dans output/podcast_ready.txt")
        return final_script

    except Exception as e:
        print("❌ Erreur lors de l'appel à l'API ou de l'accès à la réponse :", e)
        return ""