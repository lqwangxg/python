### run docker-compose for start a service 
#docker-compose up -d

docker run -it -p 8000:8000 -v $(pwd)/go:/go lqwangxg/goloangci sh  

