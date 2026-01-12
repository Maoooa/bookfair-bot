from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from sheet import get_sheet
from datetime import datetime

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
    text = event.message.text.strip()

    if text.startswith("เพิ่ม"):
        try:
            parts = text.split(" ")
            book_name = parts[1]
            price = parts[2]

            sheet = get_sheet()
            sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                book_name,
                price,
                event.source.user_id
            ])

            reply = f"📚 เพิ่มหนังสือแล้ว\nชื่อ: {book_name}\nราคา: {price} บาท"
        except:
            reply = "❌ รูปแบบไม่ถูกต้อง\nตัวอย่าง: เพิ่ม ชื่อหนังสือ 350"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
