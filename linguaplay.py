import streamlit as st
import openai
from gtts import gTTS
import playsound
import speech_recognition as sr
import pandas as pd
import random
import os

# 🔑 ضع هنا مفتاح OpenAI الخاص بك
openai.api_key = "YOUR_OPENAI_API_KEY"

# ===== واجهة المستخدم =====
st.set_page_config(page_title="🔥 LinguaPlay Ultra Max 🔥", layout="wide")

st.markdown("<h1 style='text-align:center;color:#9b59b6;'>🎮 LinguaPlay Ultra Max</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#2980b9;font-size:18px;'>Learn. Play. Speak. All Languages & Dialects</p>", unsafe_allow_html=True)

language = st.selectbox("اختر اللغة أو اللهجة:", ["English", "Français", "العربية", "Darija (Moroccan)"])

# ===== اللعبة التعليمية =====
st.header("🎲 تحدي اللعبة التعليمية")

questions = {
    "English": [
        {"q": "How do you say 'مرحبا'?", "a": "Hello", "xp": 5},
        {"q": "Translate: I love learning languages.", "a": "I love learning languages.", "xp": 10}
    ],
    "Français": [
        {"q": "Comment dit-on 'مرحبا'?", "a": "Bonjour", "xp": 5},
        {"q": "Translate: J'aime apprendre les langues.", "a": "J'aime apprendre les langues.", "xp": 10}
    ],
    "العربية": [
        {"q": "كيف تقول 'Hello' بالعربية؟", "a": "مرحبا", "xp": 5},
        {"q": "ترجم: I love learning languages.", "a": "أحب تعلم اللغات", "xp": 10}
    ],
    "Darija (Moroccan)": [
        {"q": "كيف تقول 'Hello' بالدارجة؟", "a": "سلام", "xp": 5},
        {"q": "Translate: I love learning languages.", "a": "كنحب نتعلم اللغات", "xp": 10}
    ]
}

if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1

q = random.choice(questions[language])
answer = st.text_input(f"Level {st.session_state.level}: {q['q']}")

if st.button("تحقق"):
    if answer.strip().lower() == q["a"].lower():
        st.success(f"✅ صح! +{q['xp']} XP")
        st.session_state.score += q["xp"]
        st.session_state.level += 1
    else:
        st.error(f"❌ خطأ! الإجابة الصحيحة: {q['a']}")
    st.write(f"نقاطك الحالية: {st.session_state.score} | المستوى: {st.session_state.level}")

# ===== شات AI نصي =====
st.header("💬 شات المعلم الذكي")
user_input = st.text_input("اكتب سؤالك أو جملة لتصحيحها:")

if st.button("أرسل الشات"):
    if user_input:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":user_input}]
        )
        answer_text = response['choices'][0]['message']['content']
        st.markdown(f"🤖 AI: {answer_text}")

# ===== شات صوتي =====
st.header("🎤 تحدث مع AI")

if st.button("سجل صوتك"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("📢 تحدث الآن...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.write("أنت قلت:", text)

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":text}]
        )
        answer_text = response['choices'][0]['message']['content']
        st.write("🤖 AI:", answer_text)

        tts = gTTS(answer_text, lang='en')
        tts.save("response.mp3")
        playsound.playsound("response.mp3", True)
        os.remove("response.mp3")

    except:
        st.error("لم يتم التعرف على الصوت، حاول مرة أخرى.")

# ===== Leaderboard عالمي =====
st.header("🏆 Leaderboard العالمي")

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = pd.DataFrame(columns=["Player", "Score"])

player_name = st.text_input("اسمك للـ Leaderboard:")

if st.button("حفظ النقاط"):
    if player_name:
        new_entry = pd.DataFrame({"Player":[player_name], "Score":[st.session_state.score]})
        st.session_state.leaderboard = pd.concat([st.session_state.leaderboard, new_entry], ignore_index=True)
        st.session_state.leaderboard = st.session_state.leaderboard.sort_values(by="Score", ascending=False)
        st.table(st.session_state.leaderboard.head(10))
