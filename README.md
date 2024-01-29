# link-api

## Overview
This is an API for the [Link](https://github.com/dvrpc/link) react app. 

It uses: 
* FastAPI
* Postgres (with PostGIS and PGrouting)
* DVRPC's [LTS/sidewalk connectivity tool.](https://github.com/dvrpc/LTS_island_connectivity) 
* ogr2ogr
 

## Setup/Installation

#### 1. Install dependencies, if not installed. For postgres with extensions, consider using
```shell
sudo apt install postgresql-15-pgrouting
```
which will install PostgreSQL, PostGIS, and PGrouting. If you have postgres already, you need to install the other two individually. Setup any roles you want.

You also need ogr2ogr. For Linux:
```shell
  sudo apt-get install gdal-bin
```

#### 2. Create an empty virtual environment
```shell
python -m venv ve
```
Then activate the environment. 
```shell
. ve/bin/activate
```

#### 3. Install the requirements with:
```shell 
pip install wheel && pip install -r requirements_base.txt
```

#### 4. Add a .env file 
Create a .env file at the root of the project. An example is below, which contains a URI to a database.
```
DB_URI=postgresql://user:pw@host:port/db
URL_ROOT="/api"
```

#### 5. Add config file for pg-data-etl
You also need to create a config file for pg-data-etl, which is used in the [LTS/sidewalk connectivity tool.](https://github.com/dvrpc/LTS_island_connectivity) 
This is just another file with your pg credentials. If your virtual environment is activated, you can use:
```shell
pg make-config-file
```
Then, edit the file (path will print to the terminal) and update your config settings.

#### 6. Import database backup
If you're putting this onto a remote server, you need to pipe a copy of the database from a machine that's behind the DVRPC firewall, as all of the data import and setup scripts can only be run behind the firewall, pulling from DVRPC's GIS postgres server.
The most recent backup can be found in 'G:\Shared drives\Bike LTS and Connectivity Analysis Webmap\Rethinking Connectivity\DB_Backups'. 

Pipe a copy in with:
```shell
psql -U your_username -h your_host -p your_port -d target_database < backup.sql  
```

## Usage
Start the development server with
```shell
cd app
uvicorn main:app --reload
```
See what API calls are supported by visiting [localhost:8000/api/docs](localhost:8000/docs). (Note that the "/api" part of the path here comes from the `URL_ROOT` var defined in the .env file.)

## License
The project uses the GPL 3.0 license.
