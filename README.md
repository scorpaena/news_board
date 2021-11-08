## News_board
This is a simple news board API which has been made as a test task.  
Tools that have been used for the app development: Django/DRF, Postgres, Docker.  
To start working on the app do the following steps:
1. Run migrations: `docker-compose run --rm web python ./news_board/manage.py migrate`.
2. Create superuser: `docker-compose run --rm web python ./news_board/manage.py createsuperuser`.  
Anonymous user can only see post and comments. To add post or comment, or to upvote the post user has to be logged in. Number of upvotes for each post is shown on post list/detail view.  
[Link to deployment on Heroku](https://lit-taiga-04438.herokuapp.com/api/)  
[Link to video of how it works locally](https://photos.app.goo.gl/dixd77LiqfatoFDh9)
