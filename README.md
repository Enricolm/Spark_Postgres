# Spark_Postgres


# Conteiners que vão ser utilizados no projeto:

  * postgres: Postgres será o banco onde vamos salvar as informações já tratadas, criando para cada camada uma tabela
    * Image: postgres: latest
    * Database Port: 5432
   
  * spark-master: Será orquestrador de worker do Spark
    * image: apache-spark-image:3.3.2
    * Spark-master Ports: 8080 // 7070
   
  * spark-worker-N: aqui vc pode definir a quantidade de workers que desejar, basta copiar o conteiner do yaml e apenas trocar seu nome.
    * image: apache-spark-image:3.3.2
