## Data Format
The system expects a CSV file with the following columns:
- temperature (float)
- humidity (float)
- rainfall (float)
- soil_pH (float)
- disease_present (int: 0 or 1)

## Model Performance
The model is evaluated using:
- Classification Report
- Accuracy Score

## Error Handling
- Validates input data format
- Handles missing files and values
- Includes comprehensive logging

## Requirements
See requirements.txt for detailed dependencies.

## License
MIT License