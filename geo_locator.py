import os
import requests

def get_location():
    url = os.getenv("GEO_API_URL", "http://ip-api.com/json/")
    print(f"[geo] запрос к {url}")

    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()

        if data.get("status") == "success":
            city = data.get("city")
            lat = data.get("lat")
            lon = data.get("lon")
            region = data.get("regionName")
            country = data.get("country")
            if city and lat is not None and lon is not None:
                print(f"[geo] ip-api.com -> {city}, {region}, {country} ({lat}, {lon})")
                return city, float(lat), float(lon)
            else:
                print(f"[geo] ip-api.com: неполные данные: {data}")
        else:
            print(f"[geo] ip-api.com вернул fail: {data.get('message')}")

    except requests.exceptions.Timeout:
        print("[geo] ip-api.com: таймаут")
    except requests.exceptions.RequestException as e:
        print(f"[geo] ip-api.com: сетевая ошибка: {e}")
    except ValueError as e:
        print(f"[geo] ip-api.com: некорректный JSON: {e}")

    fallback_city = os.getenv("GEO_API_FALLBACK_CITY", "Moscow")
    print(f"[geo] fallback -> {fallback_city}")
    fallback_coords = {
        "Moscow": (55.7558, 37.6176),
        "Kirov": (58.6035, 49.6679),
        "Berlin": (52.5200, 13.4050),
    }
    lat, lon = fallback_coords.get(fallback_city, (55.7558, 37.6176))
    return fallback_city, lat, lon