# Chapter 11 - Training Deep Neural Networks

## The Vanishing/Exploding Gradients Problem

### Problem
- Vanishing Gradients
    - Gradients in the lower layers get smaller in training.
    - Gradient Descent update leaves the lower layers connection weights virtually unchanged.
- Exploding Gradients
    - Gradients get larger and larger in training.

### Solutions

- Initialization
    - Glorot Initialization (Xavier Glorot & Yoshua Bengio, 2010)
        - If the variance of output equals the variance of input, then the layer does not suffer from vanishing/exploding gradient problem.
        - The equal variance is not guaranteed unless the number of inputs (fan-in) and neurons (fan-out) are the same.
        - Glorot Initialization is a pratical method that works in practice even when the fan-in and fan-out are not the same.
        - Glorot Initializaion
            - fan-avg = (fan-in + fan-out) / 2
            - Activation: logistic, None, tanh, softmax
            - Initialize the layer with one of the following
                - Normal distribution with mean 0 and variance $\sigma^2 = \frac{1}{\text{fan}_{\text{avg}}}$
                - Uniform(-r, r), with $r=\sqrt{\frac{3}{\text{fan}_\text{avg}}}$, or $r=\sqrt{3\sigma^2}$
    - Lecun Initialization for SELU activation: replace fan_avg with fan_in in the normal distribution in Glorot Initialization
    - He Initialization for ReLU activation and variants
        - Normal with mean 0 and variance $\sigma^2 = 2/\text{fan}_\text{in}$
        - Uniform with $r=\sqrt{3\sigma^2}$
    - Keras implementation
        - `Dense` default: Glorot initialization with normal distribution
        - He initialization: `keras.layers.Dense(10, activation="relu", kernel_initializer="he_normal")`
        - He uniform but replace fan_in with fan_avg
            ```Python
            he_avg_init = keras.initializers.VarianceScaling(scale=2., mode='fan_avg', distribution='uniform')
            keras.layers.Dense(10, activation='sigmoid', kernel_initializer=he_avg_init)
            ```

- Nonsaturating Activation Functions
    - ReLU activation function
        - Pros
            - Fast to compute
            - Do not sacturate for postive values
        - Cons
            - "Dying ReLU": some neurons always output 0, especially when learning rate is large
    - Leaky ReLU: an activation function solving "dying ReLU" problem
        - Leaky ReLU: $\text{LeakyReLU}_\alpha (z) = \text{max}(\alpha z, z)$
        - $\alpha$ usually is set to 0.01 or 0.2, defining the slope when z<0
        - Dead neurals (always output 0) have a change to "wake up" (output > 0)
        - Randomized Leaky ReLU (RReLU)
            - $\alpha$ is picked ramdomly in training and fixed to an average in testing.
            - Regularize the model
        - Parametric Leaky ReLU (PReLU)
            - fit $\alpha$ as a parameter
            - Outperform ReLU on large dataset, but runs the risk of overfitting in small dataset.
    - ELU: Exponetial Linear Unit; Djork-Arné Clevert et al. (2015)
        - Formula: $\text{ELU}_\alpha(z) = \alpha (\exp{(z)} - 1) \text{ if } z < 0; \text{  } z \text{ if } z \le 0$
        - Pro
            - Help with the vanishing gradients problem
            - Avoids the dead neuron problem
            - Smooth everywhere when $\alpha = 1$, speeding up Gradient Descent
        - Con
            - Slower to compute
    - SELU: Scaled Exponential Linear Unit; Günter Klambauer et al. (2017)
        - Using SELU, a network self-normalizes (mean 0, std 1) if:
            - All layers are dense.
            - All hidden layers use SELU as activation functions.
            - The input features must be standardized (mean 0, std 1)
            - Each hidden layer's weight must be initialized with Lecun Initialization. `kernel_initializer="lecun_normal"`
            - Sequential (the simpliest) model architecture, no recurrent, no skip connections.
    - Choice of activation function
        - Generally SELU > ELU > leaky ReLU > ReLU > tanh > logistic
        - Convenient, easy to find, thus maybe fastest: ReLU
        - If the network does not satisfy "self-nomalization" assumptions: ELU > SELU
        - Reduce runtime latency: Leaky ReLU
        - No extra parameter tuned: fixed $\alpha$ Leaky ReLU
        - Have spare time and computing power: use cross-valiation for RReLU (if overfitting) or PReLU (if dataset is huge)
    - Kera Implementation
        - Leaky ReLU or PReLU: create a `LeakyReLU` layer after the layer you want to apply it to
            ```Python
            model = keras.models.Sequential([
                [...]
                keras.layers.Dense(10, kernel_initializer='he_normal'),
                keras.layers.LeakyReLU(alpha-0.2) # or keras.layers.PReLU() if PReLU is used
                [...]
            ])
            ```
        - SELU: `layer = keras.layers.Dense(10, activation="selu", kernel_initializer="lecun_normal")`

