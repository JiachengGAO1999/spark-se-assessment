web: flask db init; flask db migrate; flask db upgrade; gunicorn project.server:app
heroku ps:scale web=1
