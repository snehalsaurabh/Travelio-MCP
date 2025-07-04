"""Main MCP Server."""

import asyncio
from mcp import McpServer
import structlog

from config.settings import settings
from .services import RestaurantService
from .tools import register_restaurant_tools

logger = structlog.get_logger()

class FoodTravelMCPServer:
    """Food Travel MCP Server that exposes restaurant tools."""

    def __init__(self):
        self.server = McpServer("food-travel-mcp")
        
        # Initialize services
        self.restaurant_service = RestaurantService()
        
        # Register tools
        self._setup_tools()
        
        logger.info("Food Travel MCP Server initialized")

    def _setup_tools(self):
        """Set up MCP tools."""
        register_restaurant_tools(self.server, self.restaurant_service)
        logger.info("Restaurant tools registered")

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting Food Travel MCP Server")
        
        # Run the MCP server
        async with self.server:
            await self.server.run()


async def main():
    """Entry point."""
    server = FoodTravelMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())