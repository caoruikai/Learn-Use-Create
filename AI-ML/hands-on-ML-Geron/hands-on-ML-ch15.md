# Chapter 15 - Processing Sequences Using RNNs and CNNs

## Recurrent Neurons & Layers
- At each time (frame), the neuron or layer takes both x_t at current time and output y_(t-1) from previous time point as input
- Memory: Output at every time is a function of all the inputs from previous times.
- Memory cell: a structure that preserve memory

## Input and Output of Sequences
- Seq2Seq example: input stock prices for the last N days, and output the prices shifted by 1 day
- Seq2Vec example: input a sequence of words reviewing a movie, and output the sentiment score
- Vec2seq example: input a image and output a sequence of words as caption
- Encoder-Decoder
    - Encoder: a seq2vec network
    - Decoder: a vec2seq network
    - Example: language translation. A sentence in a language input into an encoder and output a vector. A decoder takes the vector as input and output a sentence in another language.

## Training RNNs
- Unrolled the RNN and use backpropagation

## Forecasting single time step
- Input data shape (batch_size, time_steps, dimensionality)
- The target is the last the value (or vector) for each series
- The model performance can be compared with
    - Naive forcasting: simply using the last value as the prediction
    - A simple linear regression (1 dense layer with one neuron)
- Example code:
    ```Python
    model = tf.keras.models.Sequential([
        tf.keras.layers.SimpleRNN(20, return_sequences=True, input_shape=[None, 1]),
        tf.keras.layers.SimpleRNN(20),
        tf.keras.layers.Dense(1)
    ])
    ```

## Forecasting multiple time steps
- Two approaches that are not best
    - Repeat the single step prediction multiple times, each time using last time predition as the input.
    - Simply changing the output layer to multi-dimention like Dense(10)
- Better solution: using seq2seq model
    - The model predicts at every time step using feature values from previous steps
    - For each time step, the target is a sequence of value of a fixed length starting at the next time step
- Example code:
    ```Python
    model = tf.keras.models.Sequential([
        tf.keras.layers.SimpleRNN(20, return_sequences=True, input_shape=[None, 1]),
        tf.keras.layers.SimpleRNN(20, return_sequences=True),
        tf.keras.TimeDistributed(tf.keras.layers.Dense(10)) # Equivalent to tf.keras.layers.Dense(10)
    ])
    ```
- Special metrics are needed to evaluate the model: only the last prediction should be selected in the the evaluation
    ```Python
    def last_time_step_mse(Y_true, Y_pred):
        return tf.keras.metrics.mean_square_error(Y_true[:, -1], Y_pred[:, -1])

    optimizer = tf.keras.optimizers.Adam(lr=0.01)
    model.compile(loss="mse", optimizer=optimizer, metrics=[last_time_step_mse])
    ```
- MC Dropout to calculate confidence interval

## Long Sequences

### Unstable gradient problem
- Tricks that are harmful
    - non-saturating activation functions like ReLU, default using tanh.
    - Batch normalization; does not change at different time step
- Tricks that are helpful
    - Initialization (He, LeCun)
    - Faster Optimization
    - Dropout
        - use the `dropout` parameter for the input dropout
        - use the `recurrent_dropout` for the hidden status drop out for each time step.
    - Layer Normalization: Jimmy Lei Ba et al. 2016
        - Normalized across features for each time step
        - Need to be wrapped inside a keras cell like this
            ```Python
            class LNSimpleRNNCell(tf.keras.layers.layer):
                def __init__(self, units, activation="tanh", **kwargs):
                    super().__init__(**kwargs)
                    self.state_size = units
                    self.output_size = units
                    self.simple_rnn_cell = tf.keras.SimpleRNNCell(units, activation=None)
                    self.layer_norm = tf.keras.layers.LayerNormalization()
                    self.activation = tf.keras.activations.get(activation)

                def call(self, inputs, states):
                    outputs, new_states = self.simple_rnn_cell(inputs, states)
                    norm_outputs = self.activation(self.layer_norm(outputs))
                    return norm_outputs, [norm_outputs]

            model = tf.keras.models.Sequential([
                tf.keras.layers.RNN(LNSimpleRNNCell(20), return_sequences=True, input_shape=[None, 1]),
                tf.keras.layers.RNN(LNSimpleRNNCell(20), return_sequences=True),
                tf.keras.layers.TimeDistributed(keras.layers.Dense(20))
            ])
            ```

### Short-term memory problem
- LSTM: Long Short-Term Memory
    - Code example
        ```Python
        model = tf.keras.models.Sequential([
            tf.keras.layers.LSTM(20, return_sequences=True, input_shape=[None, 1])
            tf.keras.layers.LSTM(20, return_sequences=True)
            tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(10))
        ])
        ```
- GRU: Gated Recurrent Unit: `tf.keras.layers.GRU(20, return_sequences=True)`
- Adding 1D convolutional layer before GRU or LSTM
    - A layer of filters slide along the time dimension
    - Can be used to reduce the length of input into LSTM or GRU
    - Code example
        ```Python
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv1D(filters=20, kernel_size=4, strides=2, padding="causal", input_shape=[None, 1]),
            tf.keras.layers.GRU(20, return_sequences=True),
            tf.keras.layers.GRU(20, return_sequences=True),
            tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(10))
        ])
        ```
- WaveNet: tackling really long sequence
    - Aaron van den Oord et al, 2016
    - Stack 10 convolutional layers with dilation rates of 1, 2, 4, ..., 256, 512. Then stack another 10 convolutional same and yet another 10.