#!/usr/bin/env bash

# Create a softlink to dataset
# DATA="/home/yq0033/work/PycharmProjects/DATA"

# Lab207 - 2080Ti
DATA="/home/yq0033/work/DATA/"
#if [ ! -d DATA ]; then
#  ln -s ${DATA} .
#else
#  echo "DATA/ already exists."
#fi
ls -al ${DATA}

# To test if symlink is broken (by seeing if it links to an existing file)
if [ ! -e "./DATA" ]; then
  echo "Broken symlink."
  rm "./DATA"
  ln -s ${DATA} .
  echo "New symlink is created."
else
  echo "./DATA/ already exists."
fi