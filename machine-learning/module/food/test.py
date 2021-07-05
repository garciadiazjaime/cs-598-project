import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from prepare import get_images_folder, get_categories

img_size = 224

def restore_model(test_images, test_labels):
  path = "data/saved_model/food"
  if not os.path.isdir(path):
    return print("Restored model not found")

  model = tf.keras.models.load_model(path)

  # Evaluate the restored model
  loss, acc = model.evaluate(test_images, test_labels, verbose=2)
  print("----- RESTORED MODEL -----")
  print("Restored model, accuracy: {:5.2f}%\n".format(100 * acc))

  return model


def predict(model):
  if not model:
    return

  images = [
    ["https://urbanmatter.com/chicago/wp-content/uploads/2016/08/61658265_1031292940394672_2473784691572867072_o.jpg", "tacos"],
    ["https://cdn.vox-cdn.com/thumbor/dhIGCe8OGUK2YslVIcxYaW-QILQ=/0x0:1280x853/1200x900/filters:focal(538x325:742x529)/cdn.vox-cdn.com/uploads/chorus_image/image/63729432/taqueria_el_mezquite.0.jpg", "tacos"],
    
    ["https://s3-media0.fl.yelpcdn.com/bphoto/C1CConTCbLd9sRCUC2IOwA/ls.jpg", "pizza"],
    ["https://s3-media0.fl.yelpcdn.com/bphoto/XABBGCU0KSOS54IkHDfAlg/ls.jpg", "pizza"],
  ]

  for index in range(len(images)):
    [url, category] = images[index]
    path = tf.keras.utils.get_file(category + "_" + str(index), origin=url)

    img = tf.keras.preprocessing.image.load_img(
      path, target_size=(img_size, img_size)
    )

    # plt.figure()
    # plt.imshow(img)
    # plt.show()

    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) / 255.0 # Create a batch

    predictions = model.predict(img_array)
    print("----- PREDICTIONS -----")
    score = tf.nn.softmax(predictions[0])

    class_names = get_categories()
    print(
      "This image ({}) most likely belongs to *{}* with a {:.2f} percent confidence."
      .format(category, class_names[np.argmax(score)], 100 * np.max(score))
    )

def main():
  train_folder = get_images_folder()

  with open(train_folder + "/test_images.npy", "rb") as f:
    test_images = np.load(f)
  with open(train_folder + "/test_labels.npy", "rb") as f:
    test_labels = np.load(f)

  model = restore_model(test_images, test_labels)
  predict(model)



if __name__ == "__main__":
  main()
