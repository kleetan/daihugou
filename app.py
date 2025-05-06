import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="世界史年号で大富豪", layout="centered")

# --- データの読み込み ---
@st.cache_data
def load_data():
    df = pd.read_csv("nenpyou - シート1.csv")
    df["year"] = df["year"].astype(int)
    return df

# --- カードをシャッフルして配布 ---
def deal_cards(df):
    shuffled = df.sample(frac=1).reset_index(drop=True)
    player = shuffled.iloc[::2].reset_index(drop=True)
    ai = shuffled.iloc[1::2].reset_index(drop=True)
    return player, ai

# --- セッション初期化 ---
if "player_cards" not in st.session_state:
    data = load_data()
    player_cards, ai_cards = deal_cards(data)
    st.session_state.player_cards = player_cards
    st.session_state.ai_cards = ai_cards
    st.session_state.history = []
    st.session_state.result = ""

# --- タイトル ---
st.title("🃏 世界史年号で大富豪（年号が大きいほど強い）")

# --- プレイヤーの手札表示 ---
st.subheader("あなたの手札")
for i, row in st.session_state.player_cards.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{row['event']}**（{row['year']}年）")
    with col2:
        if st.button(f"出す", key=f"play_{i}"):
            player_card = row
            ai_card = st.session_state.ai_cards.sample(1).iloc[0]

            # 勝敗判定（年号が大きい方が勝ち）
            if player_card["year"] > ai_card["year"]:
                result = "🎉 あなたの勝ち！"
            elif player_card["year"] < ai_card["year"]:
                result = "🤖 AIの勝ち！"
            else:
                result = "⚔️ 引き分け！"

            # 履歴と手札更新
            st.session_state.history.append({
                "player": f"{player_card['event']}（{player_card['year']}年）",
                "ai": f"{ai_card['event']}（{ai_card['year']}年）",
                "result": result
            })

            st.session_state.player_cards = st.session_state.player_cards.drop(i).reset_index(drop=True)
            st.session_state.ai_cards = st.session_state.ai_cards.drop(ai_card.name).reset_index(drop=True)
            st.session_state.result = result
            st.experimental_rerun()

# --- 最新の勝敗表示 ---
if st.session_state.result:
    st.subheader("結果")
    st.success(st.session_state.result)

# --- 対戦履歴表示 ---
if st.session_state.history:
    st.subheader("対戦履歴")
    for h in reversed(st.session_state.history):
        st.markdown(f"🧍‍♂️ {h['player']} vs 🤖 {h['ai']} → **{h['result']}**")

# --- リセットボタン ---
if st.button("🔄 最初からやり直す"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()
