#!/usr/bin/env python3
"""
REST API test client for the Titanic Dashboard
Run this to verify all API endpoints are working
"""

import requests
import json

BASE_URL = 'http://localhost:8000/api'

def print_response(endpoint, response):
    print(f'\n{"="*70}')
    print(f'📍 Endpoint: {endpoint}')
    print(f'✅ Status: {response.status_code}')
    print('📦 Response:')
    print(json.dumps(response.json(), indent=2))
    print('='*70)

def test_health():
    """Test health check endpoint"""
    print('\n🏥 Testing Health Check...')
    response = requests.get(f'{BASE_URL}/health')
    print_response('/api/health', response)

def test_statistics():
    """Test statistics endpoint"""
    print('\n📊 Testing Statistics...')
    response = requests.get(f'{BASE_URL}/statistics')
    print_response('/api/statistics', response)

def test_passengers():
    """Test passengers endpoint with pagination"""
    print('\n👥 Testing Passengers (Page 1, 5 per page)...')
    response = requests.get(f'{BASE_URL}/passengers?page=1&per_page=5')
    print_response('/api/passengers', response)

def test_single_passenger():
    """Test single passenger endpoint"""
    print('\n👤 Testing Single Passenger (ID: 1)...')
    response = requests.get(f'{BASE_URL}/passengers/1')
    print_response('/api/passengers/1', response)

def test_survival_by_class():
    """Test survival by class endpoint"""
    print('\n🎫 Testing Survival by Class...')
    response = requests.get(f'{BASE_URL}/survival-by-class')
    print_response('/api/survival-by-class', response)

def test_survival_by_gender():
    """Test survival by gender endpoint"""
    print('\n⚧️ Testing Survival by Gender...')
    response = requests.get(f'{BASE_URL}/survival-by-gender')
    print_response('/api/survival-by-gender', response)

def test_age_distribution():
    """Test age distribution endpoint"""
    print('\n🎂 Testing Age Distribution...')
    response = requests.get(f'{BASE_URL}/age-distribution')
    print_response('/api/age-distribution', response)

if __name__ == '__main__':
    print('🚀 Starting API Tests...')
    print('📡 Testing server at:', BASE_URL)
    
    try:
        test_health()
        test_statistics()
        test_passengers()
        test_single_passenger()
        test_survival_by_class()
        test_survival_by_gender()
        test_age_distribution()
        
        print('\n✅ All API tests completed successfully!')
        
    except requests.exceptions.ConnectionError:
        print('\n❌ Error: Cannot connect to server')
        print('Make sure the Flask server is running on http://localhost:8000')
    except Exception as e:
        print(f'\n❌ Error during testing: {e}')
