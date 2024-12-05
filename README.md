# CMPT353 Climate Change Project
## Project Description

## Recommended Python Version
We recommend using the latest version of Python which at this time is 3.13.1

## Git LFS Warning
This repo contains some files that were uploaded via Git LFS, and so you probably need to run `git lfs install` before pulling it!

## Python Dependencies
Please pip install the following before running the code:
```
pip install openmeteo-requests
pip install requests-cache
pip install pandas
pip install retry-requests
pip install matplotlib
pip install openpyxl
pip install xlrd
pip install scikit-learn
pip install seaborn
```
Or use the requirement.txt to pip install the Dependencies:
```
pip install -r requirements.txt
```
## Detailed Step On How To Run The Code
The code for this project can be divided into 3 seperate catagories
1. Data Processing
2. Statistical Tests
3. Machine Learning Model

### Data Processing
The data processing step takes in the raw data and applies ETL to obtain usable data for other steps. The project includes 4 different directories to handle raw data from each fields. The data in these directories can be processed in any order as long an all the raw data is processed before combining the data.

The exact sequence of files to run and in which order can be found below. The python files do not require any additional inputs. The input file paths are hard coded based on this reposotorys.

The **0-ExtractData.py** in the weather section can take over an hour to run due to the API call limit and for the purpose of testing our model all the dataset have already been created so running the following python file is not mandatory to use the model.

**Emissions**
- 0-ExtractData.py
- 1-TransformData.py
- 1.1-TransformData_ML_Testing.py

**GDP_Data**
- 0-USA_GDP_per_capita.py
- 1-CanadaGDP_to_per_capita.py
- 2-Combine_US_Canada_GDP_Data.py

**Population**
- 0-Extract_Data_And_Interpolation.py
- 1-Population_Density.py
- 2-State_and_Province_Population.py

**Weather**
- 0-ExtractData.py
- 1-CombineData.py

The next step requires the output files from all the previous fields and should only be done after each of the previous fields data has been processed.

**Combining Data**
- 3-CombineAllData.py

At this point you will have 2 files called **Combined_Data.csv** and **Combined_Data_2011_2013.csv** which has the combined data from all the fields.

### Statistical Tests
The Statistical Test require the **Combined_Data.csv** file from the previous steps. This file is used to conduct test and produce plots on the results of these tests. In order to conduct the test go to the **Statistical_Testing** directory and run the python files in the following order. The python file do not require any input files since the location for the Combined_Data.csv file is hard coded into them.

**Statistical Tests**
- 1-Linear_Test.py
- 1.1-Temp_Test.py
- 2-Relationship_Testing.py
- 2.1-Relation_Plots.py

### Machine Learning Model
The machine learning model is trained on the data from the years 2000-2010 and we test its predictive ablity useing data for 3 years from 2011 to 2013. The code for training the model can be found in the directory called Machine_Learning.

Training the model can be a really long process so it is not recommended to train it yourselfs but if you do please remember the following:

Running **0-RegressionModelTesting.py** can take about 20 minutes

Running **1-HyperparameterTuning.py** can take over 8 hours

**Finding the best Model**
- 0-RegressionModelTesting.py
- 1-HyperparameterTuning.py

Running **2-FinalModelTraining.py** can also take about 20 minutes. This step can be done without running the **0-RegressionModelTesting.py and 1-HyperparameterTuning.py** since we already did that and found the models to use and there parameters.

**Training the Model**
- 2-FinalModelTraining.py

In the order to save time retraining the model we have provided the trained model that can be tested using the file below.
**Testing**
- 3-FinalModelResults.py


