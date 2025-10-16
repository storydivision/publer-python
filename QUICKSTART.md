# Quick Start Guide

Get up and running with the Publer API Python client in minutes.

## Installation

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .
```

### 2. Configure Your API Key

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` and add your Publer API key:

```env
PUBLER_API_KEY=your_actual_api_key_here
```

**Get your API key:**
1. Log in to [Publer](https://publer.com)
2. Go to Settings → Access & Login → API Keys
3. Generate a new API key
4. Copy it to your `.env` file

### 3. Test the Connection

Run the included verification script:

```bash
python verify_setup.py
```

This will check:
- ✓ Project structure
- ✓ Package imports
- ✓ Environment file
- ✓ API key
- ✓ API connection

If all checks pass, you're ready to go! 🎉

Alternatively, run the quick test script:

```bash
python test_api.py
```

This will fetch your workspaces, accounts, and posts to verify everything works.

## Basic Usage

### Synchronous Client

```python
from publer import PublerClient

# Using context manager (recommended)
with PublerClient() as client:
    # Get workspaces
    workspaces = client.workspaces.list()
    print(f"Found {len(workspaces)} workspace(s)")
    
    # Set active workspace
    client.set_workspace(workspaces[0].id)
    
    # Get accounts
    accounts = client.accounts.list()
    print(f"Found {len(accounts)} account(s)")
    
    # Create a post
    result = client.posts.create(
        text="Hello from Publer API!",
        accounts=[accounts[0].id],
        scheduled_at="2025-10-20T10:00:00+00:00"
    )
    print(f"Post created! Job ID: {result['job_id']}")
```

### Asynchronous Client

```python
import asyncio
from publer import AsyncPublerClient

async def main():
    async with AsyncPublerClient() as client:
        # Get workspaces
        workspaces = await client.workspaces.list()
        print(f"Found {len(workspaces)} workspace(s)")
        
        # Set active workspace
        client.set_workspace(workspaces[0].id)
        
        # Get accounts
        accounts = await client.accounts.list()
        print(f"Found {len(accounts)} account(s)")

asyncio.run(main())
```

## Next Steps

### For Development

1. **Run tests** to make sure everything works:
   ```bash
   pip install -e ".[dev]"
   pytest
   ```

2. **Check code quality**:
   ```bash
   black publer tests
   mypy publer
   pytest --cov=publer
   ```

3. **Read the architecture** in `.cascade/rules` to understand the project structure

### Implementing New Features

The core structure is ready! Now you can add:

1. **Models** in `publer/models/` - Pydantic models for API data
2. **Resources** in `publer/resources/` - API endpoint implementations
3. **Tests** in `tests/` - Test each new feature
4. **Examples** in `examples/` - Show how to use new features

See `CONTRIBUTING.md` for detailed instructions on adding new endpoints.

## Common Issues

### "API key is required"

Make sure your `.env` file exists and contains:
```env
PUBLER_API_KEY=your_key_here
```

### "Authentication failed"

- Check that your API key is correct
- Ensure you have a Business or Enterprise Publer plan
- Verify the API key hasn't been revoked

### Import errors

Make sure you installed the package:
```bash
pip install -e .
```

## Examples

Check the `examples/` directory for more usage examples:

- `examples/basic_usage.py` - Synchronous client examples
- `examples/async_usage.py` - Asynchronous client examples
- `examples/advanced_usage.py` - Job polling, media upload, analytics

## Resources

- **API Documentation**: https://publer.com/docs
- **Project README**: See `README.md` for full documentation
- **Contributing Guide**: See `CONTRIBUTING.md` for development guidelines
- **Architecture Rules**: See `.cascade/rules` for design patterns

## Need Help?

- Open an issue on GitHub
- Check the Publer API documentation
- Review the examples in the `examples/` directory

Happy coding! 🚀
