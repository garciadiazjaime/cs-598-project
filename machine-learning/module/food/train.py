import os
import numpy as np

import tensorflow as tf

from model import create_model
from prepare import get_images_folder


def main():
  image_folder = get_images_folder()

  ############# Loading images #############
  with open(image_folder + "/train_images.npy", "rb") as f:
    train_images = np.load(f)
  with open(image_folder + "/train_labels.npy", "rb") as f:
    train_labels = np.load(f)
  with open(image_folder + "/test_images.npy", "rb") as f:
    test_images = np.load(f)
  with open(image_folder + "/test_labels.npy", "rb") as f:
    test_labels = np.load(f)


  ############# Define a model #############

  # Create a basic model instance
  model = create_model()

  # Display the model's architecture
  model.summary()


  ############# Save checkpoints during training #############
  folder = "data/food/checkpoints"
  if not os.path.exists(folder):
    os.makedirs(folder)

  checkpoint_path = folder + "/cp-{epoch:04d}.ckpt"

  batch_size = 32

  # Create a callback that saves the model's weights every 5 epochs
  cp_callback = tf.keras.callbacks.ModelCheckpoint(
      filepath=checkpoint_path, 
      verbose=1, 
      save_weights_only=True,
      save_freq=5*batch_size)

  # Save the weights using the `checkpoint_path` format
  model.save_weights(checkpoint_path.format(epoch=0))

  epochs = 30

  # Train the model with the new callback
  model.fit(train_images, 
            train_labels,
            epochs=epochs, 
            batch_size=batch_size, 
            callbacks=[cp_callback],
            validation_data=(test_images, test_labels),
            verbose=1)


  ############# Save model #############
  folder = "data/saved_model"
  if not os.path.exists(folder):
    os.makedirs(folder)

  model.save('data/saved_model/food')



if __name__ == "__main__":
  main()
