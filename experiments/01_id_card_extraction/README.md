# Experiment 1: ID Card Information Extraction

## Overview
This experiment explores using NVIDIA's VLM API to extract structured information from Spanish ID cards.

## Key Findings
- VLM API can successfully extract structured information when given precise prompts
- Prompt engineering is crucial for accurate extraction
- Using example structures without actual values works better than providing real examples
- Token usage can be optimized by limiting max_tokens to 256

## Prompt Evolution
1. Initial basic prompt
2. Added structured JSON format
3. Removed document type identification
4. Used placeholder values instead of real examples

## Implementation Details
- Uses NVIDIA's VLM API (Fuyu-8B model)
- Extracts the following fields:
  - Full Name
  - ID Number
  - Date of Birth
  - Nationality
  - Expiry Date
- Returns data in structured JSON format

## Files
- `test_extraction.py`: Main script for ID card information extraction
- `sample_data/`: Contains test images

## Usage
```python
python test_extraction.py
```

## Future Improvements
1. Add error handling for different ID card formats
2. Implement batch processing for multiple images
3. Add validation for extracted data
4. Create a simple web interface for uploads
