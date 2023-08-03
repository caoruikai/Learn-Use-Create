# Chapter 8 - Dimensionality Reduction

## Curse of Dimensionality
- High dimensional spaces are sparse. Two points in them are very likely to be distant from each other. The model trained with such dataset can be unreliable.
- Training speed is too slow.
- Two main approach to reduce dimensionality
    - Projection (like PCA): project the data into a lower dimensional subspace. Some rolled and folded data (swiss roll) cannot be easily projected.
    - Manifold Learning (like LLM): learn the lower dimentional manifold

## PCA
- Principle Component Analysis: project the high dimensional data into a low dimensional subspace that preserve the most variance.
- Principle Components can be found using Singular Value Decomposition (SVD). `numpy.linalg.svd()`
- Data needs to be centered around zeros before using PCA.
- Selecting top d princile components reduces the data into d dimensions
- `sklearn.decomposition.PCA`
    - `components_`
    - `explained_variance_ratio_`: proportion of the datasets variance that lies along each component
- Choosing a right number of components that adds up to a certain proportion of total explained variances (`n_components=0.9`)
- Randomized PCA: `sklearn.decomposition.PCA(svd_solver="randomized")` speed up the computation
- Incremental PCA: `sklearn.decomposition.IncrementalPCA`. Can do PCA for min-batches for datasets larger than memory.
- Kernel PCA: `sklearn.decomposition.KernelPCA`. It applies non-linear kernels to preserve clusters or folds.
- Hyperparameter tuning
    - There is no error metrics for unsupervised learning, but if there are supervised stages, hyperparameters in PCA/kPCA can be tuned together.
    - Minimize reconstruction error `KernelPCA(fit_inverse_transform=True)`

## LLM
- Locally Linear Embedding
    1. Find the k nearest neighbors of each training instance
    2. Find the (weights of the) linear combination of the instance's nearest neighbors that is closest to the instance itself.
    3. Given the linear weights above, find the image of each instance on the low dimensional space such that the distance between each image and its k nearest neighbors are the closest.
- `sklearn.manifold.LocallyLinearEmbedding`

## Other Dimension Reductions
- Random Projections
- Multidimensionnal Scaling (MDS)
- Isomap
- t-Distributed Stochastic Neighbor Embedding (t-SNE)
- Linear Discriminant Analysis (LDA)