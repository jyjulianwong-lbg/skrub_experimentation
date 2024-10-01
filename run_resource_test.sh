#!/bin/bash

source /c/dev/virtual/skrub_experimentation/Scripts/activate

# TODO: Update value of CUSTOM_AUGMENT_TIMES.
python -m data_generator

docker build . -t skrub-experimentation:latest
docker run skrub-experimentation

deactivate