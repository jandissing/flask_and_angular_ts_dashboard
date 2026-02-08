#!/usr/bin/env python3
"""
Simple WebSocket test client for the Titanic Dashboard
Run this to verify WebSocket connectivity independently
"""

import socketio
import time

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print('✅ Connected to WebSocket server')
    print('📡 Requesting live metrics...')
    sio.emit('request_live_metrics')

@sio.event
def disconnect():
    print('❌ Disconnected from WebSocket server')

@sio.event
def connection_response(data):
    print(f'📨 Connection response: {data}')

@sio.event
def live_metrics_started(data):
    print(f'🚀 Live metrics streaming started: {data}')

@sio.event
def live_metrics(data):
    print('\n' + '='*60)
    print('📊 Live Metrics Update:')
    print(f"   Timestamp: {data['timestamp']}")
    print(f"   Active Queries: {data['active_queries']}")
    print(f"   Survival Rate: {data['current_survival_rate']:.2%}")
    print(f"   Passengers Analyzed: {data['passengers_analyzed']}")
    print(f"   Response Time: {data['avg_response_time']:.2f}ms")
    print(f"   Memory Usage: {data['memory_usage']:.2f}%")
    print(f"   Recent Survivor: {data['recent_survivor']['name']} "
          f"(Age: {data['recent_survivor']['age']}, "
          f"Class: {data['recent_survivor']['class']})")
    print('='*60)

if __name__ == '__main__':
    try:
        print('🔌 Connecting to WebSocket server at http://localhost:8000')
        sio.connect('http://localhost:8000')
        
        # Keep the script running to receive messages
        print('👂 Listening for live metrics... (Press Ctrl+C to stop)')
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print('\n\n👋 Disconnecting...')
        sio.disconnect()
        print('✅ Test client stopped')
    except Exception as e:
        print(f'❌ Error: {e}')
