# Chapter 2 - End-to-End Machine Learning Project

## Look at the Big Picture
1. Frame the Problem
2. Select a Performance Measure
    - RMSE v.s. MAE: MAE is better for heavy tail data, i.e. data with many outliers (house prices, personal incomes)
3. Check the assumptions

## Get the Data
1. Create a workspace
2. Download/Access the data
3. Preview data structure
    - `df.head()`, `df.tail()`, `df.sample()`
    - `df.info()`
    - `df.describe()`
4. Create a test set
    - `sklearn.model_selection.train_test_split`
    - `sklearn.model_selection.StratifiedShuffleSplit`
    - `sklearn.model_selection.StratifiedKFold`

## Data Analysis
- Visualization
    - Color, shades, size of dots can be used to add more dimensions to a 2D visualization
- Correlations: 
    - `df.corr()` only covers linear correlations disregarding complex patterns or slopes
    - `pandas.plotting.scatter_matrix`
- Attributes combinations

## Prepare the Data
1. Data Cleaning
    - Missing data
        - Drop row with missing `df.dropna()`
        - Drop column with missing `df.drop(col1, axis=1)`
        - Imputation
            - Fixed value `df.fillna(value)`
            - Median or mean `sklearn.impute.SimpleImputer`
2. Encoding of text and categorical data
    - `sklearn.preprocessing.OrdinalEncoder`
    - `sklearn.preprocessing.OneHotEncoder`
3. Feature scaling (normalization, etc.)
    - `sklearn.preprocessing.MinMaxScaler`
    - `sklearn.preprocessing.StandardScaler`
4. Create a data pipeline
    - `sklearn.pipeline.Pipeline`: chain the data transformers for the same group of columns
    - `sklearn.compose.ColumnTransformer`: combine pipelines for different groups of columns

## Select and train a model
1. Create a evaluation dataset for hyperparameter tuning
    - One-holdout (train_test_split on training dataset)
    - Cross-Validation `sklearn.model_selection.cross_val_score`
2. Hyperparameter tuning 
    - Grid search `sklearn.model_selection.GridSerachCV`
    - Random search `RandomizedSearchCV`
    - 
3. Evaluate the model
    - Feature importance
    - Performance metrics
        - `sklearn.model_selection.cross_val_score`
        - `sklearn.model_selection.cross_val_predict`
    - Confidence interval `scipy.stats.t.interval()` (overall confidence interval, not a confidence band)

## Deployment
- Deployment & Serve (REST API)
- Monitor
- Maintain
