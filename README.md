01_data_generation.ipynb contains the script for data generation.
The data for training is stored in data -> processed in "xfoil_dataset_rows.csv".
"xfoil_polars.csv" and "xfoil_runs_index.csv" are not important for training.
Raw data (.txt) is stored in data -> raw (-> polars).

02_model_architecture.ipynb contains the script for the model architectures.
Four different models are used: SmallNet, MediumNet, DeepNet and DropoutNet.
Data for training is saved as "data_for_training.npz" in data -> processed.
The model information from this script is saved as "model_info.npy" in data -> processed.

02_model_training.ipynb contains the script for the model training.
This script uses data generated from "02_model_architecture.ipynb".
The weights for the trained models with the loss curves (plots as PNG files) are stored in data -> processed -> trained_models.

03_evaluation.ipynb contains the script for evaluating the neural network.
It plots the aerodynamic polars via neural network output.
The plots as well as the data of the plots (.csv) are saved in reports -> evaluation_plots.
Caution: the plots need to be deleted manually once generated.
This script was used for the presentation.

03_evaluation_modified.ipynb is the new version of 03_evaluation.ipynb.
The figures of the plots are saved in reports -> evaluation_plots.
If there are plots in the folder already, the old ones are replaced by the new ones.

04_generate_original_polars.ipynb contains the script for generating data of unknown polars, which are not contained in the training data.
The data (.csv) is stored in data -> processed -> original_polars.

outdated_02_training.ipynb is an outdated script for training the model architectures.

Important note: The project should be placed in %USERPROFILE%\PyCharmMiscProject or $HOME\PyCharmMiscProject in order to work.

Furthermore, XFOIL (6.99) needs to be installed and the folder "XFOIL6.99" needs to be placed in one of the following paths:
- $HOME\Downloads
- $HOME\Desktop
- $HOME\Documents
- C:\XFOIL
- C:\XFOIL6.99
- C:\Program Files
- C:\Program Files (x86)

Link for XFOIL installation: https://web.mit.edu/drela/Public/web/xfoil/

In the "src" folder there is the list "requirements.txt" with all the packages needed for this project.
These packages need to be installed via terminal with the command "py -m pip install -r requirements.txt".

Note that for this project, the NACA guidelines are NOT considered.
There are some NACA airfoils in the data that do not adhere to the NACA guidelines.