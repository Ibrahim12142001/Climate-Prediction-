# CMPT353 Climate Insights Project
## Project Description
Github repository for our project that focused on "Climate Insights: Predicting Temperatures with CO₂ and GDP". Here you will find all of our code, as well as our raw data files that we obtained from sources indicated in the report.

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
Or use the requirements.txt to pip install the Dependencies:
```
pip install -r requirements.txt
```
## Detailed Step On How To Run The Code
The code for this project can be divided into 3 separate categories
1. Data Processing
2. Statistical Tests
3. Machine Learning Model

### Data Processing
The data processing step takes in the raw data and applies ETL to obtain usable data for other steps. The project includes 4 different directories to handle raw data from each of the fields. The **Population Data** needs to be processed first since it is used to transform other datasets. The other directories can be processed in any order as long an all the raw data is processed before combining the data.

The exact sequence of files to run and in which order can be found below. The python files do not require any additional inputs. The input file paths are hard coded based on the structure in this repository.

The **0-ExtractData.py** in the weather section can take over an hour to run due to the API call limit and for the purpose of testing our model all the datasets have already been created so running the following python files is not mandatory to use the model.

**Population**
- 0-Extract_Data_And_Interpolation.py
- 1-Population_Density.py
- 2-State_and_Province_Population.py

**Emissions**
- 0-ExtractData.py
- 1-TransformData.py
- 1.1-TransformData_ML_Testing.py

**GDP_Data**
- 0-USA_GDP_per_capita.py
- 1-CanadaGDP_to_per_capita.py
- 2-Combine_US_Canada_GDP_Data.py

**Weather**
- 0-ExtractData.py
- 1-CombineData.py

The next step requires the output files from all the previous fields and should only be done after each of the previous fields data has been processed.

**Combining Data**
- 3-CombineAllData.py

At this point you will have 2 files called **Combined_Data.csv** and **Combined_Data_2011_2013.csv** which has the combined data from all the fields.

### Statistical Tests
The Statistical Tests require the **Combined_Data.csv** file from the previous steps. This file is used to conduct tests and produce plots on the results of those tests. In order to conduct the tests go to the **Statistical_Testing** directory and run the python files in the following order. The python files do not require any input files since the location for the Combined_Data.csv file is hard coded into them.

**Statistical Tests**
- 1-Linear_Test.py
- 1.1-Temp_Test.py
- 2-Relationship_Testing.py
- 2.1-Relation_Plots.py

### Machine Learning Model
The machine learning model is trained on the data from the years 2000-2010 and we test its predictive ablity using data for the next 3 years from 2011 to 2013. The code for training the model can be found in the directory called Machine_Learning.

Training the model can be a really long process so it is not recommended to train it yourself but if you do please remember the following:

Running **0-RegressionModelTesting.py** can take about 20 minutes

Running **1-HyperparameterTuning.py** can take over 8 hours

**Finding the best Model**
- 0-RegressionModelTesting.py
- 1-HyperparameterTuning.py

Running **2-FinalModelTraining.py** can also take about 20 minutes. This step can be done without running the **0-RegressionModelTesting.py and 1-HyperparameterTuning.py** files since we already did that and found the models to use and their parameters.

**Training the Model**
- 2-FinalModelTraining.py

In order to save time retraining the model we have already provided the trained model in the Machine_Learning directory that can be tested using the file below. This file will also produce the error plot used in the report.

**Testing**
- 3-FinalModelResults.py


