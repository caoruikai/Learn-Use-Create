# Chapter 6 - Decision Trees

## Scikit-Learn
- `sklearn.tree.DecisionTreeClassifier`
- `sklearn.tree.DecisionTreeRegressor`

## Quality
- Sensitive to data rotation because it is easier to split the feature space orthogonally.
- Sensitive to small variations in the data.
- Does not need to standardize the data

## CART Classifiction & Regression Tree
- For each iteration, combination of features and thresholds to split the data were compared using the reduction of the cost function
- For classification the cost function is the weighted sum of left node Gini Impurtiy (or Entropy) and right node Gini Impurity (or Entropy)
- For regression the cost function is the weighted sum of left node MSE and right node MSE
- Stop the splitting once it reaches max_depth or cannot reduce impurity.

## Measures and Cost Functions
- Gini Impurity
    - For each node in the tree, calculate the ratio of each class instances among all instances in the node.
    - Gini impurity for that node is 1 - sum(square of all the ratios above)
- Entropy
    - Using the same ratios as Gini Impurity
    - Entropy = - sum(ratio * log_2(ratio))

## Regularization
- Regularize by hyperparameters: max_depth, min_samples_split, min_samples_leaf, min_weight_fraction_leaf, max_leaf_nodes, max_features
- Pruning: chi-square test

## Evaluaton & Visualizaton
- Visualize the tree: `sklearn.tree.export_graphviz`