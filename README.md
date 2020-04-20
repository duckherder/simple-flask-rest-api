# simple-flask-rest-api

### Introduction
Example in Python 3 of how to develop a REST API in flask. Useful for fast development of a microservice.

### Starting the service
Simply pip install flask or my personal preference is to make use of a virtual environment. With
Anaconda Python you can create a conda virtual environment and install the necessary package.

    conda create -n simple-flask
    conda activate simple-flask
    conda install flask
    
To start the web service that supports the REST API implemented in Flask (see important note at bottom of page first)

    python simple-flask-rest-api.py
    
If you wish to make your REST API available to other users on other PCs on a specific port...

    python simple-flask-rest-api.py --external --port 5001

Note that the Werkzeug web service provided with the flask Python package is **not**
recommended as a production-ready or secure server. Also note that you may need to open a
port on your firewall for others to access your microservice.

### Accessing the service
The service can be accessed using the command line tool 'curl' available in most Linux
distributions and Windows, or through packages such as cygwin.

To see if the service is up and running on your localhost and default port of 5000

    c:/> curl http://127.0.0.1:5000/simpleservice/api/v1.0/status
    OK
    
Now we can see a list of all records currently held by the service

    c:/> curl -X GET http://127.0.0.1:5000/simpleservice/api/v1.0/record
    []

The REST API has returned an empty JSON list because no records have been added so far.
So let's do that by sending a JSON file to the service using a POST request

    c:/> cat bob.json
    {
        "name": "bob",
        "address": "1 flask street"
    }
    c:/> curl -X POST -F "json=@bob.json" http://127.0.0.1:5000/simpleservice/api/v1.0/record
    OK

We could repeat this and add a second record to the service e.g. using tim.json. If we now query the service
we can see the two records that have been added.

    c:/> curl -X GET http://127.0.0.1:5000/simpleservice/api/v1.0/record
    [
      {
        "address": "1 flask street",
        "name": "bob"
      },
      {
        "address": "2 flask street",
        "name": "tim"
      }
    ]

We can update Bob's record using the PUT method by sending a modified JSON file

    c:/> cat bob.json
    {
        "name": "bob",
        "address": "4 flask street"
    }
    c:/> curl -X PUT -F "json=@bob.json" http://127.0.0.1:5000/simpleservice/api/v1.0/record
    OK

and we can get just that specific record by adding the name to the URL, if we so wish

    curl -X GET http://127.0.0.1:5000/simpleservice/api/v1.0/record/bob
    [
      {
        "address": "4 flask street",
        "name": "bob"
      }
    ]

Finally we can delete a record using the DELETE method with a URL parameter to tell the service which
record to delete

    c:/> curl -X DELETE http://127.0.0.1:5000/simpleservice/api/v1.0/record?name=tim

To shutdown the service gracefully and avoid using Ctrl-C on the running service

    c:/> curl -X POST http://127.0.0.1:5000/simpleservice/api/v1.0/shutdown

Tested on Windows 10 Pro with Anaconda 4.8.2, Python 3.8.2 and Flask 1.1.1. Also
Ubuntu 18.04, Python 2.7.17 and Flask 1.1.1.

**NOTE:** I have had issues with Avast (20.2.2401 - build 20.2.5130.570) behavioural shield reporting IDP.Generic issues with python.exe when running Flask. Recommendation to use Linux platforms rather than Windows.
