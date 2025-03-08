# Trading Pipeline

This repository contains a structured implementation of an algorithmic trading pipeline using Python and C++, utilizing Gemini's BTC trading data via REST API. The project covers data ingestion, feature extraction, model training, inference, and performance analysis, designed for practical algorithmic trading without execution.

## Project Overview

The pipeline consists of the following stages:

### 1. Data Ingestion

- Python implementation of data ingestion using Gemini's REST API.
- GitHub Actions for automated Python unit testing (pytest), linting (Ruff, Mypy), and C++ linting and formatting (Clang-Tidy, ClangFormat).
- Unit tests and CI integration for robust verification.

### 2. Feature Computation

- Feature engineering implemented in C++ using a header-only architecture.
- Features computed per trade tick: price, volume, and trade side (buy/sell).
- Integration with Python via Pybind11 (`intern` module).

### 3. Model Training and Inference

- Online training implemented using scikit-learn's Lasso Regression.
- Buffer management logic for handling datasets (maintaining 10 recent X-Y pairs).
- Real-time predictions after training on accumulated data.
- Comprehensive unit testing for buffer management and model inference processes.

### 4. Analysis

- Evaluate prediction accuracy using correlation between predicted values and actual target data.
- Automated scripts to output predictions and targets to files for subsequent analysis.
- Python scripts to perform correlation analysis and performance evaluation.

### 5. Optimization

- C++ port of data ingestion logic using CPR.
- Pybind11 integration for Python interoperability, enabling Python scripts to leverage efficient C++ implementations.

## Environment Requirements

- GNU Make
- CMake
- Ninja
- Conan

## Getting Started

Clone the repository:

```bash
git clone https://github.com/MaxBreslin/trading-pipeline.git
cd trading-pipeline
```

Set up your environment following the provided instructions and run:

```bash
make test
```

Ensure all dependencies are correctly installed to avoid build issues.

## Testing and Validation

- Python unit tests run via pytest.
- Integration tests automated through GitHub Actions.

