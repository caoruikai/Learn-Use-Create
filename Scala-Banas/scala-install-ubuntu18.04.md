# Install Scala 2.12.8 on Ubuntu 18.04

Given that OpenJDK 8 was installed, run the following commands to install Scala 2.12.8:

```shell
sudo apt-get remove scala-library scala
sudo wget www.scala-lang.org/files/archive/scala-2.12.8.deb
sudo dpkg -i scala-2.12.8.deb
```
