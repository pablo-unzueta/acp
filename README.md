# Computational Chemistry Project

## Overview
[Brief project description]

## Directory Structure
- `input/`: Input file templates and system-specific files
- `scripts/`: Analysis, submission, and utility scripts
- `notebooks/`: Jupyter notebooks for analysis
- `docs/`: Documentation and methods
- `tests/`: Validation calculations
- `results/`: Processed data and figures

## Setup
[Setup instructions]

## Data
Raw calculation data is stored on Zenodo:
- Input structures: [DOI]
- Calculation outputs: [DOI]
- Checkpoint files: [DOI]

### Data Organization on Zenodo
```
data/
├── input/                # Input structures and templates
├── calculations/         # Raw outputs organized by system
├── checkpoints/         # Large checkpoint files
└── processed/           # Analysis-ready data
```

### Uploading New Data
1. Install requirements: `pip install requests tqdm`
2. Set up tokens:
    ```bash
    # For testing (sandbox)
    export ZENODO_SANDBOX_TOKEN="your-sandbox-token"
    
    # For production
    export ZENODO_TOKEN="your-production-token"
    ```
3. Prepare data:
    ```bash
    # Compress large directories
    tar -czf calculations.tar.gz calculations/
    tar -czf checkpoints.tar.gz checkpoints/
    ```
4. Test upload first:
    ```bash
    ./scripts/utils/zenodo_upload.py \
        --sandbox \
        --title "Project Data" \
        --description "$(cat README.txt)" \
        --creators "LastName, FirstName" \
        calculations.tar.gz checkpoints.tar.gz
    ```
5. When ready, upload to production:
    ```bash
    ./scripts/utils/zenodo_upload.py \
        --title "Project Data" \
        --description "$(cat README.txt)" \
        --creators "LastName, FirstName" \
        --keywords "computational chemistry,DFT,your-keywords" \
        --communities "computational-chemistry" \
        --related-dois "10.xxxx/xxxxx" \
        calculations.tar.gz checkpoints.tar.gz
    ```

### Downloading Data
# Use Zenodo's direct download links or API
wget https://zenodo.org/record/[record]/files/[filename]

## Dependencies
[List key software dependencies]

## Usage
[Basic usage instructions]