- Batch Normalization
    - Sergey Ioffe & Christian Szegedy (2015)
    - Method
        - Add a normalization layer between dense layers
        - Layers in between does not need the bias parameter
        - Each batch normalization layer contains 2 parameters
            - 2 trainable (trained by backpropagation)
                - $\gamma$: output scale parameter vector
                - $\beta$: output shift (offset) parameter vector
            - 2 non-trainable (not by backpropagation), used in testing and scoring only
                - $\mu$: average of training data, usually moving average (e.g. Keras)
                - $\sigma$: standard deviation of training data, usually moving std (e.g. Keras)
        - Output of a Batch normalization layer (for a mini-batch B with $m_B$ instances and an instance i)
            - Mean of the mini-batch: $\bm{\mu}_B = \frac{1}{m_B} \sum^{m_B}_{i=1} \bm{x}^{(i)}$
            - Variance of the minit-batch: $\bm{\sigma}_B^2 = \frac{1}{m_B} \sum^{m_B}_{i=1}(\bm{x}^{(i)} - \bm{\mu}_B)^2$
            - Normalized i-th instance: $\hat{\bm{x}}^{(i)} = \frac{\bm{x}^{(i)} - \bm{\mu}_B}{\sqrt{\bm{\sigma}_B^2 + \epsilon}}$
                - $\epsilon$ is a tiny number to avoid devision by zero (typically 1e-5)
            - $\bm{z}^{(i)} = \gamma \otimes \hat{\bm{x}}^{(i)} + \beta$
                - $\otimes$ is element-wise multiplication
        - Example in Keras
            ```Python
            model = keras.models.Squential([
                keras.layers.Flatten(input_shape=[28,28]),
                keras.layers.BatchNormalization(),
                keras.layers.Dense(300, activation="elu", kernel_initializer="he_normal", use_bias=False),
                keras.layersBatchNormalization(),
                [...]
            ])
            ```
        - Hyperparameters
            - `momentum`
                - Momentum is used to update the moving average: $\hat{\bm{\mu}} \leftarrow \hat{\bm{\mu}} \times \text{momentum} + \bm{\mu}_B \times (1 - \text{momentum})$
                - Usually set to a value closing to 1 (e.g. 0.9, 0.99)
            - `axis` controls the dimention to be normalized.
                - Defaults -1, meaning normalize the last axis, or compute the means and variance across all other axes.
                - In other words, it is the axis to be preserved (not to be collapsed) in the normalization.

- Gradient Clipping
    - Used in *recursive models* most, since batch normalization is tricky to use.
    - Set `clipvalue`. Any dimension of the gradient will be capped with this value
    - Set `clipnorm`: gradients are normalized and the norm will be capped with this value
    - Example 
        ```Python
        optimizer= keras.optimizers.SGD(clipvalue=1.0)
        model.compile(loss="mse", optimizer=optimizer)
        ```

## Reusing Pretrained Layers - Transfer Learning

### Guidance
- Steps
    1. Find an existing DNN that sovles a similar problem.
    2. Freeze the lower layers by making the parameter non-trainable.
    3. Add layers after the frozen layers and train them.
- Tips
    - More useful in large convolutional networks than small dense networks.
    - Number of layers to freeze: the more training data one has, the less layers to freeze.
    - Number of layers to add: the more training data one has, the more layers to add.
    - Reduce the learning rate to avoid wrecking the existing parameters.

