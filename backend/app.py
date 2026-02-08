from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import pandas as pd
import numpy as np
from datetime import datetime
import threading
import time
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Load Titanic dataset
def load_titanic_data():
    """Load or create sample Titanic dataset"""
    try:
        # If you have the actual dataset, load it here
        # df = pd.read_csv('titanic.csv')
        
        # Sample data for demonstration
        data = {
            'PassengerId': range(1, 892),
            'Survived': np.random.choice([0, 1], 891, p=[0.62, 0.38]),
            'Pclass': np.random.choice([1, 2, 3], 891),
            'Name': [f'Passenger {i}' for i in range(1, 892)],
            'Sex': np.random.choice(['male', 'female'], 891),
            'Age': np.random.randint(1, 80, 891),
            'SibSp': np.random.randint(0, 5, 891),
            'Parch': np.random.randint(0, 4, 891),
            'Fare': np.random.uniform(5, 500, 891),
            'Embarked': np.random.choice(['C', 'Q', 'S'], 891)
        }
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

df = load_titanic_data()

# REST API Endpoints

@app.route('/api/passengers', methods=['GET'])
def get_passengers():
    """Get all passengers with pagination"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    start = (page - 1) * per_page
    end = start + per_page
    
    passengers = df.iloc[start:end].to_dict('records')
    
    return jsonify({
        'data': passengers,
        'total': len(df),
        'page': page,
        'per_page': per_page,
        'total_pages': (len(df) + per_page - 1) // per_page
    })

@app.route('/api/passengers/<int:passenger_id>', methods=['GET'])
def get_passenger(passenger_id):
    """Get specific passenger by ID"""
    passenger = df[df['PassengerId'] == passenger_id]
    
    if passenger.empty:
        return jsonify({'error': 'Passenger not found'}), 404
    
    return jsonify(passenger.to_dict('records')[0])

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get basic statistics about the dataset"""
    stats = {
        'total_passengers': len(df),
        'survived': int(df['Survived'].sum()),
        'perished': int((df['Survived'] == 0).sum()),
        'survival_rate': float(df['Survived'].mean()),
        'avg_age': float(df['Age'].mean()),
        'avg_fare': float(df['Fare'].mean()),
        'male_passengers': int((df['Sex'] == 'male').sum()),
        'female_passengers': int((df['Sex'] == 'female').sum()),
        'class_distribution': {
            'first': int((df['Pclass'] == 1).sum()),
            'second': int((df['Pclass'] == 2).sum()),
            'third': int((df['Pclass'] == 3).sum())
        }
    }
    
    return jsonify(stats)

@app.route('/api/survival-by-class', methods=['GET'])
def survival_by_class():
    """Get survival statistics by passenger class"""
    result = []
    for pclass in [1, 2, 3]:
        class_df = df[df['Pclass'] == pclass]
        result.append({
            'class': pclass,
            'total': len(class_df),
            'survived': int(class_df['Survived'].sum()),
            'survival_rate': float(class_df['Survived'].mean())
        })
    
    return jsonify(result)

@app.route('/api/survival-by-gender', methods=['GET'])
def survival_by_gender():
    """Get survival statistics by gender"""
    result = []
    for gender in ['male', 'female']:
        gender_df = df[df['Sex'] == gender]
        result.append({
            'gender': gender,
            'total': len(gender_df),
            'survived': int(gender_df['Survived'].sum()),
            'survival_rate': float(gender_df['Survived'].mean())
        })
    
    return jsonify(result)

@app.route('/api/age-distribution', methods=['GET'])
def age_distribution():
    """Get age distribution data"""
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80']
    
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, include_lowest=True)
    age_dist = df.groupby('AgeGroup').size().to_dict()
    
    result = [{'age_group': str(k), 'count': int(v)} for k, v in age_dist.items()]
    
    return jsonify(result)

# WebSocket events

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('connection_response', {'message': 'Connected to Titanic Dashboard'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('request_live_metrics')
def handle_live_metrics_request():
    """Start sending live metrics to the client"""
    print('Live metrics requested')
    emit('live_metrics_started', {'message': 'Live metrics streaming started'})

# Background task to send live metrics
def send_live_metrics():
    """Send live metrics via WebSocket every 3 seconds"""
    while True:
        time.sleep(3)
        
        # Simulate real-time metrics (in real scenario, this could be live data)
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'active_queries': random.randint(5, 50),
            'current_survival_rate': float(df['Survived'].mean()) + random.uniform(-0.05, 0.05),
            'passengers_analyzed': random.randint(800, 891),
            'avg_response_time': random.uniform(50, 200),
            'memory_usage': random.uniform(60, 85),
            'recent_survivor': {
                'name': f'Passenger {random.randint(1, 891)}',
                'age': random.randint(1, 80),
                'class': random.randint(1, 3)
            }
        }
        
        # Use namespace='/' and no broadcast parameter for flask-socketio 5.x
        socketio.emit('live_metrics', metrics, namespace='/')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Start background thread for live metrics
    metrics_thread = threading.Thread(target=send_live_metrics, daemon=True)
    metrics_thread.start()
    
    print("Starting Flask server with WebSocket support...")
    print("Backend running on http://localhost:8000")
    socketio.run(app, debug=True, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)
