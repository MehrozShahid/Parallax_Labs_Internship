# Data Quality Report

## Week 1: Environment & Data Acquisition

## Dataset Information

- **Dataset Name:** AG News Classification Dataset
- **File Analyzed:** `train.csv`
- **Source:** Kaggle


## Dataset Summary

| Metric | Value |
|--------|------:|
| Total Records | 120,000 |
| Total Columns | 3 |

### Columns

- Class Index
- Title
- Description


## Missing Values Analysis

The dataset was checked for missing values using the `isnull().sum()` function in Pandas.

| Column | Missing Values |
|--------|---------------:|
| Class Index | 0 |
| Title | 0 |
| Description | 0 |

### Finding

After checking each column, no missing values were found. Since every record contains complete information, no additional cleaning was required before moving to the next validation step.


## Duplicate Rows Analysis

The dataset was checked for duplicate rows using the `duplicated().sum()` function.

**Duplicate Rows:** **0**

### Finding

No duplicate records were detected. This indicates that each row in the dataset is unique and there was no need to remove repeated entries.

## Data Type Validation

The data types of all columns were verified using the `dtypes` attribute.

| Column | Data Type |
|--------|----------|
| Class Index | int64 |
| Title | object |
| Description | object |

### Finding

The data types match the contents of each column. The class labels are stored as integers, while the title and description are stored as text, which is appropriate for a text classification dataset.


## Encoding Validation

The dataset was successfully loaded using **UTF-8** encoding.

### Finding

The file loaded successfully without any encoding errors or unreadable characters, indicating that the text data can be processed correctly.


## Column Structure Validation

The following columns were expected in the dataset:

- Class Index
- Title
- Description

### Finding

The dataset contains all three expected columns, and their names match the required structure. No changes to the column names were necessary.


## Validation Summary

The dataset successfully passed all validation checks.

- ✔ Dataset contains more than **5,000** records.
- ✔ No missing values were found.
- ✔ No duplicate rows were found.
- ✔ UTF-8 encoding was verified successfully.
- ✔ All expected columns are present.
- ✔ Data types are appropriate.


## Conclusion

The dataset meets all the required validation criteria. It contains the expected number of records, has no missing or duplicate data, uses the correct encoding, and follows the expected column structure. Based on these checks, the dataset is ready for next stages.