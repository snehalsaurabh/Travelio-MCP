"""Restaurant service for business logic."""

from typing import List, Dict, Any, Optional
import structlog

from ..clients import GooglePlacesClient

logger = structlog.get_logger()


class RestaurantService:
    """Service for restaurant-related operations."""
    
    def __init__(self):
        self.google_client = GooglePlacesClient()
    
    async def search_restaurants(
        self,
        location: str,
        cuisine_type: Optional[str] = None,
        radius_km: float = 10,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for restaurants using Google Places API.
        
        Args:
            location: Location to search
            cuisine_type: Type of cuisine to filter by
            radius_km: Search radius in kilometers
            max_results: Maximum number of results to return
            
        Returns:
            List of restaurant data dictionaries
        """
        try:
            logger.info(
                "Starting restaurant search",
                location=location,
                cuisine=cuisine_type,
                radius=radius_km
            )
            
            # Convert km to meters for Google Places API
            radius_meters = int(radius_km * 1000)
            
            # Search using Google Places
            restaurants = await self.google_client.search_restaurants(
                location=location,
                radius=radius_meters,
                cuisine_type=cuisine_type
            )
            
            # Limit results
            if max_results and len(restaurants) > max_results:
                restaurants = restaurants[:max_results]
            
            logger.info(
                "Restaurant search completed",
                total_found=len(restaurants),
                location=location
            )
            
            return restaurants
            
        except Exception as e:
            logger.error("Error in restaurant service search", error=str(e))
            raise