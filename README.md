# connect-api

## Overview
This is an API for the [connect](https://github.com/dvrpc/connect) web map. It uses FastAPI and Postgres. It is still under development.

## Getting Started:
Create an empty virtual environment with 
```shell
> python -m venv ve
```
Then activate the environment. 
```shell
> . ve/bin/activate
```

Install the requirements with 
```shell 
> pip install -r requirements.txt
```
now that the environment is active. 

## Necessary parts
You'll need a .env file at the root of the project. An example is below.
```
SIGNATURE_KEY=12345678910ABCDEFGHIJKLMNOP
DB_URI=postgresql://user:pw@host:port/db
```

### Signature Key

A signature key is needed in order to sign/authenticate JSON web tokens.  

To generate one, use `openssl rand -hex 32` in the terminal, and drop the output into your .env file's signature key. 

This allows the app to sign tokens, ensuring their authenticity, and allowing us to authenticate users of the connect app.

### DB URI

A DB_URI is necessary to connect to the DB. 

## Development server
Start the development server with
```shell
> uvicorn main:app --reload
```

## To-do:
* Finish readme
* ~~build endpoint for OATH token generation~~
* properly hash passwords in user creation, tie together user creation and authentication functions
* add emails and email auth(?)
* alter oath endpoints to pull users and hashed pw's from database rather than fake db
* build endpoint for generic segment analysis
* build endpoints to retrieve segment, blob, isochrone, user data
* build endpoints to drop segments