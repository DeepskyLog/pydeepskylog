# pydeepskylog User Guide

This guide provides practical examples for common use cases with the pydeepskylog package.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Magnitude and Sky Brightness Conversions](#magnitude-and-sky-brightness-conversions)
- [Contrast Reserve Calculation](#contrast-reserve-calculation)
- [Optimal Detection Magnification](#optimal-detection-magnification)
- [DeepskyLog API Integration](#deepskylog-api-integration)
- [Validation Utilities](#validation-utilities)
- [Logging Configuration](#logging-configuration)
- [API](#api)
- [Astronomical Background](#astronomical-background)
  - [Contrast Reserve](#contrast-reserve)
  - [Optimal Detection Magnification](#optimal-detection-magnification)
  - [Magnitudes](#magnitudes)

---

## Description

A Python package with utilities for deep-sky observations.
This version of pydeepskylog provides the following functionality:

+ Calculating of contrast reserve and optimal detection magnification for deep-sky objects.
+ Conversion of magnitudes to SQM value and bortle scale and vice versa.
+ Fetching instruments, eyepieces, lenses, and filters from a DeepskyLog user account.

## Installation

Install via pip:

```bash
pip install pydeepskylog
```

## Basic Usage

Import the main modules:

```python
import pydeepskylog.magnitude as mag
import pydeepskylog.contrast_reserve as cr
```

## Magnitude and Sky Brightness Conversions

Convert NELM to SQM:

```python
sqm = mag.nelm_to_sqm(6.2)
print(f"SQM: {sqm:.2f}")
```

Convert SQM to Bortle scale:

```python
bortle = mag.sqm_to_bortle(21.0)
print(f"Bortle class: {bortle}")
```

## Contrast Reserve Calculation

Calculate the contrast reserve for an object:

```python
reserve = cr.contrast_reserve(
    sqm=21.0,
    telescope_diameter=200,  # mm
    magnification=100,
    surf_brightness=None,
    magnitude=10.5,
    object_diameter1=120,  # arcsec
    object_diameter2=60    # arcsec
)
print(f"Contrast reserve: {reserve:.2f}")
```

## Optimal Detection Magnification

Find the best magnification for detection:

```python
magnifications = [50, 75, 100, 150, 200]
optimal = cr.optimal_detection_magnification(
    sqm=21.0,
    telescope_diameter=200,
    surf_brightness=None,
    magnitude=10.5,
    object_diameter1=120,
    object_diameter2=60,
    magnifications=magnifications
)
print(f"Optimal magnification: {optimal}")
```

## DeepskyLog API Integration

Fetch user instruments:

```python
from pydeepskylog.deepskylog_interface import dsl_instruments

instruments = dsl_instruments("your_username")
for inst_id, inst in instruments.items():
    print(inst["name"], inst["diameter"])
```

The API endpoints are documented in the [API Endpoints](docs/api_endpoints.md) section.

## Validation Utilities

Validate a positive number:

```python
from pydeepskylog.validation import validate_positive

validate_positive(42, "Telescope diameter")
```

## Logging Configuration

Set up logging for debugging:

```python
from pydeepskylog.logging_config import configure_logging
import logging

configure_logging(logging.DEBUG)
```

## API

Documentation for the API is available at [Read the Docs](https://pydeepskylog.readthedocs.io/en/latest/).

## Astronomical background

### Contrast Reserve

The contrast reserve is a measure of the difference in brightness between the object and the sky background. It is calculated as the difference between the object's surface brightness and the sky background brightness. The contrast reserve is a useful metric for determining the visibility of deep sky objects through a telescope.

The higher the contrast reserve, the easier it is to see the object.  The following table can be used to interpret the contrast reserve:


| Contrast Reserve | Visibility             | Typical color |
|------------------|------------------------|---------------|
| < -0.2           | Not visible            | dark grey     |
| -0.2 < CR < 0.1  | Questionable           | light grey    |
| 0.1 < CR < 0.35  | Difficult              | dark red      |
| 0.35 < CR < 0.5  | Quite difficult to see | light red     |
| 0.5 < CR < 1.0   | Easy to see            | dark green    |
| 1.0 < CR         | Very easy to see       | light green   |

The contrast reserved is calculated for the object as a whole.  Smaller details in the object might be visible even if the contrast reserve of the object as a whole is below -0.2.  This is certainly the case for galaxies, where the core might be much brighter than the outer regions.

It is important to note that the contrast reserve is a theoretical value and that the actual visibility of an object will depend on a number of other factors, including the observer's experience, the transparency of the sky, and the seeing conditions.  The contrast reserve is just a guideline.

The calculation of the contrast reserve depends heavily on the quality of the object database.  A small error in the object's magnitude or size can lead to a large error in the contrast reserve.

Only if the observer tries to observe the object, he/she will know if the object is visible or not.

### Optimal Detection Magnification

The optimal detection magnification is the magnification at which the object is most easily visible.
Take into account that the optimal detection magnification is not the same as the best magnification for observing details in an object, but for the object as a whole.

### Magnitudes

Conversion methods are provided to convert magnitudes to SQM value and bortle scale and vice versa.

Different formulae are available to convert magnitudes to SQM value.  The formula used here converts a sqm value of 22.0 to a naked eye limiting magnitude of 6.6.  The faintest star offset can be given to the formula.  If taking a value of -1.4 for the faintest star offset, the formula converts a sqm value of 22.0 to a naked eye limiting magnitude of 8.0.

| Measurement   | Description                                                                                      | Conversion Functions                  |
|---------------|--------------------------------------------------------------------------------------------------|---------------------------------------|
| NELM          | Naked Eye Limiting Magnitude, the faintest star visible to the naked eye under ideal conditions. | `nelm_to_sqm()`, `nelm_to_bortle()`   |
| SQM           | Sky Quality Meter, a measure of sky brightness in magnitudes per square arcsecond.               | `sqm_to_nelm()`, `sqm_to_bortle()`    |
| Bortle Scale  | A qualitative scale that classifies the night sky based on light pollution and visibility.       | `bortle_to_nelm()`, `bortle_to_sqm()` |

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## License

[GPL-3.0](LICENSE)

## Acknowledgements

This package is inspired by the [DeepskyLog](https://www.deepskylog.org/) website and the code is based on the formulas used in DeepskyLog.  We would like to thank the DeepskyLog developers team.
