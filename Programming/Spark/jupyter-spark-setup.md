# How to use jupyter notebook/lab to run PySpark scripts

Personally, I don't recommand running PySpark using jupyter cells. It contains so many side effects that is hard to control when the program is deployed on a real cluster. But if when it is absolutely necessary. There are two approaches.

1. Using python package `findspark`: `import findspark; findspark.init()`.

2. Setup shell command alias as `alias pysparklab="export PYSPARK_DRIVER_PYTHON=jupyter; export PYSPARK_DRIVER_PYTHON_OPTS=lab; pyspark"` in the `.bashrc` or `.bash_profile`. However, since the `SparkSession` was created using the default configuration, it is sometimes not convinient since you have to be careful enough to either create new sessions or overwrite the existing configurations.