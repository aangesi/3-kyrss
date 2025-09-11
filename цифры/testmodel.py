import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

img_height = 28
img_width = 28

model = tf.keras.models.load_model('my_model.keras')

def load_image(filepath, invert_colors=False):
    img = Image.open(filepath).convert('L')
    img = img.resize((img_width, img_height))
    img = np.array(img).astype(np.float32) / 255.0

    if invert_colors:
        img = 1.0 - img

    plt.imshow(img, cmap='gray')
    plt.title(f"Processed Image (invert_colors={invert_colors})")
    plt.axis('off')
    plt.show()

    img = img.reshape(1, img_height, img_width, 1)
    return img

def predict_digit(filepath, invert_colors=False):
    img = load_image(filepath, invert_colors)
    prediction = model.predict(img)
    digit = np.argmax(prediction)
    print(f"Распознанная цифра: {digit}")
    return digit

if __name__ == "__main__":
    filepath = r"test\2\17.png"

    print("\nПредсказание без инверсии цвета:")
    predict_digit(filepath, invert_colors=False)
