from linebot.models import TextSendMessage, ImageSendMessage
from config import LINE_CHANNEL_ACCESS_TOKEN
from linebot import LineBotApi

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def send_messages(event, messages):
    first = True
    for msg in messages:
        if msg.startswith("http"):
            line_bot_api.push_message(
                event.source.user_id,
                ImageSendMessage(original_content_url=msg, preview_image_url=msg)
            )
        else:
            text_msg = TextSendMessage(text=msg)
            if first:
                line_bot_api.reply_message(event.reply_token, text_msg)
                first = False
            else:
                line_bot_api.push_message(event.source.user_id, text_msg)
