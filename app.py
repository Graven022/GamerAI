import streamlit as st
from openai import OpenAI
import os



# 🔑 API
client = OpenAI(api_key="sk-...LiQA")
# 🎮 PERSONNALITÉ
SYSTEM_PROMPT = """
Tu es GamerAI, un expert en développement de jeux vidéo.

Compétences :
- Python (Pygame)
_ Java
_ Javascript
- Unity (C#)
- Godot (GDScript)
- Game design
- Debugging

Personnalité :
- Sarcastique mais drôle
- Très intelligent
- Explique clairement

Règles :
- Si le code est mauvais → moque-toi gentiment
- Donne TOUJOURS une solution claire
- Propose des améliorations comme un vrai dev senior
"""

# 🎨 UI
st.set_page_config(page_title="Gamer AI 🎮", page_icon="🎮")
st.title("🎮 Gamer AI - Dev Assistant")

# 🧠 Mémoire
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🎮 MODE
mode = st.sidebar.selectbox(
    "Mode",
    ["💬 Chat", "🐍 Python", "🎮 Game Design", "🕹️ Unity", "🐉 Godot"]
)

# 🎮 GENERATEUR DE JEU
st.sidebar.header("🎮 Générateur de jeu")

game_type = st.sidebar.selectbox(
    "Type de jeu",
    ["Snake", "Platformer", "Shooter", "RPG" ]
)

language = st.sidebar.selectbox(
    "Technologie",
    ["Pygame", "Unity C#", "Godot"]
)

if st.sidebar.button("Créer un jeu 🚀"):
    prompt = f"""
Crée un jeu COMPLET.

Type: {game_type}
Technologie: {language}

Exigences :
- Code complet et fonctionnel
- Instructions pour lancer
- Structure du projet
"""

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(

                model="gpt-4.1",
                    messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                        ],
                            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })

        # 📥 Télécharger
        st.download_button(
            "📥 Télécharger le code",
            full_response,
            file_name="game.txt"
        )

# 📂 UPLOAD CODE
st.sidebar.header("Upload Code")
file = st.sidebar.file_uploader("Fichier code", type=["py", "cs", "gd"])

if file and st.sidebar.button("Analyser 🔥"):
    code = file.getvalue().decode("utf-8")

    prompt = f"""
Mode: {mode}

Analyse ce code comme un dev senior.
Sois sarcastique puis améliore-le :

{code}
"""

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })

# 💬 AFFICHAGE CHAT
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 💬 INPUT USER
if prompt := st.chat_input("Demande-moi un truc dev/game..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    full_prompt = f"Mode: {mode}\n\n{prompt}"

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *st.session_state.messages,
                {"role": "user", "content": full_prompt}
            ],
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })
