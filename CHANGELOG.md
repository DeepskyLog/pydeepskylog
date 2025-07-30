# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- (Describe any new features or enhancements here)

### Changed
- (Describe any changes here)

### Fixed
- (Describe any bug fixes here)

---

## [1.6] - 2025-07-30

### Added
- Initial changelog file.
- Comprehensive API documentation using Sphinx.
- Detailed docstrings for mathematical formulas and astronomical concepts.
- User guide with examples for common use cases.
- Inline comments for complex calculations.
- Contributing guide for new contributors.
- Code of conduct to ensure a welcoming community.
- Logging configuration for better debugging and error tracking.
- Validation module to ensure correct parameter types and ranges.
- Unit tests for all public methods to ensure reliability.
- Continuous integration setup for automated testing.
- Refactoring of the package structure for better organization.
- Documentation for API endpoints and expected responses.
- Add development dependencies to `setup.py`.
- Implement rate limiting for API requests.
- Add input sanitization for all user inputs.
- Add template for issue reporting and feature requests.

## [1.5] - 2025-07-29

### Added

- Adds support for fetching filters from DeepskyLog
- Updates the contrast reserve calculation to directly use surface brightness if available, rather than calculating it from magnitude and object diameters.

## [1.4.1] - 2025-05-30

### Added

- Add method to get lenses from DeepskyLog.

## [1.3.2] - 2025-02-03

### Changed

- Use new instruments table from DeepskyLog.

## [1.3.1] - 2024-11-13

### Added

- Make the package typed.

## [1.3] - 2024-10-30

### Added

- Add methods to convert instrument types from string to int and vice versa.

## [1.2.1] - 2024-10-24

### Fixed

- Fix python tests

## [1.2] - 2024-10-24

### Added

- Get instruments and eyepieces from the DeepskyLog website.

## [1.1] - 2024-08-01

### Added

- Conversion of magnitudes to SQM value and bortle scale and vice versa.

## [1.0.1] - 2024-08-01

### Fixed

- Make sure all methods are correctly imported in init.py.

## [0.9] - 2024-07-31

### Added
- First version of pydeepskylog. Calculates:
    - contrast reserve
    - Optimal detection magnification