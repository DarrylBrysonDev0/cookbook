---
title: "Docker Template: Python App Looped Execution"
date: 2021-02-08T10:00:00
categories:
  - templates
tags:
  - templates
  - python
  - docker
excerpt: "Docker Template w/ Docker: Looped execution of python app as a microservice"
---
# Docker Template: Python App Looped Execution
## Overview
This article describes the a template for executing a docker python application with microservice interfaces enabled ***[Include article link 2021-02-08]***. This template is suitable for both batch and always-on use cases. Project

## Template Components
- Docker stack file (docker-compose)
  - [Docker Image](https://github.com/DarrylBrysonDev0/project-templates/blob/python-app-docker-loop/Docker/Python/python-app-loop/app-image/Dockerfile.python-app-loop)
  - [docker-compose (deployment)](https://github.com/DarrylBrysonDev0/project-templates/blob/python-app-docker-loop/Docker/Python/python-app-loop/docker-compose.python-app-loop.yml)
- Interface Classes
  - [SFTP Server](https://github.com/DarrylBrysonDev0/project-templates/blob/python-app-docker-loop/Docker/Python/microservice-interface-class-information.md)
  - [Messaging Queue](https://github.com/DarrylBrysonDev0/project-templates/blob/python-app-docker-loop/Docker/Python/microservice-interface-class-information.md)
- Python app
  - [requirements.txt](https://github.com/DarrylBrysonDev0/project-templates/tree/python-app-docker-loop/Docker/Python/python-app-loop/app-image/requirements.txt)
  - [Script Boilerplate](https://github.com/DarrylBrysonDev0/project-templates/tree/python-app-docker-loop/Docker/Python/python-app-loop/app-image/python-app-loop.py)
