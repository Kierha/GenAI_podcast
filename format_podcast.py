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

PROMPT_TEMPLATE = """
Tu es un assistant éditorial expert dans l’adaptation de débats en **scripts audio immersifs**, joués par deux voix synthétiques (Noé et Lina), compatibles avec ElevenLabs.

🎯 Objectif :
Transformer un débat écrit en **dialogue naturel, vivant et rythmé**, fluide à l’écoute, optimisé pour une synthèse vocale réaliste.

🧠 Règles de réécriture :

1. Adopte un **style oral, spontané et fluide** :
   - phrases courtes ou découpées naturellement,
   - langage parlé, pas trop formel, mais clair,
   - rythme naturel, proche d’une vraie conversation.

2. Donne à chaque intervenant une **voix identifiable** :
   - **Noé** : logique, sec, sarcastique.
   - **Lina** : vive, provocante, chaleureuse.

3. Structure le script comme ceci :
   - **Noé** : <speak> ... </speak>
   - **Lina** : <speak> ... </speak>

4. Utilise **modérément et intelligemment** les balises SSML **compatibles ElevenLabs** :
   - `<break time="300ms"/>` : pour une pause brève **uniquement quand elle améliore le rythme** (pas après chaque phrase !).
   - `<emphasis>` : pour insister sur un mot important (1 à 2 max par réplique).
   - `<prosody rate="slow"> ... </prosody>` : pour ralentir une phrase forte, jamais tout le paragraphe.
   - `<s>` : pour marquer un découpage logique dans une phrase longue.

   ⚠️ **Important** : N’abuse jamais des pauses `<break>` — une pause mal placée casse le rythme et donne un rendu artificiel.

5. Pour exprimer les **émotions** :
   - Appuie-toi sur la **ponctuation expressive** (`!`, `?`, `...`) et des formulations naturelles (ex. : « Non mais... tu rigoles ?! »)
   - ❌ N’utilise **jamais** d’indications de ton entre parenthèses. Tout doit être implicite dans la formulation.

6. Ne termine **jamais** par une conclusion automatique ou un résumé.

❌ **Ne fournis pas de commentaire final, de note de bas de page ni de mise en contexte.**
✅ La dernière réplique du débat doit être la **dernière ligne du fichier**.
---

Voici le débat à reformuler :

---
{debate_text}
---

Réécris maintenant le script dans ce format immersif, fluide et balisé pour ElevenLabs :

Sortie attendu : 

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