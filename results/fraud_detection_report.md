# Fraud Detection Pipeline Report

**Generated on:** 2025-08-03 14:28:34

## Executive Summary

This report presents the results of a comprehensive fraud detection analysis on cryptocurrency wallet data. The best performing model was **Logistic Regression** with an F1-score of **1.0000**.

## Dataset Overview

- **Original Dataset Size:** 9,500 rows × 53 columns
- **Processed Dataset Size:** 9,500 rows × 50 features
- **Class Distribution:**
  - Legitimate Wallets: 8,072
  - Fraudulent Wallets: 1,428

## Model Performance Comparison

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| Logistic Regression | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Random Forest | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| XGBoost | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| SVM | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| LightGBM | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Neural Network | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

## Best Model: Logistic Regression

- **Accuracy:** 1.0000
- **Precision:** 1.0000
- **Recall:** 1.0000
- **F1-Score:** 1.0000
- **ROC-AUC:** 1.0000

## Top Predictive Features

### Permutation

| Rank | Feature | Importance Score |
|------|---------|------------------|
| 1 | tx_amount_01 | 0.0000 |
| 2 | tx_amount_02 | 0.0000 |
| 3 | tx_amount_03 | 0.0000 |
| 4 | tx_amount_04 | 0.0000 |
| 5 | tx_amount_05 | 0.0000 |
| 6 | tx_amount_06 | 0.0000 |
| 7 | tx_amount_07 | 0.0000 |
| 8 | tx_amount_08 | 0.0000 |
| 9 | tx_amount_09 | 0.0000 |
| 10 | tx_amount_10 | 0.0000 |

### Shap

| Rank | Feature | Importance Score |
|------|---------|------------------|
| 1 | behavioral_01 | 0.7321 |
| 2 | behavioral_05 | 0.6284 |
| 3 | behavioral_03 | 0.5970 |
| 4 | behavioral_07 | 0.5801 |
| 5 | behavioral_02 | 0.5750 |
| 6 | behavioral_04 | 0.5495 |
| 7 | behavioral_10 | 0.5385 |
| 8 | behavioral_08 | 0.5185 |
| 9 | behavioral_06 | 0.5134 |
| 10 | behavioral_09 | 0.4814 |

## Files Generated

- `processed_dataset.csv` - Cleaned and preprocessed dataset
- `feature_scaler.joblib` - Fitted feature scaler
- `best_model_*.joblib` - Best performing model
- `model_comparison.csv` - Cross-validation results for all models
- `summary_statistics.csv` - Descriptive statistics by class
- `feature_importance_*.csv` - Feature importance from different methods
- Various plots in the `plots/` directory

## Research Objectives Addressed

1. **Feature Identification:** The analysis identified the most predictive features for fraud detection using multiple importance methods (model-specific, permutation importance, and SHAP values).

2. **Temporal Dynamics:** The model incorporates temporal and behavioral features that capture wallet behavior patterns over time, enabling early fraud detection.

