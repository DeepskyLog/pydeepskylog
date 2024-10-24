# pydeepskylog

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Astronomical background](#astronomical-background)
  - [Contrast Reserve](#contrast-reserve)
  - [Optimal Detection Magnification](#optimal-detection-magnification)
  - [Magnitudes](#magnitudes)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Description

A Python package with utilities for deep-sky observations.
This version of pydeepskylog provides the following functionality:

+ Calculating of contrast reserve and optimal detection magnification for deep-sky objects.
+ Conversion of magnitudes to SQM value and bortle scale and vice versa.

In the future, it will also include utilities for fetching and adding observation logs from/to the DeepSkyLog website.

## Installation

```bash
pip install pydeepskylog
```

## Usage

```python
import pydeepskylog as pds

# Calculate contrast reserve. The object diameters are given in arc seconds.
contrast_reserve = pds.contrast_reserve(sqm=22, telescope_diameter=457, magnification=118, magnitude=11,
                                        object_diameter1=600, object_diameter2=600)
print(contrast_reserve)

# Define a list of possible magnifications
possible_magnifications = [50, 100, 150, 200, 250]

# Calculate optimal detection magnification
optimal_detection_magnification = pds.optimal_detection_magnification(sqm=22, telescope_diameter=457, magnitude=11,
                                                                      object_diameter1=600, object_diameter2=600,
                                                                      magnifications=possible_magnifications)
print(optimal_detection_magnification)

# Convert naked eye limiting magnitude to SQM value
sqm = pds.nelm_to_sqm(5.8)

# Convert SQM value to naked eye limiting magnitude
nelm = pds.sqm_to_nelm(21.4)

# Convert Bortle scale to SQM value
print(pds.bortle_to_sqm(4))

# Convert SQM value to Bortle scale
print(pds.sqm_to_bortle(21.4))

# Convert naked eye limiting magnitude to bortle scale
print(pds.nelm_to_bortle(5.8))

# Convert bortle scale to naked eye limiting magnitude
print(pds.bortle_to_nelm(4))

# Get all defined instruments of a DeepskyLog user
print(pds.dsl_instruments('username'))

# Get all defined eyepieces of a DeepskyLog user
print(pds.dsl_eyepieces('username'))

# Get a list of possible magnifications for a given telescope and the eyepieces as defined in DeepskyLog
telescope = pds.dsl_instruments('username')[0]
print (pds.calculate_magnifications(, telescope))
```

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

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Acknowledgements

This package is inspired by the [DeepskyLog](https://www.deepskylog.org/) website and the code is based on the formulas used in DeepskyLog.  We would like to thank the DeepskyLog developers team.
