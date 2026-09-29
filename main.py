import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_models import Base, WeatherForecast
from geo_locator import get_location
from weather_client import fetch_forecast, aggregate_daily
from exporter import export_markdown

load_dotenv()

def main():
    db_url = os.getenv("DB_URL", "sqlite:///weather_lab.db")
    output_file = os.getenv("OUTPUT_FILE", "weather_report.md")

    key = os.getenv("WEATHER_API_KEY")
    print("DEBUG ключ:", repr(key))
    print("DEBUG длина ключа:", len(key) if key else 0)
    # ---------------

    engine = create_engine(db_url)
    ...
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    city, lat, lon = get_location()
    print(f"[geo] город: {city}, координаты: {lat}, {lon}")

    items = fetch_forecast(lat, lon)
    daily = aggregate_daily(items, days=4)
    print(f"[weather] дней к сохранению: {len(daily)}")

    saved = 0
    for row in daily:
        exists = session.query(WeatherForecast).filter_by(
            city=city, forecast_date=row["date"]
        ).first()
        if exists:
            continue
        session.add(WeatherForecast(city=city, forecast_date=row["date"], **{
            k: row[k] for k in ("temp_min", "temp_max", "humidity", "wind_speed", "description")
        }))
        saved += 1
    session.commit()
    print(f"[db] сохранено новых записей: {saved}")

    export_markdown(session, city, output_file)
    session.close()

if __name__ == "__main__":
    main()