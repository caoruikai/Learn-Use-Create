# How to install Spark in stand alone mode for a local linux machine (ubuntu 18.04)

1. Install Java

    ```shell
    sudo apt update # update package list
    sudo apt install default-jdk # install OpenJDK
    java -version # check java version
    ```

2. Install Scala

   ```shell
   sudo apt-get remove scala-library scala
   sudo wget www.scala-lang.org/files/archive/scala-2.12.8.deb
   sudo dpkg -i scala-2.12.8.deb
   ```

3. Install Spark

    1. Go to [website of Spark](https://spark.apache.org/) -> `Download` -> `Version`(e.g. 2.4.3) -> `download spark`, then copy the download link.

    2. Download: `wget https://www-us.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz`.

    3. Check the downloaded file

        1. Click `signatures and checksum`, then copy the link of `spark-2.4.3-bin-hadoop2.7.tgz.sha512`.

        2. Download the checksum file: `wget https://archive.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz.sha512`.

        3. Run the verification: `shasum -a 512 spark-2.4.3-bin-hadoop2.7.tgz` and compare with the `SHA512` line of `spark-2.4.3-bin-hadoop2.7.tgz.sha512`.

    4. Install Spark

        ```shell
        tar -xzvf spark-2.4.3-bin-hadoop2.7.tgz
        sudo mv spark-2.4.3-bin-hadoop2.7 /usr/local/spark
        ```

4. Configure Spark by adding the following lines in `~/.bashrc` and then `source ~/.bashrc`:

    ```shell
    export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
    export SPARK_HOME=/usr/local/spark
    export PYSPARK_PYTHON=$HOME/anaconda3/bin/python3
    export PYSPARK_DRIVER_PYTHON=$HOME/anaconda3/bin/ipython3
    alias pysparklab="export PYSPARK_DRIVER_PYTHON=jupyter; export PYSPARK_DRIVER_PYTHON_OPTS=lab; pyspark"
    export PATH=$SPARK_HOME/bin:$PATH
    ```

5. (Optional) Copy the log property template and change the log output settings, make `log4j.rootCategory=ERROR`

    ```bash
    cp $SPARK_HOME/conf/log4j.properties.template log4j.properties
    ```

    This is equivalent to add the configuartion in the python script:

    ```Python
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')
    ```

6. Test PySpark by `spark-submit` the following script:

    ```python
    # Start pyspark via provided command
    import pyspark
    # Below code is Spark 2+
    spark = pyspark.sql.SparkSession.builder.appName('test').getOrCreate()
    print(spark.range(10).collect())
    ```
