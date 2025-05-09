import requests
from config import GOOGLE_PLACES_API_KEY
from services.reviews import get_reviews

# 📍 文字查詢餐廳
def search_restaurants(location):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{location} 餐廳",
        "key": GOOGLE_PLACES_API_KEY,
        "language": "zh-TW",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return ["😢 沒有找到相關餐廳，請換個關鍵字試試看！"]

        restaurants = sorted(data["results"], key=lambda r: r.get("rating", 0), reverse=True)[:3]
        messages = ["🍽 **熱門餐廳推薦** 🍽\n"]
        for idx, r in enumerate(restaurants, start=1):
            name = r.get("name", "未知餐廳")
            rating = r.get("rating", "無評分")
            address = r.get("formatted_address", "無地址資訊")
            status = r.get("business_status", "無營業資訊")
            place_id = r.get("place_id", "")

            photo_url = None
            if "photos" in r:
                photo_ref = r["photos"][0]["photo_reference"]
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo_ref}&key={GOOGLE_PLACES_API_KEY}"

            reviews = get_reviews(place_id)

            msg = f"🏆 **{idx}. {name}**\n⭐ 評分：{rating}/5.0\n📍 地址：{address}\n🕒 營業狀況：{status}\n"
            if reviews:
                msg += f"💬 評論：{reviews}\n"
            msg += f"🚗 [導航](https://www.google.com/maps/search/?api=1&query={address.replace(' ', '+')})\n"
            messages.append(msg.strip())
            if photo_url:
                messages.append(photo_url)
        return messages

    except requests.exceptions.RequestException as e:
        return [f"❌ 無法獲取餐廳資訊：{e}"]

# 📍 位置查詢附近餐廳
def search_nearby_restaurants(lat, lng):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 1000,
        "type": "restaurant",
        "key": GOOGLE_PLACES_API_KEY,
        "language": "zh-TW"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return ["😢 附近找不到餐廳，換個地點試試吧！"]

        restaurants = sorted(data["results"], key=lambda r: r.get("rating", 0), reverse=True)[:3]
        messages = ["📍 **你附近的熱門餐廳** 🍽\n"]
        for idx, r in enumerate(restaurants, start=1):
            name = r.get("name", "未知餐廳")
            rating = r.get("rating", "無評分")
            address = r.get("vicinity", "無地址資訊")
            place_id = r.get("place_id", "")

            photo_url = None
            if "photos" in r:
                photo_ref = r["photos"][0]["photo_reference"]
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo_ref}&key={GOOGLE_PLACES_API_KEY}"

            reviews = get_reviews(place_id)

            msg = f"🏅 **{idx}. {name}**\n⭐ 評分：{rating}\n📍 地址：{address}\n"
            if reviews:
                msg += f"💬 評論：{reviews}\n"
            msg += f"🚗 [導航](https://www.google.com/maps/search/?api=1&query={address.replace(' ', '+')})\n"
            messages.append(msg.strip())
            if photo_url:
                messages.append(photo_url)
        return messages

    except requests.exceptions.RequestException as e:
        return [f"❌ 查詢失敗：{e}"]
