"""Restaurant model for caching Google Places data."""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, JSON
from .base import Base, TimestampMixin


class RestaurantCache(Base, TimestampMixin):
    """Cache restaurant data from Google Places API."""
    __tablename__ = "restaurant_cache"

    id = Column(Integer, primary_key=True)
    google_place_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String(50))
    website = Column(String(500))
    rating = Column(Float, default=0.0)
    user_ratings_total = Column(Integer, default=0)
    price_level = Column(Integer)  # 0-4 from Google Places
    cuisine_types = Column(JSON)  # List of cuisine types
    opening_hours = Column(JSON)
    photos = Column(JSON)  # Photo references
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "google_place_id": self.google_place_id,
            "name": self.name,
            "address": self.address,
            "location": {"lat": self.latitude, "lng": self.longitude},
            "phone": self.phone,
            "website": self.website,
            "rating": self.rating,
            "user_ratings_total": self.user_ratings_total,
            "price_level": self.price_level,
            "cuisine_types": self.cuisine_types,
            "opening_hours": self.opening_hours,
            "photos": self.photos
        }