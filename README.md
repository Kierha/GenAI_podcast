# 🎤 AI Podcast Generator

Génère automatiquement un podcast immersif entre deux agents propulsés par intelligences artificielles qui débattent sur un sujet donné.  
Ce projet combine génération de texte, reformulation audio-friendly, synthèse vocale et interface utilisateur via Streamlit.

---

## 🚀 Fonctionnalités

- 💬 **Saisie d’un sujet de débat** en langage naturel.
- 🧠 **Génération d’un script de débat** entre deux agents aux personnalités distinctes.
- 🦨 **Reformulation du script** en style oral optimisé pour la lecture vocale.
- 🔊 **Synthèse vocale** des répliques (Noé & Lina) avec ElevenLabs.
- 🎧 **Écoute directe** dans l’interface Streamlit.
- 🔗 **Téléchargement du podcast audio** (format MP3).
- 📄 **Téléchargement du script formaté**.

---

## 🧱 Technologies utilisées

| Composant            | Choix technologique              | Raison du choix                      |
| -------------------- | -------------------------------- | ------------------------------------ |
| UI / Interface       | `Streamlit`                      | Déploiement rapide, responsive natif |
| Génération de script | `OpenRouter` (modèle `deepseek`) | API simple et efficace               |
| Reformulation        | `Prompt Engineering + SSML`      | Optimisé pour la synthèse vocale     |
| Synthèse audio       | `ElevenLabs API`                 | Voix naturelles et multilingues      |
| Traitement audio     | `pydub`                          | Assemblage et gestion des silences   |
| Sécurité & config    | `dotenv`                         | Gestion propre des clés d’API        |

---

## 🛠️ Structure du projet

```
🔹 app.py                    # Interface Streamlit principale
🔹 debate_logic.py          # Génération du débat brut
🔹 format_podcast.py        # Reformulation en script audio immersif
🔹 generate_audio.py        # Génération et assemblage des fichiers MP3
🔹 output/                  # Dossier de sortie
    ├debate.txt
    ├podcast_ready.txt
    └final_podcast.mp3
🔹 tests/                   # Fichiers de tests unitaires
🔹 requirements.txt         # Dépendances
```

---

## 🧪 Installation locale

1. Cloner le dépôt :

```bash
git clone https://github.com/ton-compte/ai-podcast-generator.git
cd ai-podcast-generator
```

2. Créer un environnement virtuel (facultatif mais recommandé) :

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate    # Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Spécifications utilisées :

- Python 3.11
- Streamlit ≥ 1.32
- ElevenLabs ≥ 1.0
- openai ≥ 1.16

5. Lancer en local :

```bash
streamlit run app.py
```

---

## 🔑 Clés d'API

Créez un fichier `.env` à la racine du projet contenant vos clés :

```plaintext
OPENROUTER_API_KEY=your_openrouter_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
VOICE_NOE_ID=your_voice_id_for_noe
VOICE_LINA_ID=your_voice_id_for_lina
```

---

## ▶️ Utilisation

### 🖥️ En local

1. Lancer `streamlit run app.py`
2. Entrer un sujet dans le champ dédié
3. Cliquer sur **"Générer"**
4. Écouter ou télécharger le podcast

### 🌐 En ligne

⚠️ Actuellement non fonctionnel en ligne (compte gratuit ElevenLabs)
L’application fonctionne intégralement en local, mais la génération audio est restreinte dans l’environnement cloud à cause des limitations du compte gratuit ElevenLabs (blocage des appels depuis une IP distante).

Le projet reste déployé en ligne pour prouver la capacité de déploiement via Streamlit, mais pour une expérience complète (texte + audio), il est recommandé de le faire tourner en local.

ℹ️ Important :
L’application est hébergée sur Streamlit Cloud (compte gratuit).
Après une période d’inactivité, elle peut être mise en veille.
Un simple clic sur le bouton affiché à l'écran est nécessaire pour la relancer.
Ce comportement est normal et n’impacte pas le fonctionnement du projet.

<!-- Lien vers le site -->

[Lien vers le site](https://aipodcast-student-ynov.streamlit.app/)

Aucune installation n’est requise pour l’utilisateur final.

---

## ✨ Exemples de sujets

- _Faut-il interdire les smartphones avant 16 ans ?_
- _L’IA remplacera-t-elle les enseignants ?_
- _Les réseaux sociaux sont-ils un danger pour la démocratie ?_

---

## 🔮 Evolutions futures envisagées

- 👥 **Multi-agents & personnalités variables** :

  - Choix de profils personnalisés (ex : philosophe vs ingénieur).
  - Débats entre plusieurs intervenants IA.

- 🧠 **Diversification des modèles IA** :

  - Comparaison inter-modèles (GPT vs Claude vs Gemini...).
  - Analyse automatique des styles de réponse.

- 🧱‍💻 **Amélioration UX/UI** :

  - Ajout d’un vrai espace utilisateur.
  - Historique des podcasts créés.
  - Téléchargements multi-formats (texte, audio, transcription).

- 🎧 **Rendu audio plus immersif** :
  - Tuning des pauses, intonations, style narratif.
  - Montage automatique + générique d’intro/outro.
  - Edition partielle des pistes audio via IA.

---

## 📄 Auteurs

Projet réalisé par **Thomas D**, étudiant en Mastère Expert Logiciel Mobile & IoT chez Ynov Lyon.

---

## 📁 Licence

Projet académique. Non destiné à un usage commercial.
