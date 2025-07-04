"""Restaurant search MCP tools."""

import json
from typing import Optional
from mcp import McpServer
from mcp.types import Tool, CallToolResult, TextContent
import structlog

logger = structlog.get_logger()


def register_restaurant_tools(server: McpServer, restaurant_service):
    """Register restaurant-related MCP tools."""
    
    @server.tool("search_restaurants")
    async def search_restaurants(
        location: str,
        cuisine_type: Optional[str] = None,
        radius_km: Optional[float] = None,
        max_results: Optional[int] = None
    ) -> CallToolResult:
        """
        Search for restaurants based on location and preferences.
        
        Args:
            location: Location to search (e.g., "New York, NY" or "40.7128,-74.0060")
            cuisine_type: Type of cuisine (e.g., "Italian", "Chinese") [optional]
            radius_km: Search radius in kilometers (default: 10) [optional]
            max_results: Maximum number of results (default: 10) [optional]
            
        Returns:
            List of restaurants with details like name, address, rating, etc.
        """
        try:
            logger.info(
                "Restaurant search requested",
                location=location,
                cuisine=cuisine_type,
                radius=radius_km,
                max_results=max_results
            )
            
            # Use the restaurant service to perform the search
            restaurants = await restaurant_service.search_restaurants(
                location=location,
                cuisine_type=cuisine_type,
                radius_km=radius_km or 10,  # Default 10km
                max_results=max_results or 10  # Default 10 results
            )
            
            # Format the response
            result = {
                "success": True,
                "location": location,
                "total_results": len(restaurants),
                "restaurants": restaurants
            }
            
            logger.info(
                "Restaurant search completed",
                location=location,
                results_count=len(restaurants)
            )
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))]
            )
            
        except Exception as e:
            logger.error("Error in restaurant search", error=str(e), location=location)
            
            error_result = {
                "success": False,
                "error": str(e),
                "location": location
            }
            
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(error_result, indent=2))],
                isError=True
            )