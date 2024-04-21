#! /usr/bin/python3
import os
import mysql.connector
import pandas as pd
from sys import stderr

class Sql:
    def __init__(self, DB_NAME, DB_HOST='db', DB_SOCKET='', DB_USER=os.getenv('MYSQL_USER') , DB_PASS=os.getenv('MYSQL_PASSWORD') ):
        try:
            if DB_HOST != '':
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
            print("Connection to database failed !\n" + DB_NAME + f" is probably not a valid database...\n{e}", file=stderr)
            exit(1)

    def select(self, request):
        """Execute an sql request on the chosen database and return the result"""
        try:
            cursor = self.mydb.cursor()
            cursor.execute(request)
            result = cursor.fetchall()

        except mysql.connector.Error as e:
            error_msg = f"Sql request is:\n> {request}"
            print(error_msg, file=stderr)
            raise mysql.connector.Error(f"{e}:{error_msg}") from e
        return result

    def select_to_df(self, request, cols):
        """Execute an sql request and return the result as a dataframe"""
        try:
            lines = self.select(request)
            df_res = pd.DataFrame(lines, columns=cols)
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
