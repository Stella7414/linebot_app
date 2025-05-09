from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from handlers.message_handler import handle_message
from handlers.location_handler import handle_location
from services.restaurant_search import search_restaurants

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 註冊處理器
handler.add(handle_message)
handler.add(handle_location)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
