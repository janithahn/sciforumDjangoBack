# Django Backend for the project sciForum.

**sciForum** is a faculty based online discussion forum. This is the **back-end** part of the application and is based on `Django`. The **front-end** and the **main overview** of the application can be found [here](https://github.com/s16417/sciforum).

## Overview
All the back-end tasks for the **sciForum** are handled by this part of the main application. `Celery` and `Redis`(as a message broker) have been used for automated tasks like sending daily emails. 

## Databases
- `MySQL` as the main database.
- `MongoDB` for the web crawler.
- `Firebase Realtime Database` for the chat application. 
