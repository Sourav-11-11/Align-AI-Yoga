# Contributing to Align AI Yoga

Thank you for your interest in contributing! This project welcomes contributions from developers of all skill levels.

## How to Contribute

### 1. Report Issues
- Found a bug? Create an issue with:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs actual behavior
  - Your environment (OS, Python version, browser)

### 2. Suggest Features
- Have an idea? Create a feature request issue with:
  - Clear use case
  - Why it would be valuable
  - Any implementation ideas

### 3. Submit Code Changes

#### Setup Development Environment
```bash
pip install -r requirements.txt
cd frontend
make run-local
```

#### Make Your Changes
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Write clean, documented code
3. Follow the existing code style
4. Add docstrings to functions
5. Test your changes: `pytest tests/`

#### Commit Guidelines
- Use meaningful commit messages: `git commit -m "feature: add new pose analysis mode"`
- Keep commits focused and atomic
- Reference issues when relevant: `fix: resolve #123`

#### Push & Create Pull Request
1. Push to your fork: `git push origin feature/your-feature-name`
2. Create a PR with clear description
3. Link any related issues
4. Wait for code review and address feedback

## Code Standards

### Python Style
- Follow PEP 8
- Use 4 spaces for indentation
- Max line length: 100 characters
- Write docstrings for all functions

### Naming Conventions
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

### Documentation
- Add docstrings explaining:
  - What the function does
  - Parameters and types
  - Return values
  - Example usage if complex

## Testing

```bash
# Run tests
cd frontend && pytest tests/ -v

# Run specific test
cd frontend && pytest tests/test_auth.py::test_login -v

# Check coverage
cd frontend && pytest --cov=app tests/
```

## Project Structure Guidelines

- **routes/**: HTTP endpoints and form handling
- **services/**: Business logic and ML orchestration
- **ml/**: Pure ML utilities (angle calculation, pose detection, etc.)
- **utils/**: Reusable helpers (database, file operations)
- **templates/**: HTML pages (don't modify structure)

## Performance Considerations

- **ML Operations**: Lazy-load heavy imports (MediaPipe, sklearn)
- **Database**: Use parameterized queries to prevent SQL injection
- **Caching**: Cache expensive computations (recommender build, pose guides)

## Security Guidelines

- Never commit `.env` files with real secrets
- Use environment variables for sensitive data
- Validate all user input
- Use parameterized SQL queries
- Hash passwords with Werkzeug

## Getting Help

- Check existing issues and PRs
- Read the main [README.md](README.md)
- See [ARCHITECTURE.md](ARCHITECTURE.md) for design decisions
- Ask questions in PR comments

---

**Thank you for contributing! 🙏**
