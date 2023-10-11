# Create and setting .env file 
  POSTGRES_USER=username\
  POSTGRES_PASSWORD=password\
  POSTGRES_HOST=postgres\
  POSTGRES_PORT=5432\
  POSTGRES_DB=cars\
  POSTGRES_ENCODING=UTF8\
  TZ=Europe/Kiev
  
  ROOT_DIR=/parser_autoria
  
  LOG_MODE=INFO

# Build and run docker
  docker-compose build --no-cache --pull   
  docker-compose up                        
