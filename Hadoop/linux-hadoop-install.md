# How to install Hadoop in stand alone mode on a local linux machine (ubuntu 18.04)

1. Install Java

    ```shell
    sudo apt update # update package list
    sudo apt install default-jdk # install OpenJDK
    java -version # check java version
    ```
2. Install Hadoop

    1. Go to [website of hadoop](https://hadoop.apache.org/) -> `Download` -> `Version`(e.g. 3.1.1) -> `binary`, then copy the download link.
    
    2. Download: `wget https://www-us.apache.org/dist/hadoop/common/hadoop-3.1.1/hadoop-3.1.1.tar.gz`.
    
    3. Check the downloaded file
    
        1. Right click `checksum` next to the `binary`, then copy the link.
        
        2. Download the checksum file: `wget https://dist.apache.org/repos/dist/release/hadoop/common/hadoop-3.1.1/hadoop-3.1.1.tar.gz.mds`.
        
        3. Run the verification: `shasum -a 256 hadoop-3.1.1.tar.gz` and compare with the `SHA256` line of `hadoop-3.1.1.tar.gz.mds`.
        
    4. Install Hadoop
    
        ```shell
        tar -xzvf hadoop-3.1.1.tar.gz
        sudo mv hadoop-3.1.1 /usr/local/hadoop
        ```
        
    5. Configure Hadoop: add one line to `/usr/local/hadoop/etc/hadoop/hadoop-env.sh`: `export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/`.
    
3. Test Hadoop

    - Simple command: `/usr/local/hadoop/bin/hadoop`
    
    - Run a example MapReduce program
    
        ```shell
        mkdir ~/input
        cp /usr/local/hadoop/etc/hadoop/*.xml ~/input
        /usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.1.jar grep ~/input ~/grep_example 'allowed[.]*'
        cat ~/grep_example/*
        ```
    
4. References

[Reference](https://www.digitalocean.com/community/tutorials/how-to-install-hadoop-in-stand-alone-mode-on-ubuntu-18-04)