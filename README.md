# VLM Vision Experiments

This repository contains experiments and explorations with NVIDIA's Vision Language Model (VLM) API. Each experiment is documented in its own directory with detailed README files.

## Structure
- `experiments/`: Contains individual experiment directories
- `common/`: Shared utilities and helper functions
- `requirements.txt`: Project dependencies

## Experiments
1. [ID Card Information Extraction](experiments/01_id_card_extraction/README.md): Extract structured information from Spanish ID cards using VLM API

## Setup
1. Clone this repository
2. Create a `.env` file in the project root
3. Add your NVIDIA API key:
   ```
   NVIDIA_API_KEY=your_actual_api_key_here
   ```
4. Install dependencies: 
   ```bash
   pip install -r requirements.txt
   ```

## Security
- NEVER commit your API keys to version control
- Use environment variables to manage sensitive credentials

## Contributing
Each new experiment should:
1. Have its own directory under `experiments/`
2. Include a detailed README.md
3. Document findings and learnings
4. Include sample data (if not sensitive)

## License
MIT License - See [LICENSE](LICENSE) file for details
