# Chapter 10 - Introduction to Artificial Neural Networks with Keras

## Artificial Neuron
- Input: vector $\vec{x}$
- Connection weights $\vec{w}$
    - Weights assigned to each edge between a neuron from previous layer to the current neuron
    - Same dimension as input vector $\vec{x}$
- Output (a number): $h_{\vec{w}} (\vec{x}) = \phi(\vec{x}^T \vec{w})$
    - $\phi$: activation function
- Example: Threshold logic unit (TLU) a.k.a linear threshold unit (LTU)
    - Use some step function as the activation function, can be one of the following:
        - heaviside(z) = 0 if z < 0; 1 if z >= 0
        - sgn(z) = -1 if z < 0; 0 if z = 0; +1 if z > 0
        
        
## Perceptron (single layer) (Rosenblatt 1957)
- Input layer composed of input neurons and a bias neuron (always output 1)
- Output layer composed of output neurons (e.g. TLUs)
    - $\vec{h}_{\boldsymbol{W},\vec{b}} (\boldsymbol{X}) = \phi(\boldsymbol{X} \boldsymbol{W}) + \vec{b}$
        - $\boldsymbol{X}$: the matrix of input features. One row per instance and one column per feature.
        - $\boldsymbol{W}$: the connection weight matrix. One row per input (previous) neuron (feature) and one column per neuron in the current layer.
        - $\vec{b}$: bias vector: weights between the bias neuron and the neuron in the current layer
        - $\phi$: activation function. It is a step function if neurons are TLUs.
        - $\vec{h}$: Number of output neurons determined the output vector dimension
- The output layer is fully connected (dense) because each neuron is connected to every neuron in the previous layer.
- Training: Hebbs Rule (Hebb 1949)
    - Randomly initialize $\boldsymbol{W}$.
    - For each iteration $t>=1$ (input instance), the weight update for each element in $\boldsymbol{W}$ is $w_{i,j}^t = w_{i,j}^{t-1} + \eta(y_j - \hat{y_j})x_i$
        - $w_{i,j}$ is the weight connecting the ith input neuron and the jth output neuron.
        - $x_i$ is the ith input value of the current training instances
        - $\hat{y}_j$ is the output of jth output neuron for the current training instance
        - $y_j$ is the target output of the jth output neuron for the current training instance
        - $\eta$ is the learning rate.
- Limitation of single layer perceptron
    - Can only learn linear pattern (before the transformation of activation function).
    - Cannot solve simple problems like Exclusive OR (XOR) problem.
        - XOR problem: y = 1 if only one of the x1, x2 = 1; i.e. y(0,0)=0, y(1,1)=0, y(0,1)=y(1,0)=1
        - It's not possible to find a set of weights for a single layer perception with TLUs as neurons to get the results above.
        - Stacking one more layer of a single TLU as the final output layer can solve this problem.
- Scikit Learn Implementation
    ```Python
    # Scikit-Learn's implement of Perceptron

    import numpy as np
    from sklearn.datasets import load_iris
    from sklearn.linear_model import Perceptron

    iris = load_iris()
    X = iris.data[:,(2,3)]
    y = (iris.target == 0).astype(np.int)

    per_clf = Perceptron()
    per_clf.fit(X,y)
    y_pred = per_clf.predict([[2,0.5]])

    # Equivalently, use SGDClassifier with loss="perceptron", learning_rate="constant", eta0=1, and penalty=None
    ```

- ## Multilayer Perceptron (MLP)
- Structure: one input layer, one or more hidden layers, and one output layer.
- Upper layers: layers close to the output layers.
- Lower layers: layers close to the input layers.
- All layers except the output layer includes a bias neuron.
- All layers are fully connected to the next layer.
- Feedforward neural network (FNN): signal flows only in one direction (from the input layer to the output layer).
- Deep neural network (DNN): an ANN with a deep stack of hidden layers.


## Backpropagation
- "Learning Internal Representations by Error Propagation" - Rumelhart, Hinton & Williams 1986
- Reserse-mode autodiff is used to compute gradients.
- Instead of step functions, differentiable activation functions are used
    - logistic (sigmoid) function: $\sigma(z)=1/(1+exp(-z))$
    - hyperbolic tangent function (symmetric around 0, fast to converge): $tanh(z)=2\sigma(2z)-1$
    - retified linear unit function (not differentiable at 0 but fast and good in practice): $ReLU(z) = max(0,z)$
- Without an activation function, the ANN becomes a purely linear function and cannot solve complex problems.
- Backpropagation algorithm
    1. Initialize all the weights randomly. DO NOT initialize the weights using a same value like zero. In that case, each pass will assign same error gradients to all nodes in a layer, leading to the same values after gradient decent like there is only one node per layer.
    2. It handles one mini-batch at a time (an epoch) and eventually goes through the all training set multiple times.
    3. Forward pass: Each mini-batch is fed into the input layer and the final predictions out of the output layer are made, using the weights in the current epoch.
    4. Output errors are computed using a loss function.
    5. Reserve pass: using the chain rule of differentiation, it computes how much of each node contributed to the error for each layer, all the way to the input layer.
    6. The values of the error gradient from last step were used to perform the gradient descent (adjust the weights) for the next epoch.


