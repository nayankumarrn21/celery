from celery import Celery
from celery.schedules import crontab
import plotly.graph_objects as go
import plotly.io as pio

celery = Celery('tasks', broker='redis://localhost:6379/0')

celery.conf.update(
    result_backend='redis://localhost:6379/0',
    timezone='UTC', 
)

@celery.task(bind=True, max_retries=3, default_retry_delay=10, soft_time_limit=60)
def generate_plot(self, plot_data):
    try:
        fig = go.Figure(data=go.Scatter(x=plot_data['x'], y=plot_data['y'], mode='lines'))
        
        plot_filename = f"{plot_data['task_id']}_plot.png"
        file_path = os.path.join(OUTPUT_DIR, plot_filename)
        
        fig.write_image(file_path)
        
        return {'status': 'success', 'file_path': file_path}
    except SoftTimeLimitExceeded:
        raise self.retry(exc="Task exceeded time limit!")
    except Exception as e:
        raise self.retry(exc=str(e))

@celery.task(bind=True, max_retries=3, default_retry_delay=10)
def fetch_data_and_create_plot(self):
    try:
        api_url = "https://api.example.com/data"
        response = requests.get(api_url)

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        data = response.json()
    
        x_values = data['x']
        y_values = data['y']

        fig = go.Figure(data=[go.Scatter(x=x_values, y=y_values, mode='markers')])
        image_path = os.path.join('images', 'plot.png')
        fig.write_image(image_path)
        return {'status': 'success', 'image_path': image_path}
    except Exception as e:
        raise self.retry(exc=e)