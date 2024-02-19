1. AWS configuration  
Currently AWS secrets are missing, appropriate secrets handling should be added.
As a workaround, you can set following environment variables in Dockerfile.dev  
`ENV AWS_ACCESS_KEY_ID`  
`ENV AWS_SECRET_ACCESS_KEY`   
