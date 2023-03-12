# Chapter 4 - Training Models

## Linear Regression
- target = linear combination of features
- Training algorithms
    - Closed-form: normal equation: `sklearn.linear_model.LinearRegression`
        - It requires calculations of pseudoinverse of the matrix by Singular Value Decomposition (SVD)
        - Computational complexity is high for large number of features
        - Training data must fit in memory
    - Gradient Descent: `sklearn.linear_model.SGDRegressor`
- Polynomial Regression
    - Can fit non-linear patterns
    - Adding powers of features as new features to the linear form
    - `sklearn.preprocessing.PolynomialFeatures`

## Gradient Descent
- Types
    - Batch Gradient Descent
        - use the whole batch (all) training data to calculate the gradient vector
        - Cannot be used when the dataset is too large for the memory
    - Stochastic Gradient Descent
        - pick a random instance to calculate the gradient vector
        - Can escape local optimum
        - May never reach global optimum
    - Mini-batch Gradient Descent
        - Pick a random mini-batch to calculate the gradient vector
        - In between batch and stochastic GD
- Algorithm
    1. Calculate the partial derivative formula of the loss (cost) function w.r.t. each trainable parameter
    2. Initialize the trainable parameters with random values
    3. In the parameter space, calculate the values of gradient vector
    4. Update the paramters by adding learning-rate * gradient vector
- Pros and Cons
    - Pros
        - Can be used on larget datasets that cannot be fit in memory
        - Relatively fast
    - Cons
        - Maynot reach global optimum
- Hyperparameters
    - Learning rate: grid search; scheduling
- Best practices
    - Standardize all the features

## Learning Curve & Bias/Variance Trade-off
- Train different models using different data sizes
- learning curve: loss function on the evaluation dataset of the trained models v.s. different training data size
- High Bias: underfit the data, prediction errors
- High Variance: overfit the data, poor generalization on new data

## Regularized Linear Models
- Ridge Regression `sklearn.linear_model.Ridge`
    - Add L2 regular term to the loss function (MSE)
    - The regular term is a L2 norm function of the parameter vector
- Lasso Regression `sklearn.linear_model.Lasso`
    - Add L1 regular term to the loss function (MSE)
    - The regular term is a L1 norm function of the parameter vector
    - Some coefficients can be zeros. Equivalent to feature selection
- Elastic Net `sklearn.linear_model.ElasticNet`
    - Mix of Ridge and Lasso

## Early stopping
- Calculate the evaluate set loss for different epoches and find the epoch with minimum loss and select that model.

## Logistic & Softmax Regression
- Output the logitics (sigmoid) of the linear combinations of the features
- Cost function: if actual_y=1 then -log(p_hat); if actual_y=0 then -log(1-p_hat)
- Training: no closed form solution, gradient descent can be used
- `sklearn.linear_model.LogisticRegression`
- Softmax Regression for multilabel problems
    - Cross-entroy cost function (multilabel version of logistic cost function)
    - `LogisticRegression(multi_class="multinomial", solver="lbfgs", C=10)`
