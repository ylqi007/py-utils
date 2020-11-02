#!/usr/bin/env bash

# Create a softlink to dataset
DATA="/home/yq0033/work/PycharmProjects/DATA"

if [ ! -d DATA ]; then
  ln -s ${DATA} .
else
  echo "DATA/ already exists."
fi