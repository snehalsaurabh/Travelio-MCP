"""Test MCP tools directly without full MCP client."""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import asyncio
import json
import pytest
from dotenv import load_dotenv

load_dotenv()

from src.food_mcp.services.restaurant_service import RestaurantService
from src.food_mcp.tools.restaurant_tools import register_restaurant_tools

class MockMCPServer:
    """Mock MCP server for testing tools."""
    
    def __init__(self):
        self.tools = {}
    
    def tool(self, name):
        """Decorator to register tools."""
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator
    
    async def call_tool(self, tool_name, **kwargs):
        """Call a registered tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        
        tool_func = self.tools[tool_name]
        return await tool_func(**kwargs)


class TestMCPTools:
    """Test MCP tools functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test environment."""
        import os
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        if not api_key or api_key == "your_google_places_api_key_here":
            pytest.skip("GOOGLE_PLACES_API_KEY not configured")
        
        # Set up mock server and register tools
        self.mock_server = MockMCPServer()
        self.restaurant_service = RestaurantService()
        register_restaurant_tools(self.mock_server, self.restaurant_service)
    
    async def test_search_restaurants_basic(self):
        """Test basic restaurant search tool."""
        print("\n=== Testing Basic Restaurant Search ===")
        
        # Call the tool
        result = await self.mock_server.call_tool(
            "search_restaurants",
            location="New York, NY"
        )
        
        # Parse result
        content = result.content[0].text
        data = json.loads(content)
        
        # Assertions
        assert data.get("success") is True, f"Search should succeed: {data.get('error')}"
        assert "restaurants" in data, "Response should contain restaurants"
        assert "total_results" in data, "Response should contain total_results"
        assert data["location"] == "New York, NY", "Should echo back location"
        
        print(f"✅ Found {data['total_results']} restaurants")
        
        if data['restaurants']:
            first = data['restaurants'][0]
            print(f"   Example: {first['name']} (Rating: {first['rating']})")
        
        return data
    
    async def test_search_restaurants_with_params(self):
        """Test restaurant search with all parameters."""
        print("\n=== Testing Restaurant Search with Parameters ===")
        
        # Call tool with all parameters
        result = await self.mock_server.call_tool(
            "search_restaurants",
            location="San Francisco, CA",
            cuisine_type="Italian",
            radius_km=5,
            max_results=3
        )
        
        # Parse result
        content = result.content[0].text
        data = json.loads(content)
        
        # Assertions
        assert data.get("success") is True, f"Search should succeed: {data.get('error')}"
        assert len(data['restaurants']) <= 3, "Should respect max_results limit"
        
        print(f"✅ Found {data['total_results']} Italian restaurants in SF")
        
        for i, restaurant in enumerate(data['restaurants'], 1):
            print(f"   {i}. {restaurant['name']} - Rating: {restaurant['rating']}")
        
        return data
    
    async def test_search_restaurants_invalid_location(self):
        """Test restaurant search with invalid location."""
        print("\n=== Testing Invalid Location Handling ===")
        
        try:
            result = await self.mock_server.call_tool(
                "search_restaurants",
                location="INVALID_LOCATION_XYZ123"
            )
            
            content = result.content[0].text
            data = json.loads(content)
            
            # Should either succeed with 0 results or fail gracefully
            if data.get("success"):
                print(f"✅ Handled gracefully: {data['total_results']} results")
            else:
                print(f"✅ Failed gracefully: {data.get('error')}")
            
            return data
            
        except Exception as e:
            print(f"✅ Exception handled: {e}")
            return None


# Standalone function for manual testing
async def run_mcp_tool_tests():
    """Run MCP tool tests manually (outside pytest)."""
    print("🛠️ Testing MCP Tools")
    
    try:
        test_instance = TestMCPTools()
        test_instance.setup()
        
        # Run all tests
        await test_instance.test_search_restaurants_basic()
        await test_instance.test_search_restaurants_with_params()
        await test_instance.test_search_restaurants_invalid_location()
        
        print("\n🎉 All MCP tool tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    # Run tests directly when called as script
    asyncio.run(run_mcp_tool_tests())