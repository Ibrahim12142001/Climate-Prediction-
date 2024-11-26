# CMPT353 Climate Change Project
## Project Description

## Python Dependencies
Please pip install the following before running the code:
1. pip install openmeteo-requests
2. pip install requests-cache
3. pip install pandas
4. pip install retry-requests
5. pip install matplotlib
6. pip install openpyxl
7. pip install xlrd

Or use the requirement.txt to pip install the Dependencies:

**pip install -r requirements.txt**

## Detailed Step On How To Run The Code
The code for this project can be divided into 3 seperate catagories
1. Data Processing
2. Statistical Tests
3. Machine Learning Model

### Data Processing
The data processing step takes in the raw data and applies ETL to obtain usable data for other steps. The project includes 5 different dirrectories to handle raw data from each fields. The data in these directories can be processed in any order as long an all the raw data is processed before combining the data.

The exact sequence of files to run and in which order can be found below. The python files do not require any additional inputs. The input file paths are hard coded based on this reposotorys.

**Climate_Change**
- 0-ExtractData.py
- 1-CombineData.py

**Emissions**
- 0-ExtractData.py
- 1-TransformData.py

**GDP_Data**
- 0-USA_GDP_per_capita.py
- 1-CanadaGDP_to_per_capita.py
- 2-Combine_US_Canada_GDP_Data.py

**Population**
- 0-Extract_Data_And_Interpolation.py
- 1-Population_Density.py

**Weather**
- 0-ExtractData.py
- 1-CombineData.py

The next step requires the output files from all the previous fields and should only be done after each of the previous fields data has been processed.

**Combining Data**
- 3-CombineAllData.py

At this point you will have a file called **Combined_Data.csv** which has the combined data from all the fields.

### Statistical Tests
The Statistical Test require the **Combined_Data.csv** file from the previous steps. This file is used to conduct test and produce plots on the results of these tests. In order to conduct the test go to the **Statistical_Testing** directory and run the python files in the following order. The python file do not require any input files since the location for the Combined_Data.csv file is hard coded into them.

**Statistical Tests**
- 1-Linear_Test.py
- 1.1-Temp_Test.py
- 2-Relationship_Testing.py
- 2.1-Relation_Plots.py

### Machine Learning Model
### Testing
