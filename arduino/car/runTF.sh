#!/bin/bash
cd ~/tensorflow
tensorflow/contrib/pi_examples/camera/gen/bin/camera | xargs -n1 flite -t
