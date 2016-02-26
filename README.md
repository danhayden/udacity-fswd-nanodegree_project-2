## Tournament Results

Udacity Nanodegree: Full Stack Developer (Project 2)


## How to run

Before you begin ensure you have the following installed:

* VirtualBox
* Vagrant
* Git

#### Clone & start the virtual machine

    vagrant up

This will also run the `config.sh` script which will create the `tournament` database.


#### SSH into the machine

    vagrant ssh


#### Move to the correct directory

    cd /vagrant/tournament


#### Run tests

    python tournament_test.py
