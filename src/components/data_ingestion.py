from src.logger import logging
import os

from src.exception import MyException

import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
import sys
from data_transformation import datatransformation
from model_trainer import ModelTrainer

@dataclass
class Data_ingestion_config:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=Data_ingestion_config()

    def initiate_data_ingestion(self):
        logging.info('into the data ingestion method or component')
        try:
            df=pd.read_csv('data/stud.csv')
            logging.info('read the data successfully')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info('train test initialized')

            train_set,test_set=train_test_split(df,test_size=0.2,random_state=45)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('performed the test split successfully')

            return(self.ingestion_config.train_data_path,self.ingestion_config.test_data_path)


        except Exception as e:
            logging.error('error occurred ')
            raise MyException(e,sys) 
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    Datatransformation=datatransformation()
    train_arr,test_arr,_=Datatransformation.initiate_data_transformation(train_data,test_data)
    
    modeltrainer= ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))