import pandas as pd
import numpy as np
import seaborn as sns

def data_quality_recommendations(df):
    recommendations = []

    try:
        # Data Quality Assessment
        recommendations.append("Data Quality Assessment:")

        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            recommendations.append("1. Handle missing data.")
            recommendations.append("   - Missing data by column:")
            recommendations.append(missing_data[missing_data > 0].to_string())

        # Check for data types
        recommendations.append("2. Check data types:")
        recommendations.append(df.dtypes.to_string())

        # Descriptive statistics
        recommendations.append("3. Descriptive statistics:")
        recommendations.append(df.describe().to_string())

        # Check for outliers (using z-scores, for example)
        outlier_threshold = 3  # You can adjust this threshold
        numeric_cols = df.select_dtypes(include=[np.number])
        z_scores = np.abs((numeric_cols - numeric_cols.mean()) / numeric_cols.std())
        outliers = z_scores > outlier_threshold
        if outliers.any().any():
            recommendations.append("4. Check for outliers:")
            recommendations.append("   - Columns with outliers:")
            recommendations.append(outliers.any()[outliers.any() == True].to_string())

        # Check for zero variance columns (constant columns)
        zero_variance_cols = df.columns[df.nunique() == 1]
        if len(zero_variance_cols) > 0:
            recommendations.append("5. Remove zero variance columns:")
            recommendations.append("   - Zero variance columns: " + ', '.join(zero_variance_cols))


        # Correlation Analysis
        recommendations.append("\nCorrelation Analysis:")

        # Compute the correlation matrix
        correlation_matrix = df.corr()

        # Visualize correlation matrix (optional)
        
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

        # Check for highly correlated features
        high_corr_threshold = 0.7
        high_corr_features = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                if abs(correlation_matrix.iloc[i, j]) > high_corr_threshold:
                    high_corr_features.append((correlation_matrix.index[i], correlation_matrix.columns[j]))

        if high_corr_features:
            recommendations.append("1. Highly correlated features found:")
            for feature_pair in high_corr_features:
                recommendations.append(f"   - {feature_pair[0]} and {feature_pair[1]}")

        # Duplicate Columns
        duplicate_columns = df.columns[df.columns.duplicated()]
        if len(duplicate_columns) > 0:
            recommendations.append("\nDuplicate Columns:")
            recommendations.append(f"1. Found {len(duplicate_columns)} duplicate columns.")
            recommendations.append("   - Duplicate columns: " + ', '.join(duplicate_columns))

    except Exception as e:
        recommendations.append(f"An error occurred: {str(e)}")

    return recommendations

# Example usage:
# df = pd.read_csv("your_data.csv")

# Error handling:
# try:
#     recommendations = data_quality_recommendations(df)
#     for recommendation in recommendations:
#         print(recommendation)
# except Exception as e:
#     print(f"An error occurred: {str(e)}")
