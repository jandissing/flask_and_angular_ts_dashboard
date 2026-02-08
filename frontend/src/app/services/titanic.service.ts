import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { io, Socket } from 'socket.io-client';

export interface Passenger {
  PassengerId: number;
  Survived: number;
  Pclass: number;
  Name: string;
  Sex: string;
  Age: number;
  SibSp: number;
  Parch: number;
  Fare: number;
  Embarked: string;
}

export interface PaginatedResponse {
  data: Passenger[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface Statistics {
  total_passengers: number;
  survived: number;
  perished: number;
  survival_rate: number;
  avg_age: number;
  avg_fare: number;
  male_passengers: number;
  female_passengers: number;
  class_distribution: {
    first: number;
    second: number;
    third: number;
  };
}

export interface LiveMetrics {
  timestamp: string;
  active_queries: number;
  current_survival_rate: number;
  passengers_analyzed: number;
  avg_response_time: number;
  memory_usage: number;
  recent_survivor: {
    name: string;
    age: number;
    class: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class TitanicService {
  private apiUrl = 'http://localhost:8000/api';
  private socket: Socket;
  private liveMetricsSubject = new Subject<LiveMetrics>();
  
  public liveMetrics$ = this.liveMetricsSubject.asObservable();

  constructor(private http: HttpClient) {
    this.socket = io('http://localhost:8000', {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5
    });
    this.setupSocketListeners();
  }

  private setupSocketListeners(): void {
    this.socket.on('connect', () => {
      console.log('✅ Connected to WebSocket server');
    });

    this.socket.on('connection_response', (data: any) => {
      console.log('📨 Connection response:', data);
    });

    this.socket.on('live_metrics', (metrics: LiveMetrics) => {
      console.log('📊 Live metrics received:', metrics);
      this.liveMetricsSubject.next(metrics);
    });

    this.socket.on('disconnect', () => {
      console.log('⚠️ Disconnected from WebSocket server');
    });

    this.socket.on('connect_error', (error: any) => {
      console.error('❌ WebSocket connection error:', error);
      console.log('💡 Make sure backend is running on http://localhost:8000');
    });
  }

  // REST API Methods

  getPassengers(page: number = 1, perPage: number = 10): Observable<PaginatedResponse> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('per_page', perPage.toString());
    
    return this.http.get<PaginatedResponse>(`${this.apiUrl}/passengers`, { params });
  }

  getPassenger(id: number): Observable<Passenger> {
    return this.http.get<Passenger>(`${this.apiUrl}/passengers/${id}`);
  }

  getStatistics(): Observable<Statistics> {
    return this.http.get<Statistics>(`${this.apiUrl}/statistics`);
  }

  getSurvivalByClass(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/survival-by-class`);
  }

  getSurvivalByGender(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/survival-by-gender`);
  }

  getAgeDistribution(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/age-distribution`);
  }

  // WebSocket Methods

  requestLiveMetrics(): void {
    this.socket.emit('request_live_metrics');
  }

  disconnectWebSocket(): void {
    if (this.socket) {
      this.socket.disconnect();
    }
  }

  reconnectWebSocket(): void {
    if (this.socket) {
      this.socket.connect();
    }
  }
}
