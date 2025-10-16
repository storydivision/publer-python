# Contributing to Publer API Python Client

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A Publer Business or Enterprise account (for testing)

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/yourusername/publer-api.git
cd publer-api
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install in development mode**

```bash
pip install -e ".[dev]"
```

4. **Set up pre-commit hooks**

```bash
pre-commit install
```

5. **Configure your environment**

```bash
cp .env.example .env
# Edit .env and add your Publer API key
```

## Development Workflow

### Code Style

We use several tools to maintain code quality:

- **black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking
- **ruff**: Linting

Run all checks:

```bash
# Format code
black publer tests examples

# Sort imports
isort publer tests examples

# Type check
mypy publer

# Lint
ruff check publer tests examples
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=publer --cov-report=html

# Run specific test file
pytest tests/test_client.py -v

# Run specific test
pytest tests/test_client.py::test_client_initialization -v
```

### Adding New Features

1. **Create a feature branch**

```bash
git checkout -b feature/your-feature-name
```

2. **Implement your feature**

Follow the architecture patterns in `.cascade/rules`:
- Add models in `publer/models/`
- Add resource classes in `publer/resources/`
- Update the client if needed

3. **Add tests**

Every new feature should have corresponding tests in `tests/`.

4. **Update documentation**

- Add docstrings to all public methods
- Update README.md if needed
- Add examples in `examples/` for major features

5. **Run all checks**

```bash
# Format and lint
black publer tests
isort publer tests
ruff check publer tests

# Type check
mypy publer

# Run tests
pytest
```

6. **Commit your changes**

```bash
git add .
git commit -m "feat: add support for X endpoint"
```

We follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

7. **Push and create a pull request**

```bash
git push origin feature/your-feature-name
```

Then open a pull request on GitHub.

## Project Structure

```
publer-api/
├── publer/              # Main package
│   ├── __init__.py
│   ├── client.py        # Main client classes
│   ├── session.py       # HTTP session management
│   ├── exceptions.py    # Custom exceptions
│   ├── models/          # Pydantic models
│   ├── resources/       # API resource classes
│   └── utils/           # Utility functions
├── tests/               # Test suite
├── examples/            # Usage examples
├── .cascade/            # Development rules
└── docs/                # Documentation (future)
```

## Adding New Endpoints

To add support for a new API endpoint:

1. **Create a Pydantic model** in `publer/models/`

```python
# publer/models/posts.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    """A Publer post."""
    id: str
    text: str
    state: str
    scheduled_at: Optional[datetime] = None
```

2. **Create a resource class** in `publer/resources/`

```python
# publer/resources/posts.py
from typing import List
from publer.resources.base import BaseResource
from publer.models.posts import Post

class PostsResource(BaseResource):
    """Posts API endpoints."""
    
    def list(self, state: Optional[str] = None) -> List[Post]:
        """List posts."""
        params = {}
        if state:
            params["state"] = state
        
        response = self._get("/posts", params=params)
        return [Post(**item) for item in response["posts"]]
```

3. **Add the resource to the client** in `publer/client.py`

```python
from publer.resources.posts import PostsResource

class PublerClient:
    def __init__(self, ...):
        # ... existing code ...
        self._posts = None
    
    @property
    def posts(self) -> PostsResource:
        """Access posts endpoints."""
        if self._posts is None:
            self._posts = PostsResource(self._session)
        return self._posts
```

4. **Add tests** in `tests/test_posts.py`

5. **Update exports** in `publer/__init__.py` if needed

## Testing Guidelines

- Write tests for all new features
- Aim for >90% code coverage
- Use `respx` to mock HTTP requests
- Test both success and error cases
- Test both sync and async clients

Example test:

```python
import respx
import httpx
from publer import PublerClient

@respx.mock
def test_list_posts(client):
    # Mock the API response
    respx.get("/posts").mock(
        return_value=httpx.Response(
            200,
            json={"posts": [{"id": "1", "text": "Hello"}]}
        )
    )
    
    # Test the method
    posts = client.posts.list()
    assert len(posts) == 1
    assert posts[0].id == "1"
```

## Documentation

- Use Google-style docstrings
- Include type hints for all parameters and return values
- Add examples for complex operations
- Keep README.md up to date

## Questions?

If you have questions or need help:

1. Check existing issues on GitHub
2. Read the API documentation at https://publer.com/docs
3. Open a new issue with the `question` label

## Code of Conduct

Be respectful and constructive in all interactions. We're all here to build something useful together.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
