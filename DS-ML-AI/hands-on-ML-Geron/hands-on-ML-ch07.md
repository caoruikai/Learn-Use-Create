# Chapter 7 - Ensemble Learning and Random Forests

## Ensemble Learning
- Ensemble learning: aggregate the predictions of a group of predictors.
- Voting classifiers: take the majority vote of multiple types of classifiers

## Bagging & Pasting
- Bagging & Pasting: training different predictors on random subset of training data using the same method
- Bagging: The subsets were sampled with replacement. `sklearn.ensemble.BaggingClassifier(bootstrap=True)`
- Pasting: The subsets were sampled without replacement. `sklearn.ensemble.BaggingClassifier(bootstrap=False)`
- Aggregation: most frequent prediction or average of regression
- Out-of-Bag Evaluation: some instances may not be used in training so can be used for evaluation
    - `sklearn.ensemble.BaggingClassifier(bootstrap=True, oob_score=True)`
    - Results are in `oob_score_` or `oob_decision_function` variable
- `BaggingClassifier` supports sampling features by setting `max_features` and `bootstrap_features`

## Random Forest
- Random forest is an ensemble of decision trees, trained by bagging (or pasting)
- `sklearn.ensemble.RandomForestClassifier`
- `sklearn.ensemble.RandomForestRegressor`
- For each tree training, only a random subset and a random set of features are used
- Extra-Tree (Extremely Randomized Trees)
    - Use a random threshold for each features when splitting using that feature.
    - `ExtraTreesClassifier`
- Feature Importance
    - How much the tree nodes that use a certain feature reduce the impurity on average across all the trees
    - `feature_importances_`

## Boosting
- Train weak learners sequentially, then aggregate their results
- Cannot be paralellized
- Ada Boost
    - For each iteration, increase the weight of misclassified instances and train again.
    - Scikit-Learn version: SAMME for multiclass Ada Boost `sklearn.ensemble.AdaBoostClassifier`
- Gradient Boosting
    - Train each learner on the residual errors of the previous one
    - `sklearn.ensemble.GradientBoostingRegressor`
        - `learning_rate` scale the contribution of each tree. Lower values mean more trees are needed.
        - `max_depth`, `min_sample_leaf`, `subsample` to regularize the trees

## Stacking
- Use a model as the aggregation (blender)