## Activation Functions
- logistic (sigmoid) function: $\sigma(z)=1/(1+exp(-z))$
- hyperbolic tangent function (symmetric around 0, fast to converge): $tanh(z)=2\sigma(2z)-1$
- retified linear unit function (not differentiable at 0 but fast and good in practice): $ReLU(z) = max(0,z)$
- softplus: a smooth variant of ReLU: $\text{softplus}(z)=log(1+exp(z))$. It is close to 0 when z is negative, close to z when z is positive.
- softmax: used as output activation function to normalize the multi-class classification target: $\text{softmax}(z_j) = \frac{exp(z_j)}{\sum_{i=1}^N{exp(z_i)}}$


## Loss Functions
- Since output $\vec y$ is a vector for each instance, the output of a batch input is a matrix $\boldsymbol Y$, with each row an output from one instance.
- The final value of a loss function must be summarized across both dimensions of the matrix $\boldsymbol Y$.
    - For each element, calculate $loss(y_{i,j} - \hat y_{i,j})$ with the choice of loss function.
    - For each row, calculate average or weighted average of the element-wise loss
        - In TensorFlow, set sample_weight to a matrix with same size as $\boldsymbol Y$
    - Summarize across all rows: avg, sum, weighted-sum
        - In TensorFlow, 
            - set sample_weight to a vector with same size as number of instances in the batch.
            - set `reduction` to `sum_over_batch_size` or `tf.keras.losses.Reduction.SUM_OVER_BATCH_SIZE`: average over instances
            - set `reduction` to `sum` or `tf.keras.losses.Reduction.SUM`: sum over instances
            - set `reduction` to `none` or `tf.keras.losses.Reduction.NONE`: do not summarize and output a vector with the same size as number of instances
- Choices of loss functions:
    - Continuous targets ($e_{i,j}=y_{i,j} - \hat y_{i,j}$)
        - Mean Square Error: $e_{i,j}^2$
        - Mean Absolute Error: $\vert e_{i,j} \vert$
        - Huber Loss, less sensitive to outliers: if $\vert e_{i,j} \vert \le \delta$, then $\frac{1}{2}e_{i,j}^2$; otherwise $\delta(\vert e_{i,j} \vert - \frac{1}{2}\delta)$
    - Binary targets ($\hat{p}_{i,j}$ is the estimated probability)
        - Logloss / Cross Entropy: $-[(1-y_{i,j})\log{(1-\hat{p}_{i,j})} + y_{i,j}\log{\hat{p}_{i,j}}]$


## Regression MLP
- Output dimension: equal to target dimension
- Output activation function: depends on the range of desired output
    - Any range: no activation
    - Postive output: ReLU, softplus
    - Any given range: logistic or hyperbolic tangent, then scale it to the range.
- Hidden activation function: ReLU or SELU
- Loss function: MSE or MAE/Huber (if outliers)


## Classification MLP
- Output layer:
    - Multi-label binary target: one output neuron for each label
    - Single-lable multi-class target: one output neuron for each class, input into the softmax function
        - Softmax function for a series $z_j$: $softmax(z_j) = \frac{exp(z_j)}{\sum_{i=1}^N{exp(z_i)}}$
    - Multi-label multi-class targets: combining multiple "neurons-softmax" components into the output layer.
- Hidden activation function: ReLU or SELU
- Loss function: logloss / cross-entropy

## Autodiff in TensorFlow

[Autodifferentiation](https://en.wikipedia.org/wiki/Automatic_differentiation) (autodiff) are a group of algorithms that computes the partial derivatives. The purpose of the autodiff is to generate the compuation graph for partial derivatives from the computation graph of the original function. Once the graph is computed, it can be saved and used many times later in backpropagation.

To get a compuation graph, a function $\vec y = f(\vec x)$ can be decomposed into the following elements:
- $\vec x$: independent variable vector with length n
- $\vec y$: dependent variable vector with length m
- $w_i$: the ith element to be combined by operators

For example: $y = x_1 x_2 + \sin x_1$
- $w_1 = x_1$
- $w_2 = x_2$
- $w_3 = w_1 w_2$
- $w_4 = \sin x_1$
- $w_5 = w_3 + w_4$

### Forward-Mode Autodiff (not used in TensorFlow)

Forward-Mode Autodiff algorithm

- For each independent variable $x_i$:
    - For each $w_j$:    
        - Computes $\dot{w_j} = \frac{\partial w_j}{\partial x_i}$ for each $w_j$.         
        - Eventually, the compuation reaches $\frac{\partial y_l}{\partial x_i}$.
        
### Reverse-Mode Autodiff (used in TensorFlow)

Reverse-Mode Autodiff algorithm

- For each dependent variable $y_l$:
    - For each $w_j$:
        - Computes $\bar w_j = \frac{\partial y_l}{\partial w_j}$ for each $w_j$
        - Eventually, the compuation reaches $\frac{\partial y_l}{\partial x_i}$.
        
### Compare Forward-Mode and Reverse-Mode Autodiff

- Forward-Mode
    - Goes through one x for each iteration
    - It is expensive for long $\vec x$.
    - Deep learning usually takes many input features (x), which makes forward-mode a bad choice.
- Reverse-Mode
    - Goes through one y for each iteration.
    - It is expensive for long $\vec y$.
    - Deep learning usually has limited number of y's, making reverse-mode a good choice.