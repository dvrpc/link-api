# connect-api

## Overview
This is an API for the [connect](https://github.com/dvrpc/connect) react app. 

It uses: 
* FastAPI
* Postgres (with PostGIS and PGrouting)
* DVRPC's [LTS/sidewalk connectivity tool.](https://github.com/dvrpc/LTS_island_connectivity) 
 

## Setup/Installation

#### 1. Create an empty virtual environment
```shell
python -m venv ve
```
Then activate the environment. 
```shell
. ve/bin/activate
```

#### 2. Install the requirements with:
```shell 
pip install -r requirements.txt
```

#### 3. Add a .env file 
Create a .env file at the root of the project. An example is below, which contains a URI to a database.
```
DB_URI=postgresql://user:pw@host:port/db
```


## Usage
Start the development server with
```shell
uvicorn main:app --reload
```
See what API calls are supported by visiting [localhost:8000/docs](localhost:8000/docs).

## License
The project uses the GPL 3.0 license.
