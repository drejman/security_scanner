### 1. AWS configuration  
Currently AWS secrets are missing, appropriate secrets handling should be added.
As a workaround, you can set following environment variables in Dockerfile.dev  
`ENV AWS_ACCESS_KEY_ID`  
`ENV AWS_SECRET_ACCESS_KEY`   

### 2. Running the project  
`docker-compose -f docker/compose.dev.yml up --build -d`  
should be enough to get the containers running

### 3. Setup  
I run ngrok for public domain.  
Details about ngrok, django settings and slack configuration should be explained here.

### 4. Areas needing improvement 
- dependency injection
- interfaces / ports
- tests
- serialization of messages, interface checking
- logging
- bonus point
