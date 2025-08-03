# Fraud Detection Pipeline for Elliptic++ Dataset

A comprehensive machine learning pipeline for cryptocurrency wallet fraud detection using behavioral, transactional, temporal, and graph-based features.

## 🎯 Research Objectives

1. **Feature Identification**: Identify transaction-level and wallet-level features most indicative of fraud
2. **Temporal Dynamics**: Enable early fraud detection by modeling wallet behavior over time

## 🚀 Features

- **Comprehensive Data Pipeline**: Complete preprocessing, cleaning, and feature engineering
- **Multiple ML Models**: Comparison of 6 different algorithms (Logistic Regression, Random Forest, XGBoost, SVM, LightGBM, Neural Network)
- **Advanced Analytics**: EDA with statistical analysis and visualizations
- **Class Imbalance Handling**: SMOTE oversampling for balanced training
- **Hyperparameter Tuning**: GridSearchCV optimization for best models
- **Feature Importance**: Multiple methods (model-specific, permutation, SHAP)
- **Comprehensive Reporting**: Automated report generation with visualizations

## 📋 Pipeline Steps

1. **Data Loading & Preprocessing**
   - Load CSV dataset
   - Filter unknown labels (class=3)
   - Handle missing values
   - Feature scaling and normalization

2. **Exploratory Data Analysis**
   - Descriptive statistics by class
   - Feature distribution analysis
   - Correlation analysis and multicollinearity detection
   - Visualization of class separability

3. **Class Imbalance Handling**
   - SMOTE oversampling for balanced training

4. **Model Training & Comparison**
   - 5-fold cross-validation
   - Performance metrics: Accuracy, Precision, Recall, F1-Score, ROC-AUC

5. **Hyperparameter Optimization**
   - GridSearchCV for top 2 models
   - F1-score optimization

6. **Model Evaluation**
   - Test set evaluation
   - Confusion matrix and ROC curves
   - Classification reports

7. **Feature Importance Analysis**
   - Model-specific importance
   - Permutation importance
   - SHAP values with visualizations

8. **Results Export**
   - Processed datasets
   - Trained models
   - Performance metrics
   - Comprehensive reports

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fraud-detection-pipeline
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data** (if you don't have the actual dataset):
   ```bash
   python generate_sample_data.py
   ```

## 📊 Usage

### Quick Start

```bash
# Run the complete pipeline
python fraud_detection_pipeline.py
```

### Custom Configuration

```python
from fraud_detection_pipeline import FraudDetectionPipeline

# Initialize with custom data path
pipeline = FraudDetectionPipeline(data_path='your_dataset.csv')

# Run complete pipeline
pipeline.run_complete_pipeline()

# Or run individual steps
pipeline.load_data()
pipeline.preprocess_data()
pipeline.exploratory_data_analysis()
# ... continue with other steps
```

## 📁 Output Structure

```
results/
├── processed_dataset.csv           # Cleaned dataset
├── feature_scaler.joblib           # Fitted scaler
├── best_model_*.joblib             # Best performing model
├── model_comparison.csv            # Cross-validation results
├── summary_statistics.csv          # Descriptive statistics
├── feature_importance_*.csv        # Feature importance results
├── results_summary.json            # Comprehensive results
└── fraud_detection_report.md       # Detailed report

plots/
├── feature_distributions.png       # Class-wise feature distributions
├── correlation_heatmap.png         # Feature correlation matrix
├── best_model_evaluation_*.png     # Confusion matrix & ROC curve
├── shap_feature_importance.png     # SHAP summary plot
└── comprehensive_feature_importance.png  # Combined importance plot
```

## 🔧 Requirements

- Python 3.7+
- pandas >= 1.5.0
- scikit-learn >= 1.1.0
- xgboost >= 1.6.0
- lightgbm >= 3.3.0
- shap >= 0.41.0
- imbalanced-learn >= 0.9.0

See `requirements.txt` for complete list.

## 📈 Model Performance

The pipeline automatically compares multiple algorithms and selects the best performer based on F1-score:

- **Logistic Regression**: Fast, interpretable baseline
- **Random Forest**: Robust ensemble method
- **XGBoost**: Gradient boosting with high performance
- **SVM**: Support vector machines with RBF kernel
- **LightGBM**: Fast gradient boosting
- **Neural Network**: Multi-layer perceptron

## 🎨 Visualizations

The pipeline generates comprehensive visualizations:

- Class distribution pie charts
- Feature distribution comparisons (fraud vs. legitimate)
- Correlation heatmaps
- Confusion matrices
- ROC curves
- Feature importance plots
- SHAP summary plots

## 🔍 Feature Importance Analysis

Multiple methods for identifying the most predictive features:

1. **Model-specific importance**: Built-in feature importance from tree-based models
2. **Permutation importance**: Model-agnostic importance based on performance drop
3. **SHAP values**: Unified framework for model interpretability

## 📊 Sample Data Generator

If you don't have access to the actual Elliptic++ dataset, use the sample data generator:

```python
from generate_sample_data import generate_elliptic_sample_data

# Generate 10,000 samples with 50 features
df = generate_elliptic_sample_data(n_samples=10000, n_features=50, fraud_ratio=0.15)
```

The generator creates realistic synthetic data with:
- Behavioral patterns
- Transactional features
- Temporal dynamics
- Graph-based features
- Realistic class imbalance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 References

- Elliptic++ Dataset: [Original Paper/Source]
- SHAP: Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions.
- SMOTE: Chawla, N. V., et al. (2002). SMOTE: synthetic minority oversampling technique.

## 🐛 Issues & Support

If you encounter any issues or have questions:

1. Check the existing issues on GitHub
2. Create a new issue with detailed description
3. Include error messages and system information

---

**Note**: This pipeline is designed for research and educational purposes. For production use, additional validation and security measures should be implemented.
