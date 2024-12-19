# Mini-service on FastAPI 

>**Goal:** To develop a small asynchronous web application based on FastAPI, which will interact with external APIs, perform CRUD operations with database, and also use multithreading/multitasking capabilities to speed up some operations. 

As external api was used https://dummyjson.com

## Installation

>Before installation is better to use virtual environment

To install app use your package manager **PDM**, **Poetry**... If you don't have any one, 
use the following command `pip install -e .`

## Usage

> Before usage, you must create your ENV file based on .env.example

To run the app use the command 
`python -m uvicorn main:app --host 0.0.0.0 --port 8000 --env-file=.env`


## Testing

> Testing also require ENV file

To test just run `python -m pytest`