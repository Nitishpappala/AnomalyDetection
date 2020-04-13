# AnomalyDetection

System's main goal is to create machine learning models for anomaly detection on UAVs.
The system allows creation and loading of machine learning models by using dynamic inputs. 
Moreover, the system displays different output plots and evaluation metrics which compare between different models and the diagnosis of anomalies which were found.
Running the system with dynamic parameters will allow us to extract many different machine learning models.
Comparing them based on different evaluation metrics will lead to obtaining the best machine learning models for anomaly detection.
Those models will be used as a baseline for a real-time & light-weight anomaly detection algorithm based on streaming data from UAV sensors
in to order to get the earliest possible detection of GPS spoofing attacks on UAV’s.  

## Getting Started

First, you should clone the project to your local computer.
1. Run 'guiController.py' file in order to run the system.
2. Currently the flow of creating new model is working(load existing model will be available later).
3. Enter valid inputs for train,test and results directories.
4. Choose LSTM and edit the parameters in order to continue to next step in the system (LSTM is working, more algorithms will be available later).
5. Skip the next step (will be available later).
6. Choose cosine similarity function (optional).
7. Run new model.

### Prerequisites

You should run the command (before run the system) in the console

```
pip install -r requirements.txt
```

## Generated Machine Learning Models 

* LSTM - Long Short-Term Memory
* SVR - Support Vector Regression
* Random Forest
* ARIMA - Autoregressive Integrated Moving Average

| Algorithm | Description |
| -- | -- |
| LSTM | An artificial recurrent neural network (RNN) architecture used in the field of deep learning |
| SVR | A popular machine learning tool for classification and regression. |
| Random Forest | Are supervised ensemble-learning models used for classification and regression. |
| ARIMA | A statistical model for time series forecast and analysis. |

## Python Libraries

* [Keras](https://keras.io/) - The Python Deep Learning library.
* [Scikit-learn](https://scikit-learn.org/) - is an open source machine learning library that supports supervised and unsupervised learning.
* [statsmodel](https://www.statsmodels.org/) -  is a Python module that provides classes and functions for the estimation of many different statistical models, as well as for conducting statistical tests, and statistical data exploration.

## Data Sets

* ADS-B data sets - Automatic dependent surveillance – broadcast - data sets
* Simulated data sets - Data sets which are generated by a simulator

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - The Python IDE for Professional Developers
* [Flightradar24](https://www.flightradar24.com/) - ADS-B data sets

## Authors

* **Lior Pizman** - *Prototype initial work* - [Github](https://github.com/liorpizman/)
* **Yehuda Pashay** - *Prototype initial work* - [Github](https://github.com/yehudapashay)

See also the list of [contributors](https://github.com/liorpizman/AnomalyDetection/contributors) who participated in this project.

