from linebot.models import MessageEvent, LocationMessage
from services.restaurant import search_nearby_restaurants
from utils.sender import send_messages

def handle_location(event):
    lat = event.message.latitude
    lng = event.message.longitude
    messages = search_nearby_restaurants(lat, lng)
    send_messages(event, messages)
