from src.logger import logging
from src.exception import MyException

import sys
import numpy as  np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from src.utils import save_object
import os

@dataclass
class dataclasstransformation:
    preprocessor_obj_file_path=os.path.join('artifact','preprocessor.pkl')

class datatransformation:
    def __init__(self):
        self.datatranformationconfig=dataclasstransformation()
    
    def get_data_transformer_object(self):
        """this function is responsible for data transformation"""

        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline=Pipeline(
                steps=[
                ('simpleimputer',SimpleImputer(strategy='mean')),
                ('scaler',StandardScaler())]
            )

            cat_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('onehotencoder',OneHotEncoder()),
                ]
            )

            logging.info(f'Categorical columns:{categorical_columns}')
            logging.info(f'numerical columns:{numerical_columns}')

            preprocessor=ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_columns),
                    ('categorical_pipeline',cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor
        except Exception as e:
            raise MyException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info('read train and test data completed')
            logging.info('obtaining preprocessor obj')
            preprocessor_obj=self.get_data_transformer_object()
            target_col_name='math_score'

            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_col_name])
            target_feature_train_df=train_df[target_col_name]
            input_feature_test_df=test_df.drop(columns=[target_col_name])
            target_feature_test_df=test_df[target_col_name]

            logging.info(f'Applying preprocessing object on training dataframe and testing dataframe')

            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.fit_transform(input_feature_test_df)

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info(f'saved preprocessing object')

            save_object(
                file_path=self.datatranformationconfig.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            return(train_arr,test_arr,self.datatranformationconfig.preprocessor_obj_file_path)
        
        except Exception as e:
            raise MyException(e,sys)

