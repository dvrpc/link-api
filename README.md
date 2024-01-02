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
pip install wheel && pip install -r requirements.txt
```

#### 3. Add a .env file 
Create a .env file at the root of the project. An example is below, which contains a URI to a database.
```
DB_URI=postgresql://user:pw@host:port/db
```

#### 4. Add config file for pg-data-etl
You also need to create a config file for pg-data-etl, which is used in the [LTS/sidewalk connectivity tool.](https://github.com/dvrpc/LTS_island_connectivity) 
This is just another file with your pg credentials. If your virtual environment is activated, you can use:
```shell
pg make-config-file
```

#### 5. Import database backup
If you're putting this onto a remote server, you need to pipe a copy of the database from a machine that's behind the DVRPC firewall, as all of the data import and setup scripts can only be run behind the firewall, pulling from DVRPC's GIS postgres server.
The most recent backup can be found in 'G:\Shared drives\Bike LTS and Connectivity Analysis Webmap\Rethinking Connectivity\DB_Backups'. 

Pipe a copy in with:
```shell
psql -U your_username -h your_host -p your_port -d target_database < backup.sql  
```

## Usage
Start the development server with
```shell
uvicorn main:app --reload
```
See what API calls are supported by visiting [localhost:8000/docs](localhost:8000/docs).

## License
The project uses the GPL 3.0 license.
