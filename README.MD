# Main Video Controller

### RESTful API for controlling and monitoring multiple Raspberry PI video nodes


_***Requirements & Dependencies:***_  

1. Install all packages listed in requirements.txt
2. Python 2.7.10
3. One or more Raspberry PIs on the network, each with the Node software installed and running.  

    _(To have automated scheduling running, the following must be installed and properly configured on the same server as this program.)_
4. RabbitMQ  
5. Celery
6. Redis

To start:  execute "python starter.py"  
To stop everything: execute "python shutdown_all.py"  

Starter.py will check that RabbitMQ, Celery and Redis are running, if they are not it will attempt to start them. 


The application can be run without automated scheduling by simply running run.py.  

_(It is assumed that there are one or more Raspberry PIs running and accessible over the network.  Furthermore, the Raspberry PIs have the corresponding Node application installed and running on them.
)_  

