import os, requests
from collections import defaultdict
from datetime import datetime, date, timedelta

def fetch_forecast(lat, lon):
    api_key = os.getenv("WEATHER_API_KEY")
    base = os.getenv("WEATHER_API_BASE_URL", "https://api.openweathermap.org/data/2.5/forecast")
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": "ru"}
    r = requests.get(base, params=params, timeout=15)
    if r.status_code == 401:
        raise RuntimeError("Неверный API-ключ OpenWeatherMap")
    if r.status_code == 429:
        raise RuntimeError("Превышен лимит запросов OpenWeatherMap")
    r.raise_for_status()
    data = r.json()
    if str(data.get("cod")) != "200":
        raise RuntimeError(f"API вернул ошибку: {data.get('message')}")
    return data["list"]

def aggregate_daily(items, days=4):
    buckets = defaultdict(list)
    for it in items:
        d = datetime.fromtimestamp(it["dt"]).date()
        buckets[d].append(it)

    today = date.today()
    result = []
    for d in sorted(buckets.keys()):
        if d < today:
            continue
        if len(result) >= days:
            break
        rows = buckets[d]
        temp_min = min(r["main"]["temp_min"] for r in rows)
        temp_max = max(r["main"]["temp_max"] for r in rows)
        humidity = round(sum(r["main"]["humidity"] for r in rows) / len(rows))
        wind_speed = max(r["wind"]["speed"] for r in rows)
        # описание — из полуденной точки или самое частое
        noon = min(rows, key=lambda r: abs(datetime.fromtimestamp(r["dt"]).hour - 12))
        desc = noon["weather"][0]["description"]
        result.append({
            "date": d, "temp_min": temp_min, "temp_max": temp_max,
            "humidity": humidity, "wind_speed": wind_speed, "description": desc,
        })
    return result