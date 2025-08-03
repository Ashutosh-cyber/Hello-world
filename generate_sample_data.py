#!/usr/bin/env python3
"""
Sample Data Generator for Elliptic++ Dataset
============================================

This script generates synthetic data that mimics the structure of the Elliptic++ dataset
for testing the fraud detection pipeline when the actual dataset is not available.

The generated data includes:
- Behavioral features (transaction patterns)
- Transactional features (amounts, frequencies)
- Temporal features (time-based patterns)
- Graph-based features (network connectivity)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_elliptic_sample_data(n_samples=10000, n_features=50, fraud_ratio=0.1):
    """
    Generate synthetic data mimicking the Elliptic++ dataset structure
    
    Parameters:
    -----------
    n_samples : int
        Number of wallet samples to generate
    n_features : int
        Number of features to generate
    fraud_ratio : float
        Proportion of fraudulent wallets (class=1)
    
    Returns:
    --------
    pd.DataFrame : Generated dataset
    """
    
    print(f"Generating {n_samples:,} samples with {n_features} features...")
    print(f"Fraud ratio: {fraud_ratio:.1%}")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Generate wallet addresses
    addresses = [f"wallet_{i:06d}" for i in range(n_samples)]
    
    # Generate time steps (49 time periods as in original Elliptic dataset)
    time_steps = np.random.randint(1, 50, n_samples)
    
    # Generate class labels
    n_fraud = int(n_samples * fraud_ratio)
    n_legit = n_samples - n_fraud
    classes = [1] * n_fraud + [2] * n_legit  # 1=fraud, 2=legitimate
    random.shuffle(classes)
    
    # Add some unknown labels (class=3) to test filtering
    n_unknown = int(n_samples * 0.05)  # 5% unknown
    unknown_indices = random.sample(range(n_samples), n_unknown)
    for idx in unknown_indices:
        classes[idx] = 3
    
    # Generate features based on different categories
    data = {
        'address': addresses,
        'Time step': time_steps,
        'class': classes
    }
    
    # Generate different types of features
    feature_categories = {
        'tx_amount': 10,      # Transaction amount features
        'tx_freq': 8,         # Transaction frequency features  
        'neighbor': 12,       # Neighbor/graph features
        'temporal': 10,       # Temporal pattern features
        'behavioral': 10      # Behavioral features
    }
    
    feature_idx = 0
    
    for category, count in feature_categories.items():
        for i in range(count):
            feature_name = f"{category}_{i+1:02d}"
            
            if category == 'tx_amount':
                # Transaction amounts - fraudulent wallets tend to have different patterns
                if classes[0] == 1:  # If first sample is fraud, create fraud pattern
                    fraud_pattern = np.random.lognormal(mean=8, sigma=2, size=n_fraud)
                    legit_pattern = np.random.lognormal(mean=6, sigma=1.5, size=n_legit)
                else:
                    fraud_pattern = np.random.lognormal(mean=8, sigma=2, size=n_fraud)
                    legit_pattern = np.random.lognormal(mean=6, sigma=1.5, size=n_legit)
                
                # Combine patterns based on actual class distribution
                feature_values = []
                fraud_idx = 0
                legit_idx = 0
                for cls in classes:
                    if cls == 1:  # Fraud
                        if fraud_idx < len(fraud_pattern):
                            feature_values.append(fraud_pattern[fraud_idx])
                            fraud_idx += 1
                        else:
                            feature_values.append(np.random.lognormal(8, 2))
                    elif cls == 2:  # Legitimate
                        if legit_idx < len(legit_pattern):
                            feature_values.append(legit_pattern[legit_idx])
                            legit_idx += 1
                        else:
                            feature_values.append(np.random.lognormal(6, 1.5))
                    else:  # Unknown
                        feature_values.append(np.random.lognormal(7, 1.8))
                        
            elif category == 'tx_freq':
                # Transaction frequencies - fraud patterns
                feature_values = []
                for cls in classes:
                    if cls == 1:  # Fraud - higher frequency
                        feature_values.append(np.random.poisson(15))
                    elif cls == 2:  # Legitimate - normal frequency
                        feature_values.append(np.random.poisson(8))
                    else:  # Unknown
                        feature_values.append(np.random.poisson(10))
                        
            elif category == 'neighbor':
                # Graph/network features - connectivity patterns
                feature_values = []
                for cls in classes:
                    if cls == 1:  # Fraud - different network patterns
                        feature_values.append(np.random.exponential(2))
                    elif cls == 2:  # Legitimate
                        feature_values.append(np.random.exponential(1))
                    else:  # Unknown
                        feature_values.append(np.random.exponential(1.5))
                        
            elif category == 'temporal':
                # Temporal features - time-based patterns
                feature_values = []
                for j, cls in enumerate(classes):
                    time_factor = time_steps[j] / 49.0  # Normalize by max time step
                    if cls == 1:  # Fraud - evolving patterns
                        base_value = np.random.normal(0, 1)
                        feature_values.append(base_value * (1 + time_factor))
                    elif cls == 2:  # Legitimate - stable patterns
                        feature_values.append(np.random.normal(0, 0.8))
                    else:  # Unknown
                        feature_values.append(np.random.normal(0, 0.9))
                        
            else:  # behavioral
                # Behavioral features - general patterns
                feature_values = []
                for cls in classes:
                    if cls == 1:  # Fraud
                        feature_values.append(np.random.beta(2, 5))
                    elif cls == 2:  # Legitimate
                        feature_values.append(np.random.beta(5, 2))
                    else:  # Unknown
                        feature_values.append(np.random.beta(3, 3))
            
            data[feature_name] = feature_values
            feature_idx += 1
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add some missing values to test preprocessing
    missing_features = random.sample([col for col in df.columns if col not in ['address', 'Time step', 'class']], 5)
    for feature in missing_features:
        missing_indices = random.sample(range(n_samples), int(n_samples * 0.02))  # 2% missing
        df.loc[missing_indices, feature] = np.nan
    
    print(f"✓ Generated dataset shape: {df.shape}")
    print(f"✓ Class distribution:")
    print(df['class'].value_counts().sort_index())
    print(f"✓ Missing values in {len(missing_features)} features")
    
    return df

def main():
    """Generate and save sample data"""
    print("=" * 60)
    print("ELLIPTIC++ SAMPLE DATA GENERATOR")
    print("=" * 60)
    
    # Generate sample data
    df = generate_elliptic_sample_data(
        n_samples=10000,
        n_features=50,
        fraud_ratio=0.15
    )
    
    # Save to CSV
    output_file = 'wallets_features_classes_combined.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Sample data saved to: {output_file}")
    print(f"✓ File size: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # Display sample
    print(f"\nSample of generated data:")
    print(df.head())
    
    print(f"\nFeature summary:")
    print(f"- Total features: {len(df.columns) - 3}")  # Exclude address, Time step, class
    print(f"- Behavioral features: 10")
    print(f"- Transactional features: 18") 
    print(f"- Temporal features: 10")
    print(f"- Graph-based features: 12")

if __name__ == "__main__":
    main()