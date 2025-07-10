# Contributing to NeruCord Archiver

Thank you for your interest in contributing to NeruCord Archiver! This document provides guidelines for contributors.

## Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/yourusername/nerucordarchiver.git
cd nerucordarchiver
```

3. Install dependencies:
```bash
python setup.py
```

## Development Workflow

### Branch Strategy

- `main`: Production-ready code
- `dev`: Development branch for integration
- `feature/*`: Feature development branches
- `bugfix/*`: Bug fix branches

### Creating a Feature

1. Create a feature branch from `dev`:
```bash
git checkout dev
git checkout -b feature/your-feature-name
```

2. Make your changes following the coding standards
3. Add tests for new functionality
4. Ensure all tests pass:
```bash
pytest tests/ -v
```

5. Commit your changes with descriptive messages:
```bash
git commit -m "feat: add description of your feature

- Detailed description of changes
- Any breaking changes
- References to issues if applicable"
```

6. Push your branch and create a pull request to `dev`

### Commit Message Format

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Maintenance tasks

## Code Standards

### Python Style Guide

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings for all public functions and classes
- Maximum line length: 100 characters

### Architecture Guidelines

This project follows Clean Architecture principles:

1. **Domain Layer** (`src/domain/`): Business entities and value objects
2. **Use Cases Layer** (`src/use_cases/`): Application business logic
3. **Infrastructure Layer** (`src/infrastructure/`): External adapters
4. **Interface Layer** (`src/cli/`): User interface

### Testing

- Write unit tests for all new functionality
- Aim for high test coverage (>80%)
- Use descriptive test names
- Mock external dependencies

Example test structure:
```python
class TestYourFeature:
    def test_should_do_something_when_condition(self):
        # Arrange
        # Act
        # Assert
```

## Pull Request Guidelines

Before submitting a pull request:

1. Ensure your code follows the style guidelines
2. Add tests for new functionality
3. Update documentation if needed
4. Ensure all tests pass
5. Update CHANGELOG.md if applicable

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

## Issue Reporting

When reporting issues:

1. Use the issue templates provided
2. Include steps to reproduce
3. Provide system information
4. Include error messages and logs

## Development Environment

### Required Tools

- Python 3.8+
- Git
- FFmpeg (for audio conversion)

### Recommended Tools

- VS Code with Python extension
- pytest for testing
- black for code formatting

### Environment Variables

Create a `.env` file for local development:
```
DEBUG=true
LOG_LEVEL=debug
```

## Documentation

### Code Documentation

- Use clear, descriptive docstrings
- Include parameter and return type information
- Provide usage examples for complex functions

### User Documentation

- Update README.md for user-facing changes
- Add examples for new features
- Keep installation instructions current

## Performance Guidelines

- Profile code for performance-critical sections
- Avoid blocking operations in async functions
- Use appropriate data structures
- Consider memory usage for large downloads

## Security Considerations

- Validate all user inputs
- Sanitize filenames and paths
- Handle network errors gracefully
- Don't log sensitive information

## Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create release notes
4. Tag the release
5. Deploy to distribution channels

## Getting Help

- Check existing issues and documentation
- Ask questions in discussions
- Contact maintainers for complex issues

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
