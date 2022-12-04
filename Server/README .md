# SIRS

In order to run the server, you must execute the following commands:\
    - _export FLASK_APP=app_\
    - _export FLASK_ENV=development_\
    - _flask run --host=10.0.2.15_

Besides that, it is needed to add the following port forwarding rule to the server NAT Network:\
    -_&emsp; Rule 2 &emsp; TCP &emsp; 127.0.0.1 &emsp; 5000 &emsp; 10.0.2.15 &emsp; 5000_