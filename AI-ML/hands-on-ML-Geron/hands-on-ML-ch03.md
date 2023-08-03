# Chapter 3 - Classification

## Performance Measures

### Confusion Matrix
- `sklearn.metrics.confustion_matrix`
- Row: actual class; column: predicted class
- TP/FP/TN/FN: true/false positive/negative; "Positive" or "Negative" here means predicted as positive or negative.

### Terminology Tips
- The denominators of all the "rates" are the actual values. For example, the denominator of FPR (false postive rate) is "all actual negatives"
- The numerators of all the "rates" are the predicted values. For example, the numerator of FPR (false positve rate) is "falsely predicted as positives (actual negative values)"
- Precision is special: the denomitor is all predicted postives while the numerator is true postives.

### Precision, Recall & F-1
- Precision = TP / (TP+FP or all predicted positive); Among all predicted positives, what proportion is actually postive?
- Recall (sensitivity or true positive rate) = TP / (TP+FN or all actual positive); Among all actual postives, what proportion is correctly predicted as positive?
- F1 score: harmonic mean of precision and recall
    - F1 = 2 / (1/precision + 1/recall)
    - The F1 is high only if both precision and recall are high
    - F1 favors classifiers with similar precision and recall
- `sklearn.metrics.precision_score`, `sklearn.metrics.recall_score`, `sklearn.metrics.f1_score`

### Precision/Recall Trade-off and PR Curve
- Most classifiers output a numeric score for each instance. Precision and recall depends on a threshold to separate the positve and negatice predictions.
- When changing the threshold, both precision and recall might change. In general, when precision goes up, recall goes down. So the goal is to select a threshold with best enough precision given fixed good enough recall, or vice versa.
- Precision-Recall Curve: Precision (y-axis) v.s. Recall (x-axis)
- A better PR curve is the one closer to the upper-right corner.

### ROC Curve
- True negative rate (specifity): TN / (all actual negatives)
- False positive rate: 1- TNR or FP / (all actual negatives)
- Receiver operating characterisitc (ROC) is a curve of true postive rate (recall) v.s. false postive rate
- AUC (Area under Curve) between 0 and 1 is used to evaluate the classifier
- It is easy to have high AUC for very imbalanced data. PR is prefered in this case.
- `sklearn.metrics.roc_curve`, `sklearn.metrics.roc_auc_score`

## Multiclass Classification
- Use multiple classifiers to classify multiclass targets
    - One-versus-the-Rest (OvR); `sklearn.multiclass.OneVsRestClassifer` is a wrapper for binary classifiers.
    - One-versus-One (OvO); `sklearn.svm.SVC` by default use OvO for multiclass targets.
- Some models can output multiclass predictions (softmax) like GBM and neural networks

### Error Analysis
- Confusion matrix
    - `plt.matshow` help to visualize the confusion matrix
- Error rate version of confusion matrix: divide each value in confusion matrix by the count of values in the actual class.

## Multilabel & Multioutput
- Multilabel: output a vector of targets, each is a binary target.
    - Example: classify a photo with multiple persons as target
- Multioutput-multilabel: output a vector of targets, each is a multilabel target.
