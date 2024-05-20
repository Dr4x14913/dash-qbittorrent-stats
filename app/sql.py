#! /usr/bin/python3
from sys import stderr
import mysql.connector
import os
import pandas as pd

class Sql:
    def __init__(self, DB_NAME, DB_HOST=os.getenv('MYSQL_HOST'), DB_USER=os.getenv("MYSQL_USER"), DB_PASS=os.getenv("MYSQL_PASSWORD"), DB_SOCKET=''):
        if DB_HOST is None: # Override host if not define .env file
            DB_HOST = 'db'
        try:
            if DB_SOCKET == '':
                self.mydb = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASS,
                    database=DB_NAME,
                    )
            else:
                self.mydb = mysql.connector.connect(
                    unix_socket=DB_SOCKET,
                    user=DB_USER,
                    password=DB_PASS,
                    database=DB_NAME,
                    )

        except Exception as e:
            print(f"Connection to database failed !\n{e}" , file=stderr)
            exit(1)

    def select_one(self, request, dictionary=False):
        """Execute an sql request on the chosen database and return the 1st result"""
        try:
            cursor = self.mydb.cursor(dictionary=dictionary)
            cursor.execute(request)
            result = cursor.fetchone()

        except mysql.connector.Error as e:
            error_msg = f"Sql request is:\n> {request}"
            print(error_msg, file=stderr)
            raise mysql.connector.Error(f"{e}:{error_msg}") from e
        return result

    def select(self, request, dictionary=False):
        """Execute an sql request on the chosen database and return the result"""
        try:
            cursor = self.mydb.cursor(dictionary=dictionary)
            cursor.execute(request)
            result = cursor.fetchall()

        except mysql.connector.Error as e:
            error_msg = f"Sql request is:\n> {request}"
            print(error_msg, file=stderr)
            raise mysql.connector.Error(f"{e}:{error_msg}") from e
        return result

    def select_to_df(self, request, cols=None):
        """Execute an sql request and return the result as a dataframe"""
        try:
            if cols is not None:
                lines  = self.select(request)
                df_res = pd.DataFrame(lines, columns=cols)
            else:
                lines  = self.select(request, dictionary=True)
                df_res = pd.DataFrame(lines)

        except mysql.connector.Error as e:
            error_msg = f"Sql request is:\n> {request}"
            print(error_msg, file=stderr)
            raise mysql.connector.Error(f"{e}:{error_msg}") from e
        return df_res

    def insert(self, request):
        """Execute an sql request on the chosen database and return the result"""
        try:
            cursor = self.mydb.cursor()
            cursor.execute(request)
            self.mydb.commit()
        except mysql.connector.Error as e:
            error_msg = f"Sql request is:\n> {request}"
            print(error_msg, file=stderr)
            raise mysql.connector.Error(f"{e}:{error_msg}") from e


    def close(self):
        self.mydb.close()
