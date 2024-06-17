# Price Analysis Project

This project contains a price analysis using various machine learning techniques.

## Project Structure

- `data/`: Directory containing input data and output results.
  - `input/`: Contains input CSV files.
  - `output/`: Contains output results such as training results and saved models.
- `notebooks/`: Directory containing Jupyter Notebooks.
  - `analysis.ipynb`: Jupyter Notebook with the price analysis.
- `Dockerfile`: Dockerfile for building the project Docker image.
- `requirements.txt`: List of Python dependencies.
- `.dockerignore`: Files and directories to ignore in the Docker image.
- `README.md`: Project description and instructions.

## Getting Started

### Prerequisites

- Docker installed on your machine.

### Building the Docker Image

```sh
docker build -t price-analysis-project .
