import pandas as pd
from datetime import datetime
from statistics import mean
from dateutil.relativedelta import relativedelta
import numpy as np

def calculate_numeric_column_attributes(dataframe, column_name):
    # Select the specified column
    column_df = dataframe[column_name]
    
     # Calculate NaN values count
    nan_count = column_df.isna().sum()
    
    # Calculate distinct values and distinct percentage
    distinct_count = column_df.nunique()
    distinct_percentage = (distinct_count / len(column_df)) * 100
    
    # Calculate missing values and missing percentage
    missing_count = column_df.isnull().sum()
    missing_percentage = (missing_count / len(column_df)) * 100
    
    # Calculate infinite values and infinite percentage
    infinite_count = np.isinf(column_df).sum()
    infinite_percentage = (infinite_count / len(column_df)) * 100
    
    # Calculate mean, median, mode, min, and max
    mean = column_df.mean()
    median = column_df.median()
    try:
        mode = column_df.mode().iloc[0]
    except IndexError:
        mode = 'ERROR'
#         print('Specified column index out of bounds')
    minimum = column_df.min()
    maximum = column_df.max()
    
    # Calculate zeros and zeros percentage
    zero_count = (column_df == 0).sum()
    zero_percentage = (zero_count / len(column_df)) * 100
    
    # Calculate memory usage
    memory_usage = column_df.memory_usage(deep=True)/(1024 * 1024)
    
    # Calculate quantile values (25th, 50th, and 75th percentiles)
    quantiles = column_df.quantile([0.25, 0.5, 0.75])
    q_25 = quantiles[0.25]
    q_50 = quantiles[0.5]
    q_75 = quantiles[0.75]
    # IQR
    iqr = q_75 - q_25
    # Calculate range
    column_range = maximum - minimum
    
    # Calculate kurtosis and skewness
    kurtosis = column_df.kurtosis()
    skewness = column_df.skew()
    
    # Calculate variance and standard deviation
    variance = column_df.var()
    std_deviation = column_df.std()
    
    # Create a dictionary to store the results
    attributes = {
        "column_name":column_name,
        "total count":column_df.shape[0],
        "Distinct": distinct_count,
        "nan values count":nan_count,
        "Distinct Percentage": round(distinct_percentage,2),
        "Missing": missing_count,
        "Missing Percentage": round(missing_percentage,2),
#         "Infinite": infinite_count,
#         "Infinite Percentage": round(infinite_percentage,2),
        "Mean": mean,
        "Median": median,
        "Mode": mode,
        "Minimum": minimum,
        "Maximum": maximum,
        "Zeros": zero_count,
        "Zeros Percentage": zero_percentage,
        "Memory Usage(MB)": round(memory_usage,2),
        "25th Percentile": q_25,
        "50th Percentile": q_50,
        "75th Percentile": q_75,
        "IQR":iqr,
        "Range": column_range,
        "Kurtosis": kurtosis,
        "Skewness": skewness,
        "Variance": variance,
        "Standard Deviation": std_deviation,
    }
    
    return attributes

def calculate_categorical_column_attributes(dataframe, column_name):
    # Select the specified column
    column_df = dataframe[column_name]
    
    # Calculate distinct values and distinct percentage
    distinct_count = column_df.nunique()
    distinct_percentage = (distinct_count / len(column_df)) * 100
    
    # Calculate missing values and missing percentage
    missing_count = column_df.isnull().sum()
    missing_percentage = (missing_count / len(column_df)) * 100
    
    try:
        # Calculate mode (most frequent value)
        mode_value = column_df.mode().iloc[0]
    except IndexError:
        mode_value = 'ERROR'
#         print('Specified column index out of bounds')
    
    # Count the occurrence of each value in the column
    value_counts = dict(column_df.value_counts()[:5])
    
    # Calculate memory usage
    memory_usage = column_df.memory_usage(deep=True)/(1024 * 1024)
    
    # Create a dictionary to store the results
    attributes = {
        "column_name":column_name,
        "total count":column_df.shape[0],
        "Distinct": distinct_count,
        "Distinct Percentage": round(distinct_percentage,2),
        "Missing": missing_count,
        "Missing Percentage": round(missing_percentage,2),
        "Mode": mode_value,
        "Values Count": value_counts,
        "Memory Usage(MB)": round(memory_usage,2),
    }
    
    return attributes

