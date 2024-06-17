# Price Analysis Project

This project contains a price analysis using various machine learning techniques.

Source data: https://www.kaggle.com/datasets/joebeachcapital/house-prices-2001-2020/data

## Project Structure

- `data/`: Directory containing input data and output results.
  - `input/`: There should be CSV file but it's to large. Contains *.pkl file with processed input data.
  - `output/`: Contains output results such as training results and saved models.
- `notebooks/`: Directory containing Jupyter Notebooks.
  - `analysis.ipynb`: Jupyter Notebook with the price analysis.
- `Dockerfile`: Dockerfile for building the project Docker image.
- `requirements.txt`: List of Python dependencies.
- `.dockerignore`: Files and directories to ignore in the Docker image.
- `README.md`: Project description and instructions.

## Analysis Notebook Details

The `analysis.ipynb` notebook provides a comprehensive analysis of the house price data. Here's a brief overview of the content covered in the notebook:

- **Discovering the Dataset**: Exploring and understanding of data structure and content.
- **Data Cleaning and Wrangling**: Detailed instructions on how the data was prepared (duplicates, outliers, na values and transformations).
- **Feature Engineering**: Last step in data preparation, preparation data for suitable format for ML.
- **Model Training and Evaluation**: Training different models, improving them by slecting better parameters. Used R2 score and MSE for evaluation.
- **Model Comaprison**: Insights and conclusions drawn from the analysis, highlighting the strengths and weaknesses of each model.

## Recommendations

Based on the analysis, **LightGBM** emerges as the most effective model for this dataset, consistently outperforming other models in terms of MSE and R2 score. The conclusion also suggests that Neural Networks with SGD optimizer can provide results close to LightGBM models, but require more complex optimization and training.

## Prerequisites

- Docker installed on your machine.
- (Sugested) Windows WSL or UBUNTU to enable GPU for ML training

