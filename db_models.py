from datetime import datetime, date
from sqlalchemy import String, Float, Integer, Date, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class WeatherForecast(Base):
    __tablename__ = "weather_forecast"
    __table_args__ = (UniqueConstraint("city", "forecast_date", name="uq_city_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String)
    forecast_date: Mapped[date] = mapped_column(Date)
    temp_min: Mapped[float] = mapped_column(Float)
    temp_max: Mapped[float] = mapped_column(Float)
    humidity: Mapped[int] = mapped_column(Integer)
    wind_speed: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)