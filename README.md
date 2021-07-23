# Setup Steps to Follow

1. First download the ssl certificate from this website 
```bash sslforfree.com```

2. Verify your domain by doing following procedure mention in the website.

3. Now, Update your nginx/default.conf and docker-compose.yml file acc. to your domain name.

4.Run this command to build your docker container
```bash 
docker-compose build
```
5. Run the command to run your docker in background.
```bash 
docker-compose up -d
```
3. Now you will see, there are two different container will start, now you can easily access your website.