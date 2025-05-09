from linebot.models import MessageEvent, TextMessage
from linebot.models import TextSendMessage
from services.restaurant import search_restaurants
from services.route import get_route
from utils.sender import send_messages

def handle_message(event):
    user_input = event.message.text.strip()
    if user_input.startswith("路線 "):
        try:
            _, origin, destination = user_input.split()
            info = get_route(origin, destination)
            messages = [f"🗺 **從 {origin} 到 {destination} 的建議路線**\n{info}"]
        except:
            messages = ["❌ 請輸入格式：路線 出發地 目的地"]
    elif len(user_input) >= 2:
        messages = search_restaurants(user_input)
    else:
        messages = ["❌ 請輸入 城市 + 美食類型，或使用 `路線 出發地 目的地`。"]

    send_messages(event, messages)
