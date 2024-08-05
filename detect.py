import argparse
import cv2
import os
import RPi.GPIO as GPIO

GPIO_PINS = [13, 19, 26] # The pins are subject to change

# Setup
GPIO.setmode(GPIO.BCM) 
for pin in GPIO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Ensure all pins are initially off

from picamera2 import Picamera2
from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

def main():
    # Set default values for model, labels, and other parameters
    default_model_dir = './google-coral/examples-camera/all_models'
    default_model = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
    default_labels = 'coco_labels.txt'

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='.tflite model path',
                        default=os.path.join(default_model_dir, default_model))
    parser.add_argument('--labels', help='label file path',
                        default=os.path.join(default_model_dir, default_labels))
    parser.add_argument('--top_k', type=int, default=3,
                        help='number of categories with highest score to display')
    parser.add_argument('--threshold', type=float, default=0.1,
                        help='classifier score threshold')
    args = parser.parse_args()

    # Load the model and labels
    print(f'Loading {args.model} with {args.labels}.')
    interpreter = make_interpreter(args.model)
    interpreter.allocate_tensors()
    labels = read_label_file(args.labels)
    inference_size = input_size(interpreter)

    # Initialize Picamera2
    picam2 = Picamera2()
    picam2.start()

    print('Press Ctrl+C to exit.')
    try:
        while True:
            # Capture a frame
            frame = picam2.capture_array()

            # Convert to RGB for processing
            cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the RGB frame
            cv2_im_rgb_resized = cv2.resize(cv2_im_rgb, inference_size)
            run_inference(interpreter, cv2_im_rgb_resized.tobytes())
            objs = get_objects(interpreter, args.threshold)[:args.top_k]
            countHuman = sum(1 for obj in objs if obj.id==0)
            GPIO.output(GPIO_PINS[0], GPIO.HIGH if countHuman == 0 else GPIO.LOW)
            GPIO.output(GPIO_PINS[1], GPIO.HIGH if countHuman == 1 else GPIO.LOW)
            GPIO.output(GPIO_PINS[2], GPIO.HIGH if countHuman  > 1 else GPIO.LOW)

            # Append detection results to the RGB frame
            processed_frame_rgb = append_objs_to_img(cv2_im_rgb, inference_size, objs, labels)

            # Convert processed RGB frame back to BGR for OpenCV display
            processed_frame_bgr = cv2.cvtColor(processed_frame_rgb, cv2.COLOR_RGB2BGR)

            # Display all frames
            cv2.imshow('Original BGR Frame', frame)  # Raw BGR frame
            cv2.imshow('Processed Frame (BGR)', processed_frame_bgr)  # Processed BGR frame
            cv2.imshow('Processed Frame (RGB)', processed_frame_rgb)  # Processed RGB frame

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        [GPIO.output(pin, GPIO.LOW) for pin in GPIO_PINS]
        GPIO.cleanup()
        picam2.close()
        cv2.destroyAllWindows()

def append_objs_to_img(cv2_im, inference_size, objs, labels):
    height, width, channels = cv2_im.shape
    scale_x, scale_y = width / inference_size[0], height / inference_size[1]
    for obj in objs:
        print(labels.get(obj.id, obj.id))
        bbox = obj.bbox.scale(scale_x, scale_y)
        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)

        percent = int(100 * obj.score)
        label = f'{percent}% {labels.get(obj.id, obj.id)}'

        cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2_im = cv2.putText(cv2_im, label, (x0, y0 + 30),
                             cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
    return cv2_im

if __name__ == '__main__':
    main()
