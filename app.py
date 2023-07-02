# 以下を「app.py」に書き込み
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key


system_prompt = """
あなたは優れたマネジメントです。
入力された相談に対し、分かりやすい言葉で簡潔に回答します。
あなたの役割は仕事全般のアドバイザーです。例えば以下のようなことを聞かれても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去



# ユーザーインターフェイスの構築
st.title("悩み相談のチャットボット")
st.image("25_Advisor.png")
st.write("何を悩んでしますか？  ※新しい相談事は[F5]押下等でリロードしてください")


user_input = st.text_area("メッセージを入力してください。", key="user_input")


if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])




# Shiftキーの状態を保存する変数
shift_pressed = False

# Shiftキーの状態を更新する関数
def update_shift_state(event):
    global shift_pressed
    if event.type == "keydown" and event.key == "Shift":
        shift_pressed = True
    elif event.type == "keyup" and event.key == "Shift":
        shift_pressed = False

# キーボードイベントを監視してShiftキーの状態を更新する
st.write(
    """
    <script>
    document.addEventListener("keydown", function(event) {
        if (event.key === "Shift") {
            if (typeof Streamlit !== "undefined") {
                Streamlit._sendMessage({ event: "shift_key", pressed: true });
            }
        }
    });

    document.addEventListener("keyup", function(event) {
        if (event.key === "Shift") {
            if (typeof Streamlit !== "undefined") {
                Streamlit._sendMessage({ event: "shift_key", pressed: false });
            }
        }
    });
    </script>
    """
)

# テキスト入力欄の行数を設定
rows = len(user_input.split("\n")) if shift_pressed else 1
st.text_area("メッセージを入力してください。", key="user_input", height=rows * 20)

# ユーザーの入力に応じた処理を追加する関数
def communicate():
    # ユーザーの入力を使用して処理を実行するコードを追加する

# テキスト入力欄の変更時に処理を実行する
communicate()
