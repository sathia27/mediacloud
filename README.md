
## How to run the app
```.env
cd application-path
./run.sh
```

### Build and run via docker
```.env
 docker build -t songs:VERSION .
 docker run -p 5000:5000 songs:VERSION
```