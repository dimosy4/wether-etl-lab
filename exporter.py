import os
from db_models import WeatherForecast

def export_markdown(session, city, output_file):
    rows = session.query(WeatherForecast).filter_by(city=city).order_by(WeatherForecast.forecast_date).all()
    if not rows:
        print("[export] нет данных")
        return
    period = f"{rows[0].forecast_date} — {rows[-1].forecast_date}"
    lines = [
        "# Прогноз погоды\n",
        f"Автоматически определённая локация: {city}\n",
        f"Период: {period}\n",
        "| Дата | Мин. темп. (°C) | Макс. темп. (°C) | Описание | Влажность (%) | Ветер (м/с) |",
        "|------|----------------|------------------|----------|---------------|-------------|",
    ]
    for r in rows:
        lines.append(
            f"| {r.forecast_date} | {r.temp_min:.0f} | {r.temp_max:.0f} | "
            f"{r.description.capitalize()} | {r.humidity} | {r.wind_speed:.0f} |"
        )
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[export] сохранено в {output_file}")