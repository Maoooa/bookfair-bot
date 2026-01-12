from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK", 200


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip().lower()

    if user_text == "สวัสดี":
        reply = "สวัสดีครับ 😊 มีอะไรให้ช่วยไหม"

    elif user_text == "help":
        reply = (
            "📚 Bookfair Bot ทำอะไรได้บ้าง\n"
            "- พิมพ์ 'สวัสดี'\n"
            "- พิมพ์ 'help'\n"
            "(ฟีเจอร์อื่น ๆ กำลังมา)"
        )

    else:
        reply = "ขอโทษนะครับ ยังไม่เข้าใจข้อความนี้ 🥺 พิมพ์ 'help' ได้นะ"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )
