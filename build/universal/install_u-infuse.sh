#!/bin/bash
# Author: Chris Lawson
# Contact: clawso21@une.edu.au
# Source: U-Infuse
# Purpose: U-Infuse universal installer.

# Create directories.
echo "U-Infuse installer requires: TensorFlow 1.14.x - 1.15.x, git and unzip."

read -p "Press enter to continue."

echo "Creating datasets directory."
if [ -d "datasets" ]; then
	echo "datasets directory already exists. Skipping."
else
	mkdir datasets
	echo "Created directory: datasets"
fi

echo "Creating annotations directory."
if [ -d "annotations" ]; then
	echo "annotations directory already exists. Skipping."
else
	mkdir annotations
	echo "Created directory: annotations"
fi

echo "Creating reports directory."
if [ -d "reports" ]; then
	echo "reports directory already exists. Skipping."
else
	mkdir reports
	echo "Created directory: reports"
fi

echo "Creating modules directory."
if [ -d "modules" ]; then
	echo "modules directory already exists. Skipping."
else
	mkdir modules
	echo "Created directory: modules"
fi

echo "Creating snapshots directory."
if [ -d "modules/snapshots" ]; then
	echo "modules/snapshots directory already exists. Skipping."
else
	mkdir modules/snapshots
	echo "Created directory: modules/snapshots"
fi

echo "Creating modules/pretrained_models directory."
if [ -d "modules/pretrained_models" ]; then
	echo "modules/pretrained_models directory already exists. Skipping."
else
	mkdir modules/pretrained_models
	echo "Created directory: modules/pretrained_models"
fi

# Unzip modules to modules directory.
unzip modules.zip -d modules

# Install PySide2
pyside2_out=$(pip3 show PySide2)
if echo "not found" | grep -q "$pyside2_out"; then
	echo "PySide2 not installed. Installing..."
	pip3 install --user PySide2

else
	echo "PySide2 is already installed"
fi

# Install PyQt5
pyqt5_out=$(pip3 show PyQt5)
if echo "not found" | grep -q "$pyqt5_out"; then
	echo "PyQt5 is not installed. Installing..."
	pip3 install --user PyQt5==5.14.0
else
	echo "PyQt5 is already installed"
fi

# Install QImage2ndArray
qimage2ndarray_out=$(pip3 show qimage2ndarray)
if echo "not found" | grep -q "$qimage2ndarray_out"; then
	echo "QImage2ndarray is not installed. Installing..."
	pip3 install --user qimage2ndarray
else
	echo "QImage2ndArray is already installed"
fi

# Install json2table
json2table_out=$(pip3 show json2table)
if echo "not found" | grep -q "$json2table_out"; then
	echo "json2table is not installed. Installing..."
	pip3 install --user json2table
else
	echo "json2table is already installed"
fi

# Install scikit-build
scikit_out=$(pip3 show scikit-build)
if echo "not found" | grep -q "$scikit_out"; then
	echo "scikit-build is not installed. Installing..."
	pip3 install --user scikit-build
else
	echo "scikit-build is already installed"
fi

# Install cmake
cmake_out=$(pip3 show cmake)
if echo "not found" | grep -q "$cmake_out"; then
	echo "cmake is not installed. Installing..."
	pip3 install --user cmake
else
	echo "cmake is already installed"
fi

# Clone RetinaNet
echo "Cloning RetinaNet repository"
git clone https://github.com/fizyr/keras-retinanet.git modules/keras-retinanet

# Change to repository dir
cd modules/keras-retinanet

# Install RetinaNet requirements
echo "Installing RetinaNet requirements"
pip3 install --user .

# Install pip packages required by RetinaNet
echo "Building RetinaNet"
python3 setup.py build_ext --inplace

# Install keras 2.3.1
pip3 install --user keras==2.3.1

# Go back to root of U-Infuse directory
cd -

# Move run script to root of U-Infuse directory
mv modules/u-infuse.sh u-infuse.sh

# Run U-Infuse
sh ./u-infuse.sh
