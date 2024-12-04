import os
import plotly.graph_objects as go
from flask import Flask, jsonify, request
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from celery_app import generate_plot
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/generate_plot', methods=['POST'])
def generate_plot_task():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    
    task_id = f"{x}_{y}"
    
    task = generate_plot.apply_async(args=[{'x': x, 'y': y, 'task_id': task_id}])
    
    return jsonify({'task_id': task.id}), 202

@app.route('/create_plot', methods=['POST'])
def create_plot():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    import io
    print(f"creating plot with data {x} and y: {y}")
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))
    plot_filename = "learning_plot.html"
    fig.write_html(plot_filename)
    buffer = io.StringIO()
    return jsonify({"image": "image created"}), 202

@app.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = generate_plot.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'status': 'Task is being processed'}
    elif task.state == 'SUCCESS':
        response = {'status': 'Task completed', 'result': task.result}
    elif task.state == 'FAILURE':
        response = {'status': 'Task failed', 'error': str(task.info)}
    else:
        response = {'status': 'Unknown state', 'state': task.state}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
