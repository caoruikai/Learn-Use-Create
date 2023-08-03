# Chapter 5 - Support Vector Machine

## General Concepts
- The goal of support vector machine is to find a hyperplane in the feature space that can separate the instances by the largest possible margin (distance between the two classes of data)
- Support vectors are the feature vectors that are on the edge of the separation hyperplane.
- Refitting on more instances that beyond the "support band" will not change the fitted model.
- Features should be standardized first
- Output: class, not probabilites

## Soft Margin Classfication
- Allow a limited number of margin violations
- Pros
    - Can be applied to datasets that are not completely linearly separatable
    - Less impacted by outliers
- `sklearn.svm.LinearSVC` or `sklearn.svm.SVC(kernel=linear, C=1)` or `SGDClassifier(loss="hinge", alpha=-1/(m*C))`
    - C is for regularization. Larger C allows more margin violations

## Nonlinear SVM Classification
- Add polynomial features
- Use polynomial kernel `sklearn.svm.SVC(kernel="poly")`
- Use RBF kernel
    - RBF: Gaussian Radial Basis Function
    - `SVC(kernel="rbf")`

## SVM Regression
- Objective is to fit a hyperplane band with as many instances in it.
- `sklearn.svm.LinearSVR`
- `sklearn.svm.SVR`
