Celery App

- Created virtual environment using
  python -m venv celery_env
- activate the virtual environment by running the following script
  celery_env/scripts/activate or celery_env/scripts/Activate.ps1
- Install the Dependency
  pip install -r /path/to/requirements.txt
- Run the Flask application
  python app.py
- Run the celery worer using the following command
  celery -A celery_worker.celery worker --loglevel=info
- Get the requirment file
  pip freeze >> requirements.txt
