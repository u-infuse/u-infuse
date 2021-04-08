# U-Infuse

## Available Object Detection Frameworks
* RetinaNet

## U-Infuse App Installation

#### Windows
* Go to releases page to download the Windows installation wizard and follow the prompts (Ignore security warning).

#### Universal Installer on Centos Systems:
 * Download modules.zip and build_universal_install_u-infuse1.30.sh
 * Make a directory called U_Infuse and then put the downloaded files into it
 * Open a cmd window and go into U_Infuse using cmd cd U_Infuse
 * Run the cmd sh ./build_universal_install_u-infuse.sh (you may have to authenticate first, e.g. setproxy, then put in your username and password)
 * The message "U-Infuse has been installed. Please run main.py in the modules directory to launch U-Infuse." should show up if it has installed correctly
 * Change into the modules dir using the cmd: cd modules
 * Run the cmd: python3 main.py
 * Done! U-Infuse should now be ready to use.
 
 ## Using the Jupyter Notebooks
  1. Install keras-retinanet by following the instructions on https://github.com/fizyr/keras-retinanet
  2. Git clone this repository
  3. Place your images in the datasets directory
  4. Place the corresponding annotations (if you have them) in the annotations directory
  5. Download the single_class_annotator (here), and place it in RetinaNet/pretrained_models/
  6. Download the pretrainedCOCO.h5 file (here), and place it in RetinaNet/pretrained_models/
  7. To train a custom object detector, use the U-Infuse RetinaNet Preprocessing and Training Jupyter Notebook 
  8. Once training is complete, go to the U-Infuse RetinaNet Preview Custom Models Jupyter Notebook to select and export your model
  9. You can then use your model for inference/object detection by using the U-Infuse RetinaNet Run Object Detection and Generate Reports Jupyter Notebook
  10. If you do not have annotated images, you can auto-annotate your images using the U-Infuse RetinaNet Auto-annotator Jupyter Notebook
  11. If you wish to edit the annotations, download and use labelImg (https://github.com/tzutalin/labelImg)
  12. Once annotations are complete, follow steps 7-9
  
## Sample Workflow
<img width="3967" alt="u_infuse" src="https://user-images.githubusercontent.com/39542635/113983774-ab7f7600-988d-11eb-9271-15f45c6a51c5.png">
