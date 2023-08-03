# Chapter 16 - Natural Language Processing with RNNs and Attention

## Stateless v.s. Stateful RNNs

### Stateless RNNs
- When training at each time step, the hidden states are initialized and trained from the beginning.
- Input instances can be overlapping sequences.
- Cannot learn long-term patterns

### Stateful RNNs
- When training at each time step, the hidden states from the previous time step is used to start training.
- Each input instance must be a sequence starting from the end of the sequence of the last instance.
- Can learn long-term patterns
- At the end of each epoch, the states needs to be reset.
- `stateful=True` in Keras RNN layers

## Sentiment Analysis
- Embedding layers are added to embed the words into vectors
- Pretrained embeded layers can be used

### Masking
- Can be setup in `keras.layers.Embedding(mask_zero=True)`, which mask the zero values
- The following layers automatically apply this mask tensor as long as it:
    - Supports masking: LSTM, GRU...
    - Outputs a sequence
- Alternatively, `keras.layers.Masking` can be used.
- Custom masking
    ```Python
    mask = tf.keras.layers.Lambda(lambda inputs: keras.backend.not_equal(inputs, 0))(inputs)
    z = tf.keras.layers.GRU(128, return_sequences=True)(z, mask=mask)
    ```

## Neural Machine Translation (Encoder-Decoder)
- Sentences in input language are reversed. It is to make sure the decoder sees the whole sentence before it start to translate it.
- Words are embeded first and fed into the encoder.
- Encoder output the vector to decoder.
- Decoder uses the translated target as input as well.
- Decoder has a time distributed softmax layer as output.
- At each time step, the decoder outpus a score for each word in the vocabulary.

### Bidirectional RNNs
- In solving translation problems, it is helpful to peak the future words of a sentence, unlike in the time series problems.
- Bidirectional RNN: two RNNs with outputs concatenated: one reading words from left to right, the other reverse.
- `keras.layers.Bidirectional(keras.layers.GRU(10, return_sequences=True))`

### Beam Search
- It keeps track of a list of the k most promising sentences. At each decoder step it tries to extend them by one word, then keeping only k most promising sentences.
- k is called the beam width
- When comparing the probability of each possible sentence, conditional probabilities are multiplied.
- Encoder-Decoder models do not need to be retrained, simply used in a better way.

## Attention Mechanisms

### Concatenate Attention
- Dzmitry Bahdanau et al, 2014
- Model structure
    1. All hidden states input into an alignment model (attention layer)
    2. At each time step in decoder, the alignment model outputs a vector of weights with the same length of the number of the encoder time steps (which is the same with the current input sentence)
    3. The weighted sum of the encoder output hidden state vector (based on the weight created by the alignment model) input into the decoder at this time step.
    4. Alignment model structure
        - Layers: TimeDistributed(Dense(1)) -> Softmax layer
        - Input: decoder hidden layer from previous time step concatenated with the outputs from encoder
        - Output: weights that sum up to one, with the same length as the inputs

### Multiplicative Attention
- Minh-Thang Luong et al, 2015
- Replace the alignment model with simply the dot product of (1) the previous time step decoder hidden states and (2) encoder's output. Then let it go through a softmax layer.
- The encoder's output can optionally go through a linear transformation (a time distributed dense layer without a bias term) before the dot product.
- A variant approach is to use decoder hidden states of the the current time step instead of the previous one

## Visual Attention
- Used in adding caption to images.
- Weight matrices on the feature maps can be used to highlight the area which leads to the current word in generated caption.

## Transformer Attention (Attention is All You Need)
- Vaswani et al, Google, 2017

### Postional Embedding
- A word in position i is emdeded using sin and cos function
- The embedded postion is added to the word embedding

### Scaled Dot-Product Attention
- Embeded input sentences input into 3 dense layers with trainable weight kernels: W_Q, W_K, W_V and output matrices Query Q, Key K, Value V.
- Dot product of Q and K (transposed) is scaled by the sqrt(key-dimension) to avoid saturating the softmax function
- The result above is fed into a softmax function and then the output vector is multiplied by the matrix V.
- For decoder, use `casual=True` mode to mask later words
- `keras.layers.Attention(use_scale=True, casual=False)`

### Multi-Head Attention
- Instead of just having 3 dense layers, multiply it H times to 3xH layers with 3xH trainable weight kernels.
- The outputs for each scaled dot-product attention are concatenated
- `keras.layers.MultiHeadAttention`