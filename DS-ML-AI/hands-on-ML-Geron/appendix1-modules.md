# Important Modules Imported in the Book

## scikit-learn

| Module | Class | Method | Attributes | Note |
|   ---  |  ---  |   ---  |    ---     | ---  |
| model_selection | | train_test_split() |
| model_selection | | StratifiedShuffleSplit() |
| model_selection | | cross_val_score() |
| model_selection | | cross_val_predict() |
| model_selection | GridSearchCV | fit() | best_params_, best_estimator, sv_results_ |
| model_selection | RandomizedSearchCV |
| model_selection | StratifiedKFold | split()
| impute | SimpleImputer | fit(), transform(), fit_transform() | statistics_ |
| preprocessing | OrdinalEncoder | fit(), transform(), fit_transform() | categories_ |
| preprocessing | OneHotEncoder | fit(), transform(), fit_transform() | categories_|
| preprocessing | StandardScaler | fit(), transform(), fit_transform() | 
| preprocessing | MinMaxScaler | fit(), transform(), fit_transform() | 
| preprocessing | PolynomialFeatures | fit(), transform(), fit_transform() | 
| base | BaseEstimator | get_params(), set_params() |
| base | TranformerMixin | fit(), transform(), fit_transform() |
| base | clone | fit(), predict() |
| pipeline | Pipeline | fit(), transform(), fit_transform() | | for numerical columns |
| compose | ColumnTranformer | fit(), transform(), fit_transform() | | for numerical & categorical columns |
| metrics | | accuracy() |
| metrics | | mean_squared_error() |
| metrics | | confusion_matrix() |
| metrics | | precision_score() |
| metrics | | recall_score() |
| metrics | | precision_recall_curve() |
| metrics | | roc_curve() |
| metrics | | roc_auc_score() |
| metrics | | f1_score() |
| metrics | | silhouette_score() |
| linear_model | LinearRegression | fit(), predict() | intercept_, coef_ |
| linear_model | SGDClassifier | fit(), predict() |
| linear_model | SGDRegressor | fit(), predict() | intercept_, coef_ |
| linear_model | Ridge | fit(), predict() |
| linear_model | Lasso | fit(), predict() |
| linear_model | ElasticNet | fit(), predict() |
| linear_model | LogisticRegression | fit(), predict(), predict_proba() |
| tree | DecisionTreeRegressor| fit(), predict() |
| tree | DecisionTreeRClassifier| fit(), predict(), predict_proba() |
| ensemble | VotingClassifier | fit(), predict() |
| ensemble | BaggingClassifier | fit(), predict() | oob_score_ |
| ensemble | AdaBoostClassifier | fit(), predict() |
| ensemble | RandomForestRegressor | fit(), predict() |
| ensemble | RandomForestClassifier | fit(), predict() |
| ensemble | GradientBoostingRegressor | fit(), predict() |
| svm | SVC | fit(), predict(), decision_function() | classes_ |
| svm | LinearSVC | fit(), predict() |
| svm | SVR | fit(), predict() |
| svm | LinearSVR | fit(), predict() |
| multiclass | OneVsRestClassifier(EstimatorClass()) | fit(), predict() | estimators_ |
| neighbors | KNeighborsClassifier | fit(), predict() |
| decomposition | PCA | fit(), transform(), fit_transform() | explained_variance_ratio_ |
| decomposition | IncrementalPCA | partial_fit(), transform() |
| decomposition | KernelPCA | fit(), transform(), fit_transform() | 
| manifold | LocallyLinearEmbedding | fit(), transform(), fit_transform() | 
| cluster | KMeans | fit_predict(), score() | labels_, cluster_centers, inertia_ |
| cluster | MiniBatchKMeans | fit() |
| cluster | DBSCAN | fit() | labels_, core_sample_indices_, components_ |
| mixture | GuassianMixture | fit(), predict(), predict_proba(), sample(), score_samples(), bic(), aic() | means_, covariances_, converged_, n_iter_ |
| mixture | BaysianGuassianMixture | fit(), 


## pandas

| Module | Class | Method |
|  ---   |  ---  |  ---   |
| plotting | | scatter_matrix |
