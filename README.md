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
1. Install tools: `pip install zenodo-cli`
2. Prepare data:
    ```bash
    # Compress large directories
    tar -czf calculations.tar.gz calculations/
    tar -czf checkpoints.tar.gz checkpoints/
    ```
3. Upload:
    ```bash
    export ZENODO_TOKEN="your-token"
    zenodo-cli create --title "Project Data" --type dataset
    zenodo-cli upload calculations.tar.gz checkpoints.tar.gz
    zenodo-cli publish
    ```

### Downloading Data
```bash
pip install zenodo-cli
zenodo-cli download [DOI]
```

## Dependencies
[List key software dependencies]

## Usage
[Basic usage instructions]
