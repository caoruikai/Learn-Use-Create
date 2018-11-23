# Set up Pyspark Environment on local linux-like machine

A pyspark program on a local machine needs to find 4 things: `java` location, `pyspark` location, `spark` location, `python` used for the driver node

1. Download and untar spark: `tar xvf spark-2.3.1-bin-hadoop2.7.tgz`;

2. Uninstall too old or new version of Java:

```shell
sudo rm -fr /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin
sudo rm -fr /Library/PreferencePanes/JavaControlPanel.prefPane
sudo rm -fr ~/Library/Application\ Support/Oracle/Java
sudo rm -fr /Library/Java/JavaVirtualMachines/jdk1.8.0_144.jdk
```

4. Download and install JDK-8 using the graphical installer;

5. Change environment variables in `.bash_profile` and then `source .bash_profile`:

```shell
# Added to use the installed Java
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/
export PATH=$JAVA_HOME:$PATH

# Added for Pyspark
export SPARK_HOME=$HOME/spark-2.3.1-bin-hadoop2.7
export PYSPARK_PYTHON=$HOME/anaconda3/envs/spark/bin/python3
export PYSPARK_DRIVER_PYTHON=$HOME/anaconda3/envs/spark/bin/ipython3
alias pysparknote="export PYSPARK_DRIVER_PYTHON=jupyter; export PYSPARK_DRIVER_PYTHON_OPTS=lab; pyspark"
export PATH=$SPARK_HOME:$PATH
```

6. Copy the log property template and change the log output settings, make `log4j.rootCategory=ERROR`

```bash
cp $SPARK_HOME/conf/log4j.properties.template log4j.properties
```

This is equivalent to add the configuartion in the python script:

```python
sc = spark.sparkContext
sc.setLogLevel('ERROR')
```

7. Activate conda env by `source activate spark`, open `pyspark` shell and test Spark with the following (or try the jupyter notebook alias by `pysparknote`):

```python
# Start pyspark via provided command
import pyspark
# Below code is Spark 2+
spark = pyspark.sql.SparkSession.builder.appName('test').getOrCreate()
spark.range(10).collect()
```

8. Install ipykernel of `spark` conda environment for the jupyter:

```shell
source activate spark
python -m ipykernel install --user --name spark --display-name "Python 3 (spark)"
```

9. Download and install Pycharm;

10. Create a project with interpreter `~/anaconda3/envs/spark/bin/python` and create a first python script to run:

```python
# Start pyspark via provided command
import pyspark
# Below code is Spark 2+
spark = pyspark.sql.SparkSession.builder.appName('test').getOrCreate()
print(spark.range(10).collect())
```

11. Create a runtime configuration for the script: change the interpreter to the spark one and add the script path;