def calculate_date_description_statistics(dataframe, column_name):

    date_list = dataframe[column_name]

    if not date_list.empty:
        # Convert date strings to datetime objects
        date_objects = pd.to_datetime(date_list, errors='coerce')

        # Remove rows with invalid dates (NaT)
        date_objects = date_objects.dropna()

        if not date_objects.empty:
            # Calculate minimum and maximum dates
            min_date = date_objects.min().strftime('%Y-%m-%d')
            max_date = date_objects.max().strftime('%Y-%m-%d')

            # Calculate the average date
            avg_date = mean(date_objects).strftime('%Y-%m-%d')

            # Calculate the date range
            date_objects.sort_values(inplace=True)  # Sort the dates in ascending order
            date_range = (
                date_objects.iloc[0].strftime('%Y-%m-%d'),
                date_objects.iloc[-1].strftime('%Y-%m-%d')
            )

            # Calculate the total number of years, months, and days in the date range
            start_date, end_date = date_objects.iloc[0], date_objects.iloc[-1]
            delta = relativedelta(end_date, start_date)
            years, months, days = delta.years, delta.months, delta.days

            # Create a dictionary to store the statistics
            statistics = {
                'Min Date': min_date,
                'Max Date': max_date,
                'Average Date': avg_date,
                'Date Range': date_range,
                'Total Years': years,
                'Total Months': months,
                'Total Days': days
            }

            return statistics
        else:
            return "No valid dates found in the column."
    else:
        return "The column is empty."

def dup_data_description(df,table_name):
    
    desc_results = {}
    var_results = {}
    
    df_shape = df.shape
    # print("types",df_shape)
    date_columns = []
    for column in df.columns:
        if df[column].dtype in ['datetime', 'datetime64','datetime64[ns]']:
            date_columns.append(column)
    desc_results['no_of_observations'] = df_shape[0]
    desc_results['no_of_variables'] = df_shape[1]

    # Get the data types of columns
    column_data_types = df.dtypes

    # Find unique data types
    unique_data_types = column_data_types.unique()

    # Create a dictionary to store column names by data type
    column_names_by_dtype = {dtype: [] for dtype in unique_data_types}
    # Iterate through columns and categorize them by data type
    for column_name, dtype in column_data_types.items():
        column_names_by_dtype[dtype].append(column_name)

    # Calculate missing values count per column
    missing_values_count = df.isnull().sum()

    # Calculate missing values percentage per column
    total_values = df.shape[0]
    missing_values_percentage = (missing_values_count / total_values) * 100
    
#     desc_results['Missing_values_count'] = missing_values_percentage
    
    # Calculate the number of duplicate rows
    duplicate_rows = df.duplicated(keep='first')  # Keep the first occurrence as not duplicate
    num_duplicates = duplicate_rows.sum()
    
    desc_results['duplicate_rows'] = num_duplicates
    
    # Calculate the number of duplicate rows
    num_duplicate_rows = df.duplicated().sum()

    # Calculate the total number of rows
    total_rows = len(df)

    # Calculate the percentage of duplicate rows
    duplicate_percentage = (num_duplicate_rows / total_rows) * 100
    
    desc_results['duplicate_percentage'] = duplicate_percentage
    
    # Calculate memory usage for each column
    memory_usage_per_column = df.memory_usage(deep=True)

    # Calculate the total memory usage for the entire DataFrame in bytes
    total_memory_usage = memory_usage_per_column.sum()

    # Convert the total memory usage to a more human-readable format (e.g., megabytes)
    total_memory_usage_MB = round(total_memory_usage / (1024 * 1024),2)  # Convert bytes
    
    desc_results['memory_usuage(MB)'] = total_memory_usage_MB
    #########################
    # numeric
    ########################
    numeric_columns = []
    
    for column in df.columns:
        if df[column].dtype in ['int64', 'float64']:
            numeric_columns.append(column)
            
    num_res = []
    for n_col in numeric_columns:
        num_res.append(calculate_numeric_column_attributes(df,n_col))
        
    var_results['numerical_results'] = num_res
    ######################
    # categorical
    #####################
    categoric_columns = []
    
    for column in df.columns:
        if df[column].dtype in ['object']:
            categoric_columns.append(column)
            
    cat_res = []
    for c_col in categoric_columns:
        cat_res.append(calculate_categorical_column_attributes(df,c_col))

    var_results['categorical_results'] = cat_res
    
    ####################
    # date
    ###################
    date_res = []
    for d_col in date_columns:
        date_res.append(calculate_date_description_statistics(df,d_col))
        
    var_results['date_results'] = date_res 
    ######################
    # boolean
    ####################
    # Filter boolean columns
    bool_columns = df.select_dtypes(include=['bool'])
#     boolean_res = []
#     for bl_col in bool_columns:
#         date_res.append(calculate_date_description_statistics(df,bl_col))
        
#     var_results['boolean_results'] = boolean_res 
    
    
    return desc_results,var_results