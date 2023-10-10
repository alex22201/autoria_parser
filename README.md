# Create  .env file
  DB_USERNAME=username\
  DB_PASSWORD=pass\
  DB_NAME=db\
  PGCLIENTENCODING=UTF8

# Build and run docker
  docker-compose build --no-cache --pull   
  docker-compose up                        
