# CSV Analytics Program

This program provides a comprehensive CSV analytics pipeline using LangGraph and AI-powered code generation.

## Features

The CSV analytics program can:

1. **Data Loading & Inspection**
   - Load any CSV file or create sample data
   - Display dataset information (shape, columns, data types)
   - Show sample rows and summary statistics

2. **Data Quality Analysis**
   - Check for missing values and duplicates
   - Identify data type issues
   - Handle missing data appropriately

3. **Descriptive Analytics**
   - Generate summary statistics for numerical columns
   - Frequency analysis for categorical columns
   - Correlation analysis between variables

4. **Data Visualizations**
   - Distribution plots (histograms)
   - Box plots for outlier detection
   - Correlation heatmaps
   - Scatter plots for relationships
   - Bar charts for categorical data
   - Time series plots (if date columns exist)

5. **Advanced Analytics**
   - Pattern identification
   - Outlier detection using statistical methods
   - Trend analysis
   - Basic statistical tests

6. **Export Results**
   - Cleaned data saved to new CSV files
   - Summary reports of key findings
   - All visualizations saved as PNG files
   - Text summaries of insights

## Usage

### Option 1: Use Sample Data
The program comes with sample sales data. Simply run:
```bash
python python_developer.py
```

### Option 2: Use Your Own CSV File
1. Place your CSV file in the `langgraph_demo` folder
2. Modify the script to use your file:
```python
# Uncomment and modify this line in the script:
result = run_analytics_with_custom_file("/path/to/your/file.csv")
```
3. Run the program

### Option 3: Create Synthetic Data
The AI agent can create realistic sample data for demonstration purposes.

## Output Files

After running the program, check the `langgraph_demo` folder for:
- **Visualizations**: Various PNG files with charts and graphs
- **Cleaned Data**: Processed CSV files
- **Reports**: Text files with analysis summaries
- **Statistics**: Numerical summaries and insights

## Sample Data

The included `sample_sales_data.csv` contains:
- Sales transactions with dates
- Product information and categories
- Customer demographics
- Sales amounts and quantities
- Regional data
- Customer satisfaction scores
- Some missing values for testing data cleaning

## Requirements

- Python 3.8+
- LangGraph
- LangChain
- pandas
- matplotlib
- seaborn
- numpy
- Other dependencies as specified in the main project

## Customization

You can easily modify the analytics pipeline by:
1. Editing the `analytics_prompt` in the `run_csv_analytics()` function
2. Adding new visualization types
3. Including additional statistical analyses
4. Modifying the data cleaning procedures

The AI agent will generate appropriate Python code based on your requirements and execute it automatically.

