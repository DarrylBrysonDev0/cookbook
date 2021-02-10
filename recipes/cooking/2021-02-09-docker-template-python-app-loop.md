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
  - Docker Image
  - docker-compose (deployment)
- Interface Classes
  - SFTP Server
  - Messaging Queue
- Python app
  - requirments.txt
  - Base script
