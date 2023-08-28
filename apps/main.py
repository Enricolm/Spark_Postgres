from pathlib import Path
from pyspark.sql import SparkSession, functions as f
from datetime import datetime,timedelta
import yfinance
import pandas as ps
from os.path import join
from pathlib import Path
import sqlalchemy
import psycopg2

class extracao_finance():
    def __init__(self,path,start_date,end_date,ticker = "AAPL"):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.path = path
        self.spark = SparkSession\
            .builder\
            .appName("extracao_Finance")\
            .getOrCreate()
        super().__init__()


    def criando_pasta(self):
        (Path(self.path).parent).mkdir(exist_ok=True, parents=True)
    

    def extraindo_dados(self):
        dados_hist = yfinance.Ticker(ticker="AAPL").history(
            interval="1d",
            start=self.start_date,
            end= self.end_date,         
            prepost=True
        )

        dados_hist = dados_hist.reset_index()
        dados = self.spark.createDataFrame(dados_hist)

        dados = dados.drop('Stock Splits')

        dados = dados.withColumn("Open", f.round(f.col('Open'),2))
        dados = dados.withColumn("High", f.round(f.col('High'),2))
        dados = dados.withColumn("Low", f.round(f.col('Low'),2))
        dados = dados.withColumn("Close", f.round(f.col('Close'),2))
        dados = dados.withColumn("Date", f.split(f.col('Date'),' ')[0])

        self.dados = dados
        dados.show()
    def execute (self):

        self.criando_pasta()
        self.extraindo_dados()
        dados_pandas = self.dados.toPandas()

        postgres_conn = sqlalchemy.create_engine("postgresql://user1:postgres@spark_yfinance-db-1:5432/t_apple").connect()
        dados_pandas.to_sql("T_Apple", con = postgres_conn, index=False, if_exists="append")

if __name__ == "__main__":
    start_date= (datetime.now() - timedelta(days=240)).strftime('%Y-%m-%d')
    end_date= (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    Base_folder = join(Path('../'),
                    ('data/Data={date}'))
    extracao = extracao_finance(path=Base_folder.format(date=f'2023-08-08'), start_date=start_date, end_date=end_date)
    extracao.execute()