### Transfer Learning with Keras
```Python
# 1. Load an existing model A
model_A = keras.models.load_model("my_model_A.h5")

# 2. Make a clone of model A if you want to keep model A intact
model_A_clone = keras.models.clone_model(model_A)
model_A_clone.set_weights(model_A.get_weights())

# 3. Create a model B based on part of model A
model_B_on_A = keras.models.Sequential(model_A.layers[:-1])

# 4. Add extra layers for B
model_B_on_A.add(keras.layers.Dense(1, activation="sigmoid"))

# 5. Freeze the original layers' parameters from model A for the first few epoches
for layer in model_B_on_A.layers[:-1]:
    layer.trainable = False
# Always compile the model after freezing or unfreezing
model_B_on_A.compile(loss="binary_crossentropy", optimizer="sgd", metrics=["accuracy"])

# 6. Train the model for a few epoches
history = model_B_on_A.fit(X_train_B, y_train_B, epochs=4, validation_data=(X_valid_B, y_valid_B))

# 7. Unfreeze the layers and compile again
for layer in model_B_on_A.layers[:-1]:
    layer.trainable = True

optimizer = keras.optimizers.SGD(lr=1e-4)
model_B_on_A.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=["accuracy"])

# 8. Train the model for the rest of the epochs
history = model_B_on_A.fit(X_train_B, y_train_B, epochs=16, validation_data=(X_valid_B, y_valid_B))
```

### When Labeled Data is Scarce
- Unsupervised pretraining: training an autoencoder or GAN using unlabled data, then the last few layers using labeled data.
- Auxiliary Task: change the definition of the task to a similar one so some existing models or data can be used, then train it using the data with exact labels.
- Self-supervised learning: labels are automatically generated.

## Faster Optimizers
- The following are all 1st order (Jacobians) optimizers. For DNN, it is too slow and memory intensive to use 2nd order (Hessian) optimizers.

### Momentum Optimization
- Origianl Version: Boris Polyak 1964
    - Update the momentum and then the weight, unlike in Gradient Descent
        1. $\nabla_\theta J(\theta)$ is the gradient of the cost function $J(\theta)$ for weights $\theta$
        2. $\bm{m} \leftarrow \beta \bm{m} - \eta \nabla_\theta J(\theta)$
        3. $\theta \leftarrow \theta + \bm{m}$
    - Hyperparameters
        - $\eta$: learning rate for momentum
        - $\beta \in [0, 1]$: called `momentum` in Keras, controlling the "friction", usually 0.9 works well
    - Pros
        - Faster than Gradient Descent around the "plateaus and valleys"
        - Easier to past local optima
        - Works well if batch normalization is not used for upper layers
    - Cons
        - One more hyperparameter to tune
    - In Keras: `optimzier = keras.optimizer.SGD(lr=0.001, momentum=0.9)`
- Nesterov Accelerated Gradient
    - Yurii Nesterov 1983
    - Use the gradient not at the local weight, but with a shift
        1. $\bm{m} \leftarrow \beta \bm{m} - \eta \nabla_\theta J(\theta + \beta \bm{m})$
        2. $\theta \leftarrow \theta + \bm{m}$
    - Faster than vanilla momentum optimization
    - Keras: `optimzier = keras.optimizer.SGD(lr=0.001, momentum=0.9, nesterov=True)`

### AdaGrad
- John Duchi et al. 2011
- Scales down the learning rate (adaptive learning rate) on the dimension where the gradient is large.
- Algorithm
    1. $\bm{s} \leftarrow \bm{s} + \nabla_{\bm{\theta}} J(\bm{\theta}) \otimes \nabla_{\bm{\theta}} J(\bm{\theta})$
    2. $\bm{\theta} \leftarrow \bm{\theta} - \eta \nabla_{\bm{\theta}} J(\bm{\theta}) \oslash \sqrt{\bm{s} + \epsilon}$
    - $\otimes$ and $\oslash$ are element-wise multiplication and division
- Performs well for quadratic problems, but often stops too early for DNN
- Less need to tune learning rate since it is adaptive

### RMSProp
- Add an exponential decay hyperparameter $\beta$ to the updates of adaptive factor of learning rate.
- Avoid too fast slow down in the descent in AdaGrad
- Algorithm
    1. $\bm{s} \leftarrow \beta\bm{s} + (1-\beta)\nabla_{\bm{\theta}} J(\bm{\theta}) \otimes \nabla_{\bm{\theta}} J(\bm{\theta})$
    2. $\bm{\theta} \leftarrow \bm{\theta} - \eta \nabla_{\bm{\theta}} J(\bm{\theta}) \oslash \sqrt{\bm{s} + \epsilon}$
    - $\otimes$ and $\oslash$ are element-wise multiplication and division
    - $\beta$ as 0.9 usually works well.
