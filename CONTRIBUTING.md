# Contributing to AstroDesk

Thank you for your interest in contributing to AstroDesk! We welcome contributions from the community to help make this project better.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat everyone with respect and kindness.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub. Include the following details:
*   A clear and descriptive title.
*   Steps to reproduce the bug.
*   Expected behavior vs. actual behavior.
*   Screenshots or logs, if applicable.

### Suggesting Enhancements

We love new ideas! If you have a feature request, please open an issue and describe:
*   The problem you're trying to solve.
*   Your proposed solution.
*   Any alternatives you've considered.

### Pull Requests

1.  **Fork the repository** and create a new branch for your feature or bug fix.
    ```bash
    git checkout -b feature/your-feature-name
    ```
2.  **Make your changes** and ensure the code follows the project's style guidelines.
3.  **Test your changes** to ensure they work as expected.
4.  **Commit your changes** with clear and concise commit messages.
    ```bash
    git commit -m "Add feature: your feature name"
    ```
5.  **Push to your fork** and submit a Pull Request (PR) to the `main` branch.
    ```bash
    git push origin feature/your-feature-name
    ```
6.  **Describe your PR** in detail, referencing any related issues.

## Development Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/JosephJonathanFernandes/astrodesk.git
    cd astrodesk
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up environment variables (see `.env.example`).
5.  Run the application:
    ```bash
    python app.py
    ```

## Style Guidelines

*   Follow PEP 8 for Python code.
*   Use meaningful variable and function names.
*   Add comments for complex logic.

Thank you for your contributions! 🚀
