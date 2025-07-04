"""Run all tests in sequence with detailed output."""

import asyncio
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tests.test_components import run_component_tests
from tests.test_mcp_tools import run_mcp_tool_tests


async def main():
    """Run all tests in sequence."""
    print("🚀 Food Travel MCP Server - Full Test Suite")
    print("=" * 50)
    
    # Test 1: Component Tests
    print("\n📋 PHASE 1: Component Testing")
    print("-" * 30)
    component_success = await run_component_tests()
    
    if not component_success:
        print("\n❌ Component tests failed. Stopping here.")
        return False
    
    # Test 2: MCP Tools Tests
    print("\n📋 PHASE 2: MCP Tools Testing")
    print("-" * 30)
    tools_success = await run_mcp_tool_tests()
    
    if not tools_success:
        print("\n❌ MCP tools tests failed.")
        return False
    
    # All tests passed
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("✅ Components working correctly")
    print("✅ MCP tools functioning properly")
    print("✅ Ready for server startup testing")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)