#!/bin/bash

# Capturez l'image
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
raspistill -o  "/home/thibault/webcampics/static/images/image_${DATE}.jpg"
