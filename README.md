# Traffic Flow Prediction Using Big Data & Deep Learning

## Project Overview
This project focuses on predicting traffic flow using deep learning techniques. It processes raw traffic data, trains a model, and serves predictions via a simple REST API.

## Directory Structure
- `api/`: Contains the Flask web application (`app.py`) to serve model predictions.
- `data/`: Used for storing datasets. Place your raw files in `data/raw/`.
- `notebooks/`: Useful for Jupyter notebooks containing exploratory data analysis (EDA) and early experiments.
- `src/`: Houses the core source code for the project:
  - `data_preprocessing.py`: For data cleaning, handling missing values, and feature engineering.
  - `model.py`: For defining the neural network architectures.
  - `train.py`: For setting up the training loop and recording metrics.
  - `predict.py`: For generating predictions using the fully trained model.

## Installation
1. It's recommended to create a virtual environment first.
2. Ensure you have Python installed.
3. Install the project dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Running the API
Start the Flask development server by running:
```bash
python api/app.py
```
By default, this will expose an API running on `http://127.0.0.1:5000`. 
Check `http://127.0.0.1:5000/` in your browser for a welcome message!

### Making Predictions
Make a `POST` request with JSON data to `http://127.0.0.1:5000/predict` to get traffic flow predictions from the model.