- Keras: `optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9)`
- Less need to tune learning rate since it is adaptive

### Adam (Adaptive Moment Estimation), AdaMax & Nadam
- Diederik P. Kingma & Jimmy Ba, 2014
- Tracks exponential decaying average of both past gradients (like momentum optimization) and past squared gradients (like RMSProp).
- Algorithm
    1. Initialize $\bm{m}=\bm{s}=\bm{0}$, $\beta_1=0.9$, $\beta_2=0.999$, $\epsilon=10^{-7}$
    2. $\bm{m} \leftarrow \beta_1 \bm{m} - (1-\beta_1) \nabla_\theta J(\bm{\theta})$
    3. $\bm{s} \leftarrow \beta_2\bm{s} + (1-\beta_2)\nabla_{\bm{\theta}} J(\bm{\theta}) \otimes \nabla_{\bm{\theta}} J(\bm{\theta})$
    4. $\hat{\bm{m}} \leftarrow \frac{\bm{m}}{1-\beta_1^T}$ with T as the number of iteration
    5. $\hat{\bm{s}} \leftarrow \frac{\bm{s}}{1-\beta_2^T}$ with T as the number of iteration
    6. $\bm{\theta} \leftarrow \bm{\theta} + \eta \hat{\bm{m}} \oslash \sqrt{\hat{\bm{s}} + \epsilon}$
- Keras: `optimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999)`
- Adamax: variation of Adam by using $l_\infty$ norm of gradients instead of $l_2$ norm when updating $\bm{s}$
- Nadam: Adam + Nesterov

### Compare optimizers
- `SGD`: slowest, good quality 
- `SGD(momentum=...)`, `SGD(momentum=...,nesterov=True)`: faster than `SGD`, good quality
- `Adagrad`: fast, poor quality
- `RMSprop`, `Adam`, `Nadam`, `AdaMax`: fast, ok to good quality

## Learning Schedules (Strategies to Tune Learning Rate)
- Power scheduling
    - $\eta(t) = \eta_0 / (1 + t/s)^c$
    - t is the iteration number
    - Hyperparameters
        - `$\eta_0`: initial learning rate
        - `c`: power, typically 1
        - `s`: some step
    - After s steps, the learning rate drops to $\eta_0 / 2$, then after anther s steps, drops to $\eta_0 / 3$...
    - Decay slower and slower
    - Keras: `optimzer = keras.optimizers.SGD(lr=0.01, decay=1e-4)`, where `decay` is 1/s, c is always 1 and cannot be tuned.
- Exponential Scheduling
    - $\eta(t) = \eta_0 0.1^{t/s}$
    - Drop by a factor of 10 every s steps, do not slow down like the Power scheduling
    - Keras
        ```Python
        # If lr and s are hard-coded
        def exponential_decay_fn(epoch):
            return 0.01 * 0.1**(epoch / 20)

        # If lr and s are arguments
        def exponential_decay(lr0, s):
            def exponential_decay_fn(epoch):
                return lr0 * 0.1**(epoch / s)
            return exponential_decay_fn
        exponential_decay_fn = exponential_decay(lr0=0.01, s=20)

        # Yet another way to write it
        # Use the initial optimizer's learning rate and previous step's learning rate
        def exponential_decay_fn(epoch, lr):
            return lr * 0.1**(1 . 20)

        # Create a LearningRateScheduler callback
        # Give the callback the schedule function
        # Pass the callback to the fit() method
        lr_scheduler = keras.callbacks.LearningRateScheduler(exponential_decay_fn)
        history = model.fit(X_train_scaled, y_train, [...], callbacks=[lr_scheduler])
        ```
- Piecewise constant scheduling
    - Use difference constant learning rate for different stages
    - Keras
        ```Python
        def piecewise_constant_fn(epoch):
            if epoch < 5:
                return 0.01
            elif epoch < 15:
                return 0.005
            else:
                return 0.001
        # Then use the LearningRateScheduler callback
        ```
- Performance scheduling
    - Measure the validation error every N steps, and reduce the learning rate by a factor when the error stops dropping.
    - Keras: `lr_scheduler = keras.ReduceLROnPlateau(factor-0.5, patience=5)`. It multiplies the learning rate with `factor` if the best validation loss does not improve for `patience` number of epochs.
