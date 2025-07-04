"""Google Places API client."""

import asyncio
from typing import List, Dict, Any, Optional
import googlemaps
import structlog

from config.settings import settings

logger = structlog.get_logger()


class GooglePlacesClient:
    """Client for Google Places API."""

    def __init__(self):
        self.client = googlemaps.Client(key=settings.google_places_api_key)

    async def search_restaurants(
        self,
        location: str,
        radius: int = 10000,
        cuisine_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search for restaurants."""
        try:
            # Build query
            query = "restaurant"
            if cuisine_type:
                query = f"{cuisine_type} restaurant"

            # Search parameters
            search_params = {
                "query": query,
                "location": location,
                "radius": min(radius, 50000),  # Google API limit
                "type": "restaurant"
            }

            # Execute search in thread pool (Google Maps client is sync)
            response = await asyncio.to_thread(
                self.client.places,
                **search_params
            )

            # Format results
            restaurants = []
            for place in response.get("results", []):
                restaurant_data = self._format_place_data(place)
                if restaurant_data:
                    restaurants.append(restaurant_data)

            logger.info(
                "Restaurant search completed",
                location=location,
                cuisine=cuisine_type,
                count=len(restaurants)
            )

            return restaurants

        except Exception as e:
            logger.error("Error searching restaurants", error=str(e))
            return []

    def _format_place_data(self, place: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Format Google Places data."""
        try:
            geometry = place.get("geometry", {})
            location = geometry.get("location", {})

            return {
                "google_place_id": place.get("place_id"),
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "latitude": location.get("lat"),
                "longitude": location.get("lng"),
                "rating": place.get("rating", 0.0),
                "user_ratings_total": place.get("user_ratings_total", 0),
                "price_level": place.get("price_level"),
                "types": place.get("types", [])
            }
        except Exception as e:
            logger.warning("Error formatting place data", error=str(e))
            return None