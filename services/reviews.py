import requests
from config import GOOGLE_PLACES_API_KEY

# 🗣 查詢評論
def get_reviews(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": GOOGLE_PLACES_API_KEY,
        "language": "zh-TW"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        reviews = data.get("result", {}).get("reviews", [])
        for r in reviews:
            if 'zh' in r.get("language", ""):
                return r.get("text")
        return reviews[0]["text"] if reviews else None
    except requests.exceptions.RequestException:
        return None
