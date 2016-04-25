# CS6310 Project 3

### Introduction

This repository includes the application components for Project 3. There are three major components:

* User-facing front end (`/src`)
* Back end API services for registration (`/api`)
* Gurobi components (solver and intermediate API) (`/optimizer`)

### Instructions for Use

The application can be accessed via its hosted versions (on Heroku and Amazon Web Services) with the information provided below or via a locally-deployed version. To access the local version, you must have Docker Compose installed and configured (the defaults should be sufficient). From the project root, run the following:
```
docker-compose up
```
You will then have a version of the application that can be accessed by going to `http://<your-docker-ip>/` with the front end and back end API services running locally. The optimizer service will still default to calling the AWS version as building a working Gurobi instance cannot be scripted due to licensing issues. To change this behavior, you can run the optimizer server API by running the `optimizer/server.py` script and changing the target URL in `api/controllers/solver.py`.

To load test data for the optimizer and user accounts, you can use the following command:

```
docker-compose exec web python import_test_data.py sample
```
This will load the sample data from Project 1 and allow the user to interact. The user accounts created have the same username as their Project 1 counterparts and each user's password is the username (e.g. `aberge1/aberge1`). An additional administrative user is created with the username and password of `aadmin3`. Additional loading options are in the `import_test_data.py` file for randomly generated data sets.

To access the remote, hosted version of the application, you can visit:
```
https://cryptic-beyond-81330.herokuapp.com
```