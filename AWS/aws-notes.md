# Instructions and Notes on AWS

## Setup

1. Create IAM user and avoid using root access from now on. (Offical Doc)[https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html]

2. Download the .csv file at the last step and keep it at anywhere safe (dont' store it at cloud, `~/.ssh` is a good option).

3. Use the new console url for web UI and access keys for aws cli

    - A list of created user:
    
        1. Administrator: [Web UI URL](https://378857920884.signin.aws.amazon.com/console)

## EC2

[Offical Doc for EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)

1. To start an EC2 instances for the first time, better use the web UI:

    - create a security group with SSH protocals and `myIP` as the only IP
    
    - generate and download the .pem file for the SSH key

2. Change the permission of the .pem file `chmod 400 <file-name>.pem`

3. SSH to EC2 instance:
    
    - `ssh -i <key-pair-file>.pem ec2-user@<Public DNS (IPv4) from web UI>`
    
    - for example: `ssh -i /path/my-key-pair.pem ec2-user@ec2-198-51-100-1.compute-1.amazonaws.com`
    
    - [Offical Doc for connecting to EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)
    
4. Use aws cli to start an EC2 instance:
    
    - [Offical Doc - Deploying EC2](https://docs.aws.amazon.com/cli/latest/userguide/tutorial-ec2-ubuntu.html)

    
## AWS CLI

1. Installation on local: `pip install --upgrade awscli`

2. Configure aws cli using the info in `credentials.csv` (for me, saved in `~/.ssh/`: ``

