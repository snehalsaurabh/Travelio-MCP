# Food Travel MCP Server

A **Model Context Protocol (MCP) server** that provides restaurant search and food recommendation tools for AI clients. This server integrates with Google Places API to deliver real-time restaurant data to AI applications.

## 🎯 What is MCP?

**Model Context Protocol (MCP)** enables AI applications to access external tools and data sources through a standardized interface.

- **MCP Server** (this project): Exposes food-related tools to AI clients
- **MCP Client** (Claude Desktop, custom AI agents): Calls our tools based on user prompts

### How it Works
```
User: "Find Italian restaurants near me"
    ↓
AI Client (Claude/Custom Agent)
    ↓ (analyzes prompt, decides to call search_restaurants tool)
Our MCP Server
    ↓ (calls Google Places API)
Real Restaurant Data
    ↓ (returns structured JSON to AI client)
AI Client formats response for user
```

## 🚀 Features

- **Real-time restaurant search** using Google Places API
- **Location-based filtering** with customizable radius
- **Cuisine-type filtering** (Italian, Chinese, etc.)
- **Flexible parameters** (max results, price level)
- **Database caching** for improved performance
- **Comprehensive testing suite**
- **Production-ready architecture**

## 📋 Prerequisites

- Python 3.8 or higher
- Google Places API key ([Get one here](https://developers.google.com/maps/documentation/places/web-service/get-api-key))
- Git

## 🛠️ Installation

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd Food-Travel-MCP
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your Google Places API key
# Replace "your_google_places_api_key_here" with your actual API key
```

**Required environment variables in `.env`:**
```env
GOOGLE_PLACES_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite:///./food_travel.db
DEBUG=false
```

### Step 5: Initialize Database
```bash
python scripts/init_db.py
```

You should see:
```
Creating database tables...
Database tables created successfully!
```


## 🧪 Testing

### Quick Test (Recommended)
```bash
# Run all tests in sequence
python tests/run_all_tests.py
```

### Individual Test Components
```bash
# Test Google Places API integration
python tests/test_components.py

# Test MCP tools functionality  
python tests/test_mcp_tools.py
```

### Using Pytest (Advanced)
```bash
# Install pytest if not already included
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run with output
pytest tests/ -v -s
```

### Expected Test Output
✅ **Component Tests**: Verify Google Places API connectivity and data formatting  
✅ **MCP Tools Tests**: Verify tools accept parameters and return proper JSON responses  
✅ **Integration Tests**: End-to-end functionality verification

## 🎮 Running the Server

### Start the MCP Server
```bash
python -m src.food_mcp.server
```

**Expected output:**
```
INFO Food Travel MCP Server initialized
INFO Restaurant tools registered
INFO Starting Food Travel MCP Server
[Server running and waiting for MCP client connections...]
```


### Server Endpoints

The server exposes the following MCP tools:

#### `search_restaurants`
Search for restaurants based on location and preferences.

**Parameters:**
- `location` (required): "New York, NY" or "40.7128,-74.0060"
- `cuisine_type` (optional): "Italian", "Chinese", "Pizza", etc.
- `radius_km` (optional): Search radius in kilometers (default: 10)
- `max_results` (optional): Maximum results to return (default: 10)

**Example Response:**
```json
{
  "success": true,
  "location": "New York, NY",
  "total_results": 5,
  "restaurants": [
    {
      "google_place_id": "ChIJ...",
      "name": "Tony's Italian Restaurant",
      "address": "123 Main St, New York, NY",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "rating": 4.5,
      "user_ratings_total": 127,
      "price_level": 2,
      "types": ["restaurant", "food"]
    }
  ]
}
```

## 📁 Project Structure

```
Food-Travel-MCP/
├── 📄 README.md                 # This file
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example             # Environment template
├── 📄 .gitignore               # Git ignore rules
│
├── 📁 config/                  # Configuration
│   ├── __init__.py
│   └── settings.py             # Application settings
│
├── 📁 src/food_mcp/           # Main MCP server package
│   ├── __init__.py
│   ├── server.py              # MCP server entry point
│   │
│   ├── 📁 models/             # Database models
│   │   ├── __init__.py
│   │   ├── base.py            # Database base & session
│   │   └── restaurant.py      # Restaurant cache model
│   │
│   ├── 📁 clients/            # External API clients
│   │   ├── __init__.py
│   │   └── google_places.py   # Google Places API client
│   │
│   ├── 📁 services/           # Business logic layer
│   │   ├── __init__.py
│   │   └── restaurant_service.py
│   │
│   └── 📁 tools/              # MCP tool definitions
│       ├── __init__.py
│       └── restaurant_tools.py # Restaurant search tools
│
├── 📁 tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── test_components.py     # Component tests
│   ├── test_mcp_tools.py      # MCP tools tests
│   └── run_all_tests.py       # Test runner
│
└── 📁 scripts/                # Utility scripts
    └── init_db.py             # Database initialization
```


## 🔧 Development Workflow

### 1. Development Setup
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt

# Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### 2. Making Changes
```bash
# Run tests before making changes
python tests/run_all_tests.py

# Make your changes...

# Run tests again to ensure nothing broke
python tests/run_all_tests.py

# Test server startup
python -m src.food_mcp.server
```

### 3. Adding New Tools
1. Create tool function in `src/food_mcp/tools/`
2. Register tool in `__init__.py`
3. Add corresponding service logic in `src/food_mcp/services/`
4. Write tests in `tests/`
5. Update documentation

## 🌟 Usage Examples

### With Claude Desktop
1. Install Claude Desktop
2. Configure MCP server in Claude's settings
3. Ask: "Find Italian restaurants near Times Square"

### With Custom MCP Client
```python
# Example client code
import asyncio
from mcp_client import MCPClient

async def find_restaurants():
    client = MCPClient("food-travel-mcp")
    
    result = await client.call_tool(
        "search_restaurants",
        location="San Francisco, CA",
        cuisine_type="Italian",
        max_results=5
    )
    
    print(result)
```

## 🚧 Current Phase: Phase 1 - Basic Restaurant Search

### ✅ Completed
- [x] Production-ready project structure
- [x] Google Places API integration
- [x] Basic restaurant search tool
- [x] Database models and caching structure
- [x] Comprehensive testing suite
- [x] Error handling and validation

### 🔄 In Progress
- [ ] Database caching implementation
- [ ] Performance optimization
- [ ] Additional restaurant tools (menu, reviews)

### 📅 Future Phases
- **Phase 2**: User personalization integration with existing backend
- **Phase 3**: Menu data and ordering capabilities
- **Phase 4**: Enhanced AI features and trend analysis
- **Phase 5**: Production deployment and monitoring

## 🐛 Troubleshooting

### Common Issues

**Import Error: `ModuleNotFoundError: No module named 'src'`**
```bash
# Make sure you're running from project root
cd Food-Travel-MCP
python scripts/init_db.py
```

**Google Places API Error**
```bash
# Check your API key in .env file
cat .env | grep GOOGLE_PLACES_API_KEY

# Verify API key has Places API enabled in Google Console
```

**Database Issues**
```bash
# Reinitialize database
rm food_travel.db  # if using SQLite
python scripts/init_db.py
```

**Test Failures**
```bash
# Check API key configuration
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key configured:', bool(os.getenv('GOOGLE_PLACES_API_KEY')))"

# Run individual test components
python tests/test_components.py
```

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review test output for specific errors
3. Ensure all prerequisites are met
4. Verify Google Places API key is valid and has proper permissions

## 🎉 Quick Start Summary

```bash
# 1. Setup
git clone <repo> && cd Food-Travel-MCP
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your Google Places API key

# 3. Initialize
python scripts/init_db.py

# 4. Test
python tests/run_all_tests.py

# 5. Run
python -m src.food_mcp.server
```

**🎯 You're ready to integrate with AI clients and start finding restaurants!**