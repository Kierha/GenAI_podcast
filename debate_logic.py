# debate_logic.py — DeepSeek via OpenRouter (nouveau SDK client)

import os
from openai import OpenAI
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialiser le client OpenRouter
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

# Rôles fixes pour la V1
ROLE_NOE = (
    "Tu es Noé. Tu es rationnel, analytique et critique. "
    "Tu argumentes avec rigueur, tu privilégies les faits et la logique, "
    "Tu ne te laisses pas séduire par des raisonnements émotionnels. "
    "Tu peux être piquant ou ironique si ton interlocutrice est trop idéaliste."
)

ROLE_LINA = (
    "Tu es Lina. Tu es passionnée, ouverte et visionnaire. "
    "Tu n’as pas peur d’aller à contre-courant pour défendre une idée nouvelle. "
    "Tu utilises l’humour, la provocation et parfois l’exagération pour faire passer tes messages. "
    "Ton style est percutant mais argumenté."
)

def build_single_prompt(sujet: str) -> str:
    return f"""
Tu es un modèle de génération de texte conçu pour écrire des scripts de podcast immersifs, vivants et en français.

Sujet du débat : "{sujet}"

Deux intelligences artificielles débattent sur ce sujet, chacune ayant une personnalité distincte et un nom humain.

Rôle de Noé : {ROLE_NOE}
Rôle de Lina : {ROLE_LINA}

Contraintes :
- Le débat doit être rédigé **exclusivement en français**. Tu n’as pas le droit d’utiliser des mots ou expressions en anglais.
- Structure : **5 tours complets** (10 répliques en tout, Noé puis Lina à chaque tour).
- Format :

Noé : ...
Lina : ...
...

- Le débat suit une progression logique : **introduction → confrontation → fin argumentée**, mais **pas de consensus artificiel**.
- **Évite les métaphores banales ou génériques** (ex : yin et yang, “nous nous complétons”, etc.).
- Tu peux utiliser un ton **piquant, provocateur, sarcastique ou drôle**, en restant crédible et pertinent.
- Le style est **fluide, oral, dynamique**, adapté à un **podcast francophone**.
- **Termine clairement après la dixième réplique**, sans couper une idée en plein milieu.

Génère uniquement le contenu du débat ci-dessous :
"""

def query_openrouter(prompt: str) -> str:
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        extra_headers={
            "HTTP-Referer": "https://yourapp.com",
            "X-Title": "GenAI Podcast"
        },
        extra_body={}
    )
    return completion.choices[0].message.content.strip()

def simulate_debate(sujet: str) -> str:
    print("🎙️ Génération du script de podcast via DeepSeek (OpenRouter)...")
    prompt = build_single_prompt(sujet)
    result = query_openrouter(prompt)

    # Sauvegarde
    os.makedirs("output", exist_ok=True)
    with open("output/debate.txt", "w", encoding="utf-8") as f:
        f.write(result)

    print("✅ Script généré avec succès et sauvegardé dans output/debate.txt")
    return result