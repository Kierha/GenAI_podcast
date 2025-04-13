import streamlit as st
import os
from datetime import datetime
from debate_logic import simulate_debate
from format_podcast import format_podcast_script
from generate_audio import run_audio_pipeline

# ───────────────────────────────
# CONFIGURATION STREAMLIT
# ───────────────────────────────
st.set_page_config(page_title="AI Podcast Generator", layout="centered")
st.markdown("""
    <style>
    h1 a, h2 a, h3 a { display: none; }  /* Cacher les ancres */
    </style>
""", unsafe_allow_html=True)

# ───────────────────────────────
# EN-TÊTE
# ───────────────────────────────
st.title("🎙️ AI Podcast Generator")

st.markdown("""
Bienvenue sur **AI Podcast Generator**.  
Tape un sujet de débat, et laisse deux agents d'intelligence artificielles simuler un échange vivant, mis en voix automatiquement.

**Version 1.0**  
Ce prototype génère pour l’instant **les répliques audio** entre 2 personnages (Noé et Lina), ainsi que le **script complet** au format txt.
""")

# ───────────────────────────────
# INPUT
# ───────────────────────────────
sujet = st.text_input("Insère le sujet du débat")

# ───────────────────────────────
# BOUTON GÉNÉRER
# ───────────────────────────────
if st.button("Générer") and sujet.strip():
    with st.spinner("1/3 - Génération du script brut..."):
        simulate_debate(sujet)
        st.success("✅ Débat généré.")

    with st.spinner("2/3 - Adaptation en format podcast..."):
        format_podcast_script_path = format_podcast_script(open("output/debate.txt", "r", encoding="utf-8").read())
        st.success("✅ Script podcast prêt.")

    with st.spinner("3/3 - Génération audio des deux premières répliques..."):
        run_audio_pipeline()
        st.success("✅ Audio généré.")

    # ────────────────
    # AFFICHAGE RÉSULTAT
    # ────────────────
    st.markdown("---")
    st.subheader("🎧 Résultat : Podcast généré")

    audio_file_path = "output/final_podcast.mp3"
    script_file_path = "output/podcast_ready.txt"

    if os.path.exists(audio_file_path):
        st.audio(audio_file_path)

        col1, col2 = st.columns([2, 1])
        with col1:
            with open(script_file_path, "rb") as script_file:
                st.download_button(
                    label="📄 Télécharger le script",
                    data=script_file,
                    file_name=f"Script - {sujet[:30]}.txt",
                    mime="text/plain"
                )
        with col2:
            with open(audio_file_path, "rb") as audio_file:
                st.download_button(
                    label="🎵 Télécharger le podcast",
                    data=audio_file,
                    file_name=f"Podcast - {sujet[:30]} - {datetime.now().strftime('%Y-%m-%d')}.mp3",
                    mime="audio/mpeg"
                )
else:
    st.info("📝 Saisis un sujet de débat pour commencer.")
