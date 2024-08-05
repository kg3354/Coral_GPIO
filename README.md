# Edge TPU simple camera examples

This repo contains a example that use camera streams and GPIO 
together with the [TensorFlow Lite API](https://tensorflow.org/lite) with a
Coral device such as the
[USB Accelerator](https://coral.withgoogle.com/products/accelerator) or
[Dev Board](https://coral.withgoogle.com/products/dev-board) to achieve close-loop demo.

## Installation

1.  First, be sure you have completed the [setup instructions for your Coral
    device](https://coral.ai/docs/setup/). If it's been a while, repeat to be sure
    you have the latest software.

    Importantly, you should have the latest TensorFlow Lite runtime installed
    (as per the [Python quickstart](
    https://www.tensorflow.org/lite/guide/python)).
    
    This demo is tested using [Raspios arm64 bullseye](https://downloads.raspberrypi.com/raspios_arm64/images/raspios_arm64-2021-11-08/) on Pi 4

2.  Clone this Git repo onto your computer:

    ```
    git clone 
    
    cd 
    
    mkdir google-coral && cd google-coral

    git clone https://github.com/google-coral/examples-camera.git --depth 1
    ```

3.  Download the models:

    ```
    cd examples-camera

    sh download_models.sh
    ```

    These canned models will be downloaded and extracted to a new folder
    ```all_models```.

4.  Install the OpenCV libraries and GPIO library:
    
    ```
    cd ../..

    sh install_requirements.sh
    ```
