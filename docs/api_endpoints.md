## DeepskyLog API Endpoints

The following endpoints are used to retrieve user-specific astronomical equipment data from the DeepskyLog API.

Base URL:
https://test.deepskylog.org/api/

### Instruments

- Endpoint: /api/instrument/{username}
- Description: Returns all telescopes and observing instruments for the specified user.
- Method: GET
- Response:
```JSON
{
  "123": {
    "id": 123,
    "name": "8\" Dobsonian",
    "diameter": 200,
    "fd": 6,
    "fixedMagnification": null,
    ...
  },
  ...
}
```

### Eyepieces

- Endpoint: /api/eyepieces/{username}
- Description: Returns all eyepieces for the specified user.
- Method: GET
- Response:
```JSON
{
  "456": {
    "id": 456,
    "name": "Plössl 25mm",
    "focal_length_mm": 25,
    "eyepieceactive": true,
    ...
  },
  ...
}
```

### Lenses

- Endpoint: /api/lenses/{username}
- Description: Returns all lenses for the specified user.
- Method: GET
- Response:
```JSON
{
  "789": {
    "id": 789,
    "name": "Barlow 2x",
    "focal_length_mm": 2,
    ...
  },
  ...
}
```

### Filters

- Endpoint: /api/filters/{username}
- Description: Returns all filters for the specified user.
- Method: GET
- Response:
```JSON
{
  "321": {
    "id": 321,
    "name": "UHC Filter",
    "type": "UHC",
    ...
  },
  ...
}
```

### Error Responses
- 401/403 Unauthorized:
```JSON
{ "error": "Authentication failed for user 'username'" }
```
- 500 Server Error:
```JSON
{ "error": "Internal server error" }
```
- Malformed Data:
```JSON
{ "error": "Malformed data for {resource}" }
```
Note:
All endpoints return a dictionary mapping resource IDs to their details. If no data is found, an empty dictionary is returned. For more details, see the docstrings in pydeepskylog/deepskylog_interface.py.