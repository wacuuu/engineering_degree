# Engineering Project for my degree
-----------------------------------


This repo is a port from two other repos that served me during preparing the project for my degree. I do not port history, because as you will see it would have both some private and API keys I don't want to share.

------------------------------------
## Overview

Let's start with full title of my thesis: Scalable and reliable deployment of distributed application with different IaaS providers. The idea is to make a PoC app, that would be then deployed to some public cloud for testing. At least some good practices should be shown during the process. App should be written in manner allowing scaling, CD and have at least basic set of metrics.

App was developed with use case in mind. It was meant to be a distributed database with CRUD over RESTfull API. Infra(because i was working o IaaS), was supposed to be automated and kept as a code.

-------------------------------------
## Tech stack

#### App

For db I used Casssandra, as it natively distributes well between clouds and DCs. Crud written in Python 3 with cassandra-driver(using object mappers), shared via API in Flask. This was wrapped in gunicorn, and via socket in nginx.

#### Monitoring

For monitoring I used Elasticseearch combined with Metricbeat and Kibana. 

#### Scaling

As I wanted to show different approaches, I used Digital Ocean and GCE. As DO doesn't have native scaling, I've prepared my own based on metrics from Elastic and Python. On GCE i have bash scripts that configure autoscaling.

#### Infra as code
Packer using proper cloud provider with Ansible.

------------------------------------
## How to run this

If you are interested in running this, here is what you would have to do more or less:

#### DO
First, images. You would have to fill proper access token in packer.json and pick proper images. Also add ssh keys in proper place. Using build.sh (combined with proper service name, like db, api, monitoring etc.) you would have built images. Then fill those in config in DO deployment dir, and simply run deploy.py assuming you have needed libraries. This should setup whole service with scaling. Keep in mind, that loadbalancer will be also created.

#### GCE
Same as DO, you have to make images first. Then edit scripts in templates dir under GCE deployment dir. Run those scripts. You now have instance templates that will be used in starting service. Then simply run deploy.sh. This will create managed instances groups, setup loadbalancer and all needed security groups.

---------------------------------
## Final thoughts

#### Code separation
During development code was split between two repos: infra and db. This is due to good practices, that app should be handled separately from infra. If you try to deploy this, remember that some services clone code from app repo on init.

#### Platform agnostic
App is meant to be platform agnostic, which means you don't need to change the codebase to make it work at any public cloud provider. However it may be needed from infra point of view, because some other CLI tools would be needed on instances.

#### Commentary
I am aware that this is not a top notch production ready setup. It was never meant to be one. For example service discovery(via DNS for example) is lacking from this project. Feel free to rise any meaningful comments via issues, I will do my best to respond.

---------------------------------
### Legal note
Use this as you wish, however before you start, let me know.
