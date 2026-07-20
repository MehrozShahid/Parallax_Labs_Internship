# Week 1 – Environment & Data Acquisition

## Introduction

This project was completed for the first week of my internship. The main goal was to prepare a working Python environment for future tasks and make sure all the required libraries were installed correctly. I also downloaded a real-world dataset, checked its quality, and documented the results in a data quality report.

## Tasks Completed

During this assignment, I completed the following tasks:

- Installed all the required Python libraries.
- Verified that each library was working correctly.
- Downloaded the AG News Classification Dataset.
- Checked the dataset for missing values, duplicate records, encoding issues, and column structure.
- Prepared a data quality report based on the validation results.

## Environment

The following tools and libraries were installed and verified as part of this assignment:

- Python
- pandas
- spaCy
- NLTK
- sentence-transformers
- ChromaDB

## Dataset

**Dataset Name:** AG News Classification Dataset

The dataset contains news articles grouped into different categories. It was selected because it provides a large number of records, making it suitable for practicing data validation and preparing for future Natural Language Processing tasks.

## Project Files

Week1_Environment_Data_Acquisition/
│
├── README.md
├── verify_environment.py
├── validate_dataset.py
├── data_quality_report.md
└── dataset/
    ├── train.csv
    └── test.csv


## My Approach

### Environment Verification

After installing the required libraries, I created a Python script to verify that everything was working properly. The script imports each library and performs a simple test to confirm that the environment is ready for development.

### Dataset Validation

I created a Python script to validate the downloaded dataset before using it for future tasks. The script performs the following checks:

- Reads the dataset using UTF-8 encoding to ensure there are no encoding issues.
- Displays the total number of rows in the dataset.
- Displays the column names.
- Checks for missing values in each column.
- Checks for duplicate rows.
- Displays the data type of each column.
- Verifies that the expected columns (`Class Index`, `Title`, and `Description`) are present in the dataset.

These checks help confirm that the dataset is complete, properly structured, and ready for further preprocessing and analysis.


### Data Quality Report

After completing the validation, I summarized the results in a separate report. The report includes the dataset information, missing value analysis, duplicate record analysis, encoding validation, and an overall conclusion.

## How to Run

1. Make sure Python is installed.

2. Install the required libraries:

pip install pandas spacy nltk sentence-transformers chromadb

3. Run the environment verification script.

python verify_environment.py

4. Run the dataset validation script.

python validate_dataset.py

## Files Included

- README.md
- verify_environment.py
- validate_dataset.py
- data_quality_report.md
- dataset/
  - train.csv
  - test.csv

## Conclusion

This assignment helped me set up a complete development environment and become familiar with checking the quality of a dataset before using it. All required libraries were successfully verified, and the dataset passed the validation checks. The project is now ready for the next stage of the internship.
