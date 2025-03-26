import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from debate_logic import simulate_debate

sujet = "L'Intelligence Artificielle est-elle une menace ou une opportunité à l'école ?"
resultat = simulate_debate(sujet)
print("\n🗣️ Débat généré :\n")
print(resultat)
