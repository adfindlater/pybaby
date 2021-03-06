import tflite_runtime.interpreter as tflite
import numpy as np
import cv2

interpreter = tflite.Interpreter(
    model_path="/home/pi/Code/pyBaby/pybaby/data/model.tflite"
)

interpreter.allocate_tensors()

def inference(image):
    # Load the input image.
    # image_path = 'PATH_TO_YOUR_IMAGE'
    # image = tf.io.read_file(image_path)
    # image = tf.compat.v1.image.decode_jpeg(image)
    # image = tflite.expand_dims(image, axis=0)
    # Resize and pad the image to keep the aspect ratio and fit the expected size.
    # image = tflite.image.resize_with_pad(image, 192, 192)
    input_image = cv2.resize(image, (192, 192))
    input_image = input_image / 255.0
    input_image = np.expand_dims(input_image, axis=0).astype("uint8")

    # TF Lite format expects tensor type of float32.
    # input_image = tflite.cast(image, dtype=tflite.float32)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]["index"], input_image)

    interpreter.invoke()

    # Output is a [1, 1, 17, 3] numpy array.
    keypoints_with_scores = interpreter.get_tensor(output_details[0]["index"])

    return input_image, output_details, keypoints_with_scores
