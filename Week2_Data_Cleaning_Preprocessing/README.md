# Week 2 - Data Cleaning & Preprocessing

## Overview

This project implements the data cleaning and preprocessing pipeline for the AG News Classification Dataset. The goal is to clean the text data, handle common edge cases, perform basic NLP preprocessing using spaCy, and generate a cleaned dataset ready for text embedding.

---

## Dataset

- **Dataset:** AG News Classification Dataset
- **Input File:** `dataset/train.csv`
- **Output File:** `dataset/cleaned_train.csv`

---

## Project Structure

```
Week2_Data_Cleaning_Preprocessing/
│
├── dataset/
│   ├── train.csv
│   ├── test.csv
│   └── cleaned_train.csv
│
├── cleaning.py
├── preprocessing.py
├── test_cleaning.py
└── README.md
```

---

## Features Implemented

### Text Cleaning

The following preprocessing steps are applied:

- Remove HTML tags
- Remove special characters
- Normalize whitespace
- Handle empty text
- Handle `None` values
- Truncate extremely long text to 100,000 characters

---

### Edge Cases Handled

The cleaning pipeline correctly handles:

- Empty strings
- `None` values
- Extremely long text
- Multiple spaces and newline characters

---

### spaCy NLP Processing

Basic NLP preprocessing is performed on the first 100 cleaned records using **spaCy**.

The following information is generated:

- Tokenization
- Lemmatization

---

### Output

The preprocessing script:

- Combines the **Title** and **Description** columns
- Cleans the combined text
- Removes rows with empty cleaned text
- Saves the cleaned dataset as:

```
dataset/cleaned_train.csv
```

A cleaning report is also displayed, including:

- Original number of rows
- Remaining rows
- Rows removed
- Percentage of data removed

---

## Unit Testing

Unit tests are implemented using Python's `unittest` module.

The following functions are tested:

- `remove_html()`
- `remove_special_chars()`
- `normalize_whitespace()`
- `clean_text()` with empty text
- `clean_text()` with `None`
- `clean_text()` with extremely long text

Run the tests using:

```bash
python test_cleaning.py
```

---

## Requirements

Install the required packages:

```bash
pip install pandas spacy
python -m spacy download en_core_web_sm
```

---

## Run the Preprocessing Pipeline

Execute:

```bash
python preprocessing.py
```

---

## Example Cleaning Report

```
Cleaning Report

Original rows: 120000
Remaining rows: 120000
Rows removed: 0
Percentage removed: 0.00%
```

If rows become empty after cleaning, they are automatically removed and included in the report.

---

## Technologies Used

- Python
- Pandas
- spaCy
- Regular Expressions (re)
- unittest

---

## Author

**Mehroz Shahid**