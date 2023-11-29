import sys
import logging
import pymysql
import json
import pandas as pd


class data_generation:
    def __init__(self, rds_host, port, user_name, password, db_name, table_name=False):
        self.rds_host = rds_host
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.table = table_name
        self.port = port

    # connect to database and run query
    def insert_data(self, cin_condition):
        if 'insert' in cin_condition.lower():
            query = F'''   INSERT INTO {self.db_name}.{self.table}(description, qr_path, flag) 
                        VALUES (%s, %s, %s)'''
            return query, cin_condition

    def read_data(self, cin_condition):
        if 'read' in cin_condition.lower() or 'get' in cin_condition.lower():
            query = f'''SELECT * From {self.db_name}.{self.table}'''
            return query, cin_condition

    def modify_data(self, cin_condition, search_condition):
        if 'modify' in cin_condition.lower() or 'get' in cin_condition.lower():
            query = f'''UPDATE {search_condition[0]}
                    SET column1 = value1, column2 = value2...., columnN = valueN
                    WHERE [condition];'''
            return query, cin_condition

    def get_first(self, cin_condition):
        if 'new' in cin_condition.lower():
            query = f'''select description from {self.db_name}.{self.table}'''
            return query, cin_condition
    def connect(self, query, df=False):
        data = []
        if isinstance(df, list):
            print(1)
            data = df
        else:
            data.append(df)
        print(data)
        try:
            query1 = query[0]
            condition = query[1]
            connection = pymysql.connect(user=self.user_name, password=self.password, host=self.rds_host,
                                         port=self.port, database=self.db_name, connect_timeout=15)
            print('connecting...')
            cursor = connection.cursor()
            select_Query = f'''{query1}'''
            # action to databse
            if 'insert' in condition:
                print('inserting...')
                cursor.executemany(select_Query, data)
                connection.commit()
                return 'insert success'
            elif 'get' in condition or 'read' in condition:
                cursor.execute(select_Query)
                records = cursor.fetchall()
                list_data = [list(x) for x in records]
                return list_data
            if 'new' in condition:
                cursor.execute(select_Query)
                records = cursor.fetchall()
                list_data = [list(x) for x in records]
                return list_data

        except pymysql.Error as error:
            print("Error while fetching data sql", error)
        finally:
            # closing database connection.
            try:
                if connection:
                    cursor.close()
                    connection.close()
            except Exception as e:
                print(e)


