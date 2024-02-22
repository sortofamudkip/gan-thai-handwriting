from tensorflow import keras

def create_classification_model(input_shape, num_classes, augmentation_layers:'function'=None):
    inputs = keras.Input(shape=input_shape)
    # * rescale the input
    x = keras.layers.Rescaling(1./255)(inputs)
    # * apply data augmentation
    if augmentation_layers:
        x = augmentation_layers(x)
    # * convolutional layers
    for filter_size, dropout_ratio in zip([32, 64, 128, 256], [0.1, 0.15, 0.2, 0.25]):
        x = keras.layers.Conv2D(filter_size, 5, activation='relu')(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.MaxPooling2D()(x)
        x = keras.layers.Dropout(dropout_ratio)(x)
    # * flatten layer
    x = keras.layers.Flatten()(x)
    # * fully connected layers
    x = keras.layers.Dense(512, activation='relu')(x)
    x = keras.layers.Dropout(0.5)(x)
    x = keras.layers.Dense(256, activation='relu')(x)
    # * output layer (softmax activation function for multiclass classification)
    outputs = keras.layers.Dense(num_classes, activation='softmax')(x)

    return keras.Model(inputs, outputs)
