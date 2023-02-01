# Chapter 14 - Deep Computer Vision Using Convolutional Neural Networks
I found the way CNN was explained in this chapter is confusing. So I referred to other materials and summarized my understanding.

## Properties of Convolutional NN
- Largely reduced the number of parameters compared to dense NN
- Still requires a large amount of RAMs during training. Some tricks to try if out-of-memory error is encountered:
    - Reduce the size of mini-batch
    - Increase stride to reduce the size of feature maps
    - Use 16-bit floats instead of 32-bit
    - Distribute computing

## Elements of a Convolutional Neural Networks

### Input
- Inputs are usually 3D tensors with shapes (height, width, channels). For example, a RGB picture can be represented by a tensor with 3 channels.
- A mini-batch of inputs is of shape (mini-batch size, height, width, channels)

### Filters and Feature Maps
- A **filter** is a 2D matrix with trainable values and arbitrary shape (`kernel_size`).
- A filter is multiplied with a rolling rectangle called **receptive field** on the input matrix.
- Each time the filter is rolled and multiplied with a receptive field, the output is a numeric value (result of matrix multiplication).
- The outputs consist of output values are called **feature maps**.
- Features maps are possibly the input for the next convolutional layer.
- The sizes of the output feature maps are determined by both the size of input feature maps and the rolling fashion of the filter. The rolling fashion is controlled by `strides` and `padding`.
    - `strides` determines the number of indices to move forward every time the filter rolls. For example, `strides=2` means the filter skips 1 element when it moves along both the height and width; `stride=(2,3)` means strides along the height and width are 2 and 3, respectively.
    - `padding` determines if zero values are added to the edge of the input matrix whenever needed. `padding="same"` means to add zero pads, `padding="valid"` means no zero pads.
    - When `strides=1` and `padding="same"`, the input and output are of the same size.

### Convolutional Layers
- A convolutional layer is consist of multiple filters with the same sizes.
- Using the "neural" concept, each neuron is a position on the output feature map, and connected to the neurons within the receptive field from all the feature maps from the previous layers. The weight matrix is the filter matrix.
- Each filter is trained indepedently.

## Pooling Layers
- A **pooling kernel** is a kernel with NO weights. It only aggregates the values on the input feature maps.
- Example: Max Pooling Layer: only the maximumn value in the receptive field from feature maps of the previous layer makes it to the next layer.
- Inserted every few convolutional layers.
- Pros
    - Reduce the size of data, parameters, RAM usage.
    - Prevent overfitting, adding invariance.
    - Good for task like classification when the details of images are not as important.
- Cons
    - Loss of details of information
    - Not recommended for tasks like semantic segmentation when details are needed.
- Max pooling is preferred most of the time.
- Depthwise pooling: aggregate the values on the last dimension, i.e., across channels / feature maps.
- Global average pooling: simply output the average of the entire input feature map. In other words, the filter size is the same with the feature map.

## Keras Implementation
- 2D convolutional layer: `conv = tf.keras.layers.Conv2D(filters=32, kernel_size=3, strides=1, padding="same", activation="relu")`
- Max pooling layer: `max_pool = tf.keras.layers.MaxPool2D(pool_size=2)`
- Avg pooling layer: `avg_pool = tf.keras.layers.AvgPool2D(pool_size=2)`
- Depthwise max pooling:
    ```Python
    kernel_size = 3 # must be a divisor of the input depth
    strides_value = 3
    output = tf.nn.max_pool(images, ksize=(1,1,1,kernel_size), strides=(1,1,1,strides_value), padding="valid")

    # Wrap the layer in Lambda function to be used in tf.keras
    depth_pool = tf.keras.layers.Lambda(lambda X: tf.nn.max_pool(images, ksize=(1,1,1,kernel_size), strides=(1,1,1,strides_value), padding="valid"))
    ```
- Global average pooling: `global_avg_pool = keras.layers.GlobalAvgPool2D()`

## CNN Architectures
- A typical convolutional neural network
    1. Starts with a layer with a relative large convolutional kernel + ReLU (5x5 or 7x7), optionally with stride>=2 if the input is large.
    2. Followed by several small convolutional layers + ReLU (3x3)
    3. Add a pooling layer
    4. Repeat 1-3 several times
    5. Finish with some fully connected layers

### Famous Architectures
1. LeNet-5: Yann LeCun et al, "Gradient-Based Learning Applied to Document Recogonition", 1998
    - Each convolutional layer is followed by a average pooling layer
2. Alex Krizhevsky et al, "ImageNet Classification with Deep Convolutional Neural Networks", 2012
    - Stack convolutional layers directly together without pooling layer in between
    - Reduce overfitting
        - 2 dropout layers with 50% rate
        - Data Augmentation: make the model "custom" to the variantions
    - Data Augmentation: generate more variants of the exisiting images
        - The modifications should be learnable (not white noise)
        - Example: shrinking, rotating, flipping, changing lighting conditions
    - Local response normalization (LRN): an output on the feature maps are normalized with its neighbors on the same map. Effectively, making the largest output dominate the neighor. `tf.nn.local_response_normalization()`
    - ZF Net is a variant of AlexNet with tweaked hyperparameters
