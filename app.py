import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="世界史大富豪", layout="centered")

# --- データ読み込み ---
@st.cache_data
def load_data():
    df = pd.read_csv("nenpyou - シート1.csv")
    df["year"] = df["year"].astype(int)
    return df

# --- 初期化 ---
def init_game():
    data = load_data().sample(frac=1).reset_index(drop=True)
    st.session_state.player_cards = data.iloc[:7].reset_index(drop=True)
    st.session_state.ai_cards = data.iloc[7:14].reset_index(drop=True)
    st.session_state.history = []
    st.session_state.turn = "ai"
    st.session_state.current_ai_card = None
    st.session_state.result = ""

# --- 初回のみ初期化 ---
if "player_cards" not in st.session_state:
    init_game()
# --- セッション初期化 ---
if "player_cards" not in st.session_state:
    init_game()

# 🔐 安全にアクセスするように修正（重要！！）
if "turn" not in st.session_state:
    st.session_state.turn = "ai"

if "ai_cards" not in st.session_state:
    st.session_state.ai_cards = pd.DataFrame()

if "current_ai_card" not in st.session_state:
    st.session_state.current_ai_card = None

# --- タイトル ---
st.title("🃏 世界史年号で大富豪（AI先攻）")
st.markdown("ルール：**年号が新しいほうが勝ち**。AIのカードを見てから出すか選べます。")

# --- ターン処理 ---
if st.session_state.turn == "ai" and st.session_state.ai_cards.shape[0] > 0:
    ai_card = st.session_state.ai_cards.iloc[0]
    st.session_state.current_ai_card = ai_card
    st.session_state.turn = "player"

# --- AIが出したカード表示 ---
if st.session_state.current_ai_card is not None:
    st.subheader("🤖 AIが出したカード")
    st.markdown(f"**{st.session_state.current_ai_card['event']}**（{st.session_state.current_ai_card['year']}年）")

# --- プレイヤーの選択肢 ---
if st.session_state.turn == "player":
    st.subheader("🧍‍♂️ あなたの手札")
    for i, row in st.session_state.player_cards.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{row['event']}**（{row['year']}年）")
        with col2:
            if st.button("このカードで勝負！", key=f"play_{i}"):
                player_card = row
                ai_card = st.session_state.current_ai_card

                if player_card["year"] > ai_card["year"]:
                    result = "🎉 あなたの勝ち！"
                elif player_card["year"] < ai_card["year"]:
                    result = "🤖 AIの勝ち！"
                else:
                    result = "⚔️ 引き分け！"

                st.session_state.history.append({
                    "player": f"{player_card['event']}（{player_card['year']}年）",
                    "ai": f"{ai_card['event']}（{ai_card['year']}年）",
                    "result": result
                })

                st.session_state.player_cards = st.session_state.player_cards.drop(i).reset_index(drop=True)
                st.session_state.ai_cards = st.session_state.ai_cards.drop(0).reset_index(drop=True)
                st.session_state.result = result
                st.session_state.turn = "ai"
                st.session_state.current_ai_card = None
                st.experimental_rerun()

    # --- 出さずにスキップ ---
    if st.button("出さずにスキップ"):
        st.session_state.history.append({
            "player": "出さなかった",
            "ai": f"{st.session_state.current_ai_card['event']}（{st.session_state.current_ai_card['year']}年）",
            "result": "🕊️ スキップ"
        })
        st.session_state.ai_cards = st.session_state.ai_cards.drop(0).reset_index(drop=True)
        st.session_state.turn = "ai"
        st.session_state.current_ai_card = None
        st.session_state.result = ""
        st.experimental_rerun()

# --- 結果表示 ---
if st.session_state.result:
    st.subheader("結果")
    st.success(st.session_state.result)

# --- 履歴表示 ---
if st.session_state.history:
    st.subheader("🕘 対戦履歴")
    for h in reversed(st.session_state.history):
        st.markdown(f"🧍‍♂️ {h['player']} vs 🤖 {h['ai']} → **{h['result']}**")

# --- ゲーム終了チェック ---
if st.session_state.player_cards.empty or st.session_state.ai_cards.empty:
    st.warning("🎮 ゲーム終了！最初からやり直せます。")

# --- リセットボタン ---
if st.button("🔄 最初からやり直す"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()
