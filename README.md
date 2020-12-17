# MIE1628MoA
A Repo for Mechanism of Action competition on Kaggle for MIE1628: Big Data Science

This repo contains the following files:
* **[DataExploration-and-visulization.ipynb](DataExploration-and-visulization.ipynb)** (for submission): This notebook contains the code for visualization and data explorations.
* **[Model_1_to_3-LR_RF_GBT.ipynb](Model_1_to_3-LR_RF_GBT.ipynb)** (for submission): This notebook contains the code for the first pipeline (logistic regression), second pipeline (random forest), and the thrid pipeline (gradient boosting machine).
* **[Model_4-Challenger-Model.ipynb](Model_4-Challenger-Model.ipynb)** (for submission): This notebook contains the code for the fourth pipeline (random forest + logistic regression).
* **[MBE.csv](MBE.csv)** (for submission): This csv file contains the MBE loss for **ALL** four pipelines (tuned and untuned) that we attampted.
* **[scv.py](scv.py)** (for reference only): The stratified cross-validation Python module. This module is referenced by [Model_4-Challenger-Model.ipynb](Model_4-Challenger-Model.ipynb) notebook.
* Folder **[./misc](./misc)** (for reference only) contains our other attampts in terms of feature engineering and parallelization. These attampts were not adopted by any of the four models that we use for the final submission.