3. GoogLeNet
    - Inception module: a module with 3 layers of bottleneck convolutional layer and normal convolutioal layer and concatenate them
    - Bottleneck convolutional layer: a layer with 1x1 filter, only process depthwise pattern.
    - Deep combinations of convolution, max pooling, local reponse, and inception modules.
4. VGGNet: a simple architecture with 2 or 3 convolutional layers and repeat
5. ResNet: Kaiming He et al 2015
    - Deeper but with fewer parameters
    - skip (shortcut) connection
        - The input of a layer is also added to the output of a later layer: h(x)+x
        - The model is forced to learn H(x)-x instead of h(x), thus the name residual learning
        - It is faster because most of the time the target is close to indentity function
        - Residual Unit (RU): a module with skip connection
        - ResNet: a stack of residual units
    - When the size of the feature maps change, inputs cannot be added directly. It must go through a bottleneck convolutional layer with a 1x1 filter.
6. Xception: Francois Chollet 2016
    - Depthwise separable convolution layer: spatial only filters (one for each input feature map) -> a layer with many 1x1 filters.
    - Stack the spatial and depthwise filters instead of contatenate them as in GoogLeNet (inception modules)
    - Should be considered as default, generally better than inception modules
7. SENet: Squeeze-and-Excitation Network, Jie Hu et al 2017
    - Boost the Inception (SE-Inception) and ResNet (SE-ResNet) using SE block
    - SE block is a small network with input from the unit (inception or ResNet), and multiply the output to the unit output as the final output.
    - Structure of SE block: global avg pooling -> dense(ReLU) -> Dense(Sigmoid)
    - Global avg pooling generate a average value for each input feature maps, and then squeezed by the ReLU dense layer into a shorter vector, and then recalibrated back to the original dimension by the sigmoid dense layer, but with a fixed range (0,1)
- Keras Pretrained model `model = tf.keras.applications.resnet50.ResNet50(weights="imagenet")`

## Problems of Different Types

### Localization
- Localization of an object in images: predicting a bounding box around the object. In other words, prediting the horizontal and vertical coordinates of the object's center, as well as it's height and width. It can be interpreted as a vector regression problem with 4 elements.
- Add an output layer to CNN with 4 units, on top of the global pooling layer.
- Using MSE loss
- Using Intersection over Union (IoU) as the evaluation metric
    - Between the predicted area and the labeled area, the IoU is defined as the ratio of 1) area of interaction of the 2 and 2) area of union fo the 2. `tf.keras.metrics.MeanIoU`
- Bounding boxes must be added manually on the images. It can be crowdsourced or labeled by some tools.
- Bounding boxes coordinates, height, width should be normalized
- Common data shape (images, (class labels, (coordinates_norm, sqrt(hight_norm), sqrt(width_norm))))
- Example in Tensorflow
    ```Python
    base_model = tf.keras.applications.xception.Xception(weights="imagenet", include_top=False)
    avg = tf.keras.layers.GlobalAveragePooling2D()(base_model.output)
    loc_output = tf.keras.layers.Dense(4)(avg)
    model = tf.keras.Model(inputs=base_model.input, outputs=[class_output, loc_output])
    model.compile(loss=["sparse_categorical_crossentropy", "mse"], loss_weight=[0.8, 0.2], optimizer=optimizer, metrics=["accuracy"])
    ```

### Object Detection (localization for multiple objects)
- Old fashioned and straight-forward way: slide a window to detect the same image many times, and then aggregate the results.
- Fully Convolutional Networks (FCN)
    - Jonathan Long et al 2015
    - Replace the top dense layers with convolutional layers
    - filter size is the same with previous feature map size
    - When the new image is a larger image than the training images, the output multiplies, each grid representing a section of the large image. It's like running CNN several times on the large image.
- YOLO (You Only Look Once)
    - Joseph Redmon et al, 2015, 2016, 2018
    - Difference with FCN
        - On each grid of the output, there are 5 instead of 1 bounding boxes with objectness scores
        - The coordinate is relative to each grid, not the whole image.
        - Anchor box
        - Trained using images of different scales
    - An implementation: https://github.com/zzh8829/yolov3-tf2
- Other achitectures
    - SSD (single shot detector)
    - Faster-RCNN
- Metric for Object Detection
    - mAP: mean Average Precision for the object classfication
        - In binary classification, sometimes both precision and recall can increase when
        - For a list of recalls: 0%, 10%, ... 100%, calculate the maximum precision for each case, then average them to get the average precision.
        - For multi-class problem, calculate the mean of the average precision: mAP.
    - Location metric
        - One approach, define a success only of the IoU is greater than some threshold like 0.5
        - Alternatively, calculate the mean of mAP across a list of threshold of IoU.

### Semantic Segmentation
- Each pixel needs to be classified so the areas of classified objects can be identified, instead of bounding boxes.
- Fully Convolutional Networks can solve this problem.
    - Upsamping to solve the output too coarse problem.
    - Transposed convolutional layer as an upsampling technique `tf.keras.Conv2DTranspose`
    - Strides is a factor of streching the input in this case.
    - After the transposed layer, add skip connections to recover lost details
    - Super-resolution: upsampling to a larget output than the input

### Instance Segmentation
- Each object in the area are separated.
- Mask R-CNN 2017