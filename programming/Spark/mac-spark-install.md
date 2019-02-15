# Set up Pyspark Environment on local Mac (OSX) machine

1. Uninstall too old or new version of Java:

    ```shell
    sudo rm -fr /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin
    sudo rm -fr /Library/PreferencePanes/JavaControlPanel.prefPane
    sudo rm -fr ~/Library/Application\ Support/Oracle/Java
    sudo rm -fr /Library/Java/JavaVirtualMachines/jdk1.8.0_144.jdk
    ```

2. Download and install JDK-8 using the graphical installer;

3. Install Spark

    1. Go to [website of Spark](https://spark.apache.org/) -> `Download` -> `Version`(e.g. 2.4.0) -> `download spark`, then copy the download link.
    
    2. Download: `wget https://www-us.apache.org/dist/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz`.
    
    3. Check the downloaded file
    
        1. Click `signatures and checksum`, then copy the link of `spark-2.4.0-bin-hadoop2.7.tgz.sha512`.
        
        2. Download the checksum file: `wget https://archive.apache.org/dist/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz.sha512`.
        
        3. Run the verification: `shasum -a 512 spark-2.4.0-bin-hadoop2.7.tgz` and compare with the `SHA512` line of `spark-2.4.0-bin-hadoop2.7.tgz.sha512`.
        
    4. Install Hadoop
    
        ```shell
        tar -xzvf spark-2.4.0-bin-hadoop2.7.tgz
        sudo mv spark-2.4.0-bin-hadoop2.7 /usr/local/spark
        ```

4. Change environment variables in `.bash_profile` and then `source .bash_profile`:

    ```shell
    # Added for Pyspark
    export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/
    export SPARK_HOME=$HOME/spark-2.3.1-bin-hadoop2.7
    export PYSPARK_PYTHON=$HOME/anaconda3/bin/python3
    export PYSPARK_DRIVER_PYTHON=$HOME/anaconda3/bin/ipython3
    alias pysparknote="export PYSPARK_DRIVER_PYTHON=jupyter; export PYSPARK_DRIVER_PYTHON_OPTS=lab; pyspark"
    export PATH=$SPARK_HOME/bin:$PATH
    ```

5. (Optional) Copy the log property template and change the log output settings, make `log4j.rootCategory=ERROR`

    ```bash
    cp $SPARK_HOME/conf/log4j.properties.template log4j.properties
    ```

This is equivalent to add the configuartion in the python script:

    ```python
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