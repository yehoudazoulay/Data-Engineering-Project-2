# Tweets similarity program.
This program provides a web interface where the user can submit a text. The program will return the top20 tweets matching his query.

The program uses Elastich search engine to do the similarity scoring and it is able to process more than <b>10 000 queries per minute</b>.

To start the program run :

```console
sudo docker-compose up
```

The program will be running on port 5000 at this adress :

http://localhost:5000

Then you can close the program :

```console
sudo docker-compose down
```