- 1cycle scheduling
    - Leslie Smith, 2018
    - Increase from initial learning rate to a second rate linearly for the first half of the training, then reduce back to the initial rate during the later half the training.
    - If using momentum, decrease the momentum and then increase back to the initial one.
- Survey & Comparison: Andrew Senior et al., 2013
- Tips on Keras Implementation
    - Set `fit(initial_epoch=...)` to set the inital epoch number if continue training a model, not from scrach. Because the final epoch number is not saved with the model.
- `tf.keras` implementation
    - Define the scheduel using `keras.optimizers.schedules`, and pass it to any optimizer
    - Example: Exponential Scheduling
        ```Python
        s = 20 * len(X_train) // 32 # number of steps in 20 epochs with batch size = 32
        learning_rate = keras.optimizers.schedules.ExponentialDecay(0.01, s, 0.1)
        optimizer = keras.optimizers.SGD(learning_rate)
        ```

## Regularization

### Early Stopping

### Batch Normalization

### L1 and L2 Regularization
- L1 Regularization leads to a sparse model (with many weights equal to 0)
- Keras: `keras.layers.Dense(100, activation="elu", kernel_initializer="he_normal", kernel_regularizer=keras.regularizers.l2(0.01))`
    - L1: `kernel_regularizer=keras.regularizers.l1()`
    - L2: `kernel_regularizer=keras.regularizers.l2()`
    - L1 & L2: `kernel_regularizer=keras.regularizers.l1_l2()`

### Dropout
- Geoffrey Hinton 2012, Nitish Srivastava et al., 2014
- Algorithm
    - At every training step, every neuron (including input neurons, but excluding output neurons) has a probability p of being "dropped out", meaning ignored during this training step but maybe active again in the next.
    - Dropout rate p:
        - Typically 10% to 50%
        - 20% to 30% for RNN
        - 40% to 50% for CNN
- Tips in practice
    - Usually only applied to top 1 to 3 layers (excluding the output layer), sometimes only after the last hidden layer.
    - Training and validation loss can be misleading if dropout is applied.
    - Weights needs to be multiplied by "keep probability" (1-p) after training.
    - SELU & self-normalizing networks: alpha dropout
- Keras: `keras.layers.Dropout(rate=0.2)`

### Monte Carlo (MC) Dropout
- Dropout has a Bayesian explanation
- Once a model is trained using dropout, then
    - Repeat the prediction N times
    - Average the prediction
    - The result is the MC Dropout prediction
- Example
    ```Python
    y_probas = np.stack([model.predict(X_test_scaled, training=True)]) # training=True to activate dropout
    y_proba = y_probas.mean(axis=0)
    ```
- Can be used to improve probability estimation and uncertainty estimates

### Max-Norm Regularization
- After each training step, update the weight as $\bm{w} \leftarrow \bm{w} r / \Vert \bm{w} \Vert_2$.
- r is a hyperparameter where the L2 norm of weight cannot exceed.
- Keras: `keras.layers.Dense(100, activation="elu", kernel_initializer="he_normal", kernel_constraint=keras.constraints.max_norm(1.))`

### Tip: use Python `functools.partial()` to avoid repeating layers in code. 
- Example:
    ```Python
    from functools import partial

    RegularizedDense = partial(keras.layers.Dense,
                                activation = "elu",
                                kernel_initializer="he_normal",
                                kernel_regularizer=keras.regularizers.l2(0.01)
                              )

    model = keras.model.Sequential([
        keras.layers.Flatten(input_shape=[28,28]),
        RegularizedDense(300),
        RegularizedDense(100),
        RegularizedDense(10, activation="softmax", kernal_initializer="glorot_uniform")
    ])
    ```

## Summary & Practice Guide

### Default DNN Setting
- Kernel initializer: He initialization
- Activation function: ELU
- Normalization: None if shallow, Batch Norm if deep
- Regularization: Early Stopping (+L2 if needed)
- Optimizer: Momentum (or RMSProp or Nadam)
- Learning rate schedule: 1cycle

### Simple Stack of dense layers that can self-normalize
- Kernel initializer: LeCun initialization
- Activation function: SELU
- Normalization: None
- Regularization: Alpha Dropout if needed
- Optimizer: Momentum (or RMSProp or Nadam)
- Learning rate schedule: 1cycle

