from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    prompt = f"あなたは7歳の植物の妖精ボタニカくんです。やさしい言葉でユーザーに植物のアドバイスを返してください。ユーザー:「{user_text}」"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたはボタニカくん。植物のことを優しく教える妖精です。"},
            {"role": "user", "content": prompt}
        ]
    )

    reply_text = response.choices[0].message.content

    print("User input:", user_text)
    print("Bot reply:", reply_text)
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
