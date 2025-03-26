import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from format_podcast import format_podcast_script

with open("output/debate.txt", "r", encoding="utf-8") as f:
    raw_debate = f.read()

script_reformate = format_podcast_script(raw_debate)
print("\n Script généré :\n")
print(script_reformate)
