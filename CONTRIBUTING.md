# Contributing to PyDeepSkyLog

Thank you for your interest in contributing to PyDeepSkyLog! We welcome contributions of all kinds, including bug reports, feature requests, code, and documentation.

## Getting Started

1. **Fork the repository** on GitHub and clone your fork locally.
2. **Set up a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install the dependencies**:

   ```bash
   pip install -e .
   ```
   
## Coding Standards

- We follow the PEP 8 style guide for Python code. Please ensure your code adheres to these standards. You can use tools like `flake8` or `black` to check and format your code.
- Use type hints and docstrings to document your code. This helps maintain clarity and usability.
- Write unit tests for any new features or bug fixes. Ensure that all tests pass before submitting your changes.
- Commit your changes with clear, descriptive commit messages. Use the format `Fix: <issue description>` for bug fixes and `Feature: <feature description>` for new features.

## Testing

- Run the test suite to ensure that your changes do not break existing functionality:

  ```bash
  python -m unittest discover pydeepskylog/tests
  ```
  
- Ensure that all tests pass before submitting your pull request. If you are adding new features, please include tests for those features as well.
- If you are fixing a bug, please include a test that reproduces the bug and verifies that it is fixed.
- If you are adding a new feature, please include tests that verify the feature works as expected.
- If you are making changes to existing code, please ensure that the tests for that code still pass.
- If you are making changes to the API, please ensure that the API documentation is updated accordingly.
- If you are making changes to the documentation, please ensure that the documentation is updated accordingly.

## Submitting Changes

- Push your changes to your forked repository.
- Open a pull request against the `main` branch of the original repository.
- Provide a clear description of the changes you made, including any relevant issue numbers.
- Be responsive to feedback and be prepared to make changes based on code review comments.
- If your pull request addresses an existing issue, please reference it in the pull request description (e.g., "Fixes #123").
- If your pull request is a work in progress, please mark it as such and indicate what still needs to be done.
- If your pull request is ready for review, please remove the "WIP" label and indicate that it is ready for review.
- If your pull request is accepted, it will be merged into the main branch. You will receive credit for your contribution in the commit history.
- If your pull request is rejected, please don't be discouraged. We appreciate your effort and encourage you to continue contributing in the future.
- If you have any questions or need help, please feel free to ask in the pull request comments or open an issue.
- If you are working on a large feature or change, consider opening an issue first to discuss your plans and get feedback before starting work.
- If you are working on a new feature, consider creating a separate branch for your work. This allows you to keep your changes organized and makes it easier to submit a pull request when you are ready.
- If you are working on a bug fix, consider creating a separate branch for your work. This allows you to keep your changes organized and makes it easier to submit a pull request when you are ready.

## Reporting Issues
If you find a bug or have a feature request, please open an issue on GitHub. When reporting an issue, please include the following information:
- A clear description of the issue or feature request.
- Steps to reproduce the issue, if applicable.
- Any relevant error messages or logs.
- The version of pydeepskylog you are using.
- Your operating system and Python version.
- Any other relevant information that might help us understand the issue.
- If you are reporting a bug, please include a minimal example that reproduces the issue. This helps us quickly identify and fix the problem.
- If you are reporting a feature request, please include a clear description of the feature and how it would be useful.
- If you are reporting a security issue, please do not open an issue on GitHub. Instead, please contact us directly at [deepskywim@gmail.com](mailto:deepskywim@gmail.com) to report the issue privately. We take security issues seriously and will work with you to resolve them as quickly as possible.
- If you are unsure whether an issue is a bug or a feature request, please open an issue and we will help you determine the best course of action.
- If you are reporting an issue that has already been reported, please add a comment to the existing issue instead of opening a new one. This helps us keep track of issues and avoid duplicates.

## Code of Conduct

We expect all contributors to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

