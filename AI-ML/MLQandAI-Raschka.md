# Learning Note for the Book "Machine Learning Q and AI" by Sebastian Raschka

# Q1. Embeddings, Representations, and Latent Space

## Embeddings
- An embedding is a type of prepresentations.
- Similar items are close to each other.
- Encode high-dimentional data into low-dimentional vectors
- Examples
    - Transform an one-hot encoded inputs into a dense vector
        - user embedding in a recommender
        - word embedding (one-hot respective to the dictionary)
    - Any layer output of a neural network can be seen as an embedding.
        - Outputs of last layers of CNN
        - Outputs of bottleneck layers of Autoencoders
    - 2D embeddings used for visualizations.

## Latent Space
- Same as embedding sapce
- The space embedding vectors are in.

## Representations
- A general term
- Encoded form of input data
- Can contain trainable weights like embeddings, or simpler form like one-hot encoding

## Q1 Quiz
### 1A
- Q: Which neural network layers can be utilized to produce useful embeddings in a network similar to AlexNet?
- A: The last few fully connected layers.
### 1B
- Q: Name at least one type of input representation that is not an embedding.
- A: One-hot encoding.

# Q2. Self-supervised Learning

## When to use it v.s. not to use it
- When there is little labeled data
- Self-supervised learning task is also called pre-text tasks.
- Not useful nor neccessary for small neural network models

## Process
1. Create label from the dataset
2. Build a large scale model using the created label
3. Fine tuned the pretrained model on the target (downstream) task

## Alternative
- Transfer learning is an alternative to self-supervised learning
- The difference: the pretained model in transfer learning is a model trained on more general labeled data

## Types
### Self-prediction: Hide or change part of the input
- Examples
    - Transformer-based LLMs
        - Mask (next) words from text corpus and use the masked words as labels
    - Diffusion Autoencoders
        - Add noise to the image and train the model to remove the image
### Contrastive: train similarity embeddings
- Example: sample constractive siamese network
    1. Generate similar data from the original data.
        - Augment, corrupt, perturb the images to generate similar but different images
        - Examples of methods generating new images: Shifting, rotating, adding noises, changing light conditions
    2. Create label
        - Create tuple `(img1, img2, label)` from the original dataset. 
        - The `label=1` when the two images are similar, otherise 0.
    3. Model architecture
        1. Feed the network twice using `img1` and `img2`
        2. Combine the two outputs into a contrastive loss
    4. Use pretrained siamese network for the downstream task
### Further Reading
- Sample contrastive: https://arxiv.org/abs/2002.05709
- Dimension contrastive: https://arxiv.org/abs/2103.03230
- Siamese networks: https://builtin.com/machine-learning/siamese-network

## Q2 Quiz
### 2A
- Q: How could we apply self-supervised learning to video data?
- A: We can use self-prediction method. More specifically, we can mask some (next) frames and use them as labels.
### 2B
- Q: Can self-supervised learning be used for tabular data represented as rows and columns? If so, how can we approch this?
- A: We can use mask random feature values and use self-prediction.


