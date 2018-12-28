# How to use jupyter notebook/lab to run PySpark scripts

Personally, I don't recommand running PySpark using jupyter cells. It contains so many side effects that is hard to control when the program is deployed on a real cluster. But if when it is absolutely necessary. There are three approaches.

1. Using python package `findspark`: `import findspark; findspark.init()`.

2. Setup shell command alias as `alias pysparklab="export PYSPARK_DRIVER_PYTHON=jupyter; export PYSPARK_DRIVER_PYTHON_OPTS=lab; pyspark"` in the `.bashrc` or `.bash_profile`. However, since the `SparkSession` was created using the default configuration, it is sometimes not convinient since you have to be careful enough to either create new sessions or overwrite the existing configurations.

3. Setup path environment variable inside python script, e.g.

```
import sys
sys.path.append("/usr/local/spark/python")
sys.path.append("/usr/local/spark/python/lib/py4j-0.10.7-src.zip")

from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
```