FROM kennethreitz/pipenv

COPY . /app

# -- Replace with the correct path to your app's main executable

CMD gunicorn -k gevent -w 5 --bind 0.0.0.0:5000 --reload --reload-extra-file ./knowledgebase kernel:app