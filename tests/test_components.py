"""Test individual components before running full MCP server."""

import asyncio
import os
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.food_mcp.clients.google_places import GooglePlacesClient
from src.food_mcp.services.restaurant_service import RestaurantService


class TestComponents:
    """Test individual components of the MCP server."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test environment."""
        # Check if API key is configured
        self.api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        if not self.api_key or self.api_key == "your_google_places_api_key_here":
            pytest.skip("GOOGLE_PLACES_API_KEY not configured in .env file")
    
    async def test_google_places_client(self):
        """Test Google Places client directly."""
        print("\n=== Testing Google Places Client ===")
        
        client = GooglePlacesClient()
        
        # Test basic search
        restaurants = await client.search_restaurants(
            location="New York, NY",
            radius=5000,  # 5km in meters
            cuisine_type="Italian"
        )
        
        # Assertions
        assert isinstance(restaurants, list), "Should return a list"
        print(f"✅ Found {len(restaurants)} restaurants")
        
        if restaurants:
            first_restaurant = restaurants[0]
            assert "name" in first_restaurant, "Restaurant should have a name"
            assert "google_place_id" in first_restaurant, "Should have place ID"
            assert "rating" in first_restaurant, "Should have rating"
            print(f"   Example: {first_restaurant['name']} (Rating: {first_restaurant['rating']})")
        
        return restaurants

    async def test_restaurant_service(self):
        """Test restaurant service layer."""
        print("\n=== Testing Restaurant Service ===")
        
        service = RestaurantService()
        
        # Test service search with various parameters
        restaurants = await service.search_restaurants(
            location="San Francisco, CA",
            cuisine_type="Pizza",
            radius_km=5,
            max_results=3
        )
        
        # Assertions
        assert isinstance(restaurants, list), "Should return a list"
        assert len(restaurants) <= 3, "Should respect max_results limit"
        print(f"✅ Service returned {len(restaurants)} restaurants")
        
        for i, restaurant in enumerate(restaurants, 1):
            assert "name" in restaurant, f"Restaurant {i} should have a name"
            assert "rating" in restaurant, f"Restaurant {i} should have a rating"
            print(f"   {i}. {restaurant['name']} - Rating: {restaurant['rating']}")
        
        return restaurants


# Standalone functions for manual testing
async def run_component_tests():
    """Run component tests manually (outside pytest)."""
    print("🧪 Testing Food Travel MCP Components")
    
    # Check API key
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key or api_key == "your_google_places_api_key_here":
        print("❌ Please set GOOGLE_PLACES_API_KEY in your .env file")
        return False
    
    print(f"✅ API key configured: {api_key[:10]}...")
    
    try:
        test_instance = TestComponents()
        test_instance.setup()
        
        # Run tests
        print("\n--- Testing Google Places Client ---")
        await test_instance.test_google_places_client()
        
        print("\n--- Testing Restaurant Service ---")
        await test_instance.test_restaurant_service()
        
        print("\n🎉 All component tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    # Run tests directly when called as script
    asyncio.run(run_component_tests())