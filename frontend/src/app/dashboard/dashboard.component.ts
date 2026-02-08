import { Component, OnInit, OnDestroy } from '@angular/core';
import { TitanicService, Statistics, LiveMetrics } from '../services/titanic.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, OnDestroy {
  statistics: Statistics | null = null;
  liveMetrics: LiveMetrics | null = null;
  survivalByClass: any[] = [];
  survivalByGender: any[] = [];
  ageDistribution: any[] = [];
  
  isLoading = true;
  error: string | null = null;
  
  private metricsSubscription: Subscription | null = null;

  constructor(private titanicService: TitanicService) {}

  ngOnInit(): void {
    this.loadDashboardData();
    this.setupLiveMetrics();
  }

  ngOnDestroy(): void {
    if (this.metricsSubscription) {
      this.metricsSubscription.unsubscribe();
    }
    this.titanicService.disconnectWebSocket();
  }

  loadDashboardData(): void {
    this.isLoading = true;
    this.error = null;

    // Load statistics
    this.titanicService.getStatistics().subscribe({
      next: (data) => {
        this.statistics = data;
        this.isLoading = false;
      },
      error: (err) => {
        this.error = 'Failed to load statistics';
        this.isLoading = false;
        console.error('Error loading statistics:', err);
      }
    });

    // Load survival by class
    this.titanicService.getSurvivalByClass().subscribe({
      next: (data) => {
        this.survivalByClass = data;
      },
      error: (err) => {
        console.error('Error loading survival by class:', err);
      }
    });

    // Load survival by gender
    this.titanicService.getSurvivalByGender().subscribe({
      next: (data) => {
        this.survivalByGender = data;
      },
      error: (err) => {
        console.error('Error loading survival by gender:', err);
      }
    });

    // Load age distribution
    this.titanicService.getAgeDistribution().subscribe({
      next: (data) => {
        this.ageDistribution = data;
      },
      error: (err) => {
        console.error('Error loading age distribution:', err);
      }
    });
  }

  setupLiveMetrics(): void {
    // Subscribe to live metrics from WebSocket
    this.metricsSubscription = this.titanicService.liveMetrics$.subscribe({
      next: (metrics) => {
        this.liveMetrics = metrics;
      },
      error: (err) => {
        console.error('Error receiving live metrics:', err);
      }
    });

    // Request live metrics from server
    this.titanicService.requestLiveMetrics();
  }

  getSurvivalPercentage(): number {
    return this.statistics ? this.statistics.survival_rate * 100 : 0;
  }

  getClassLabel(classNum: number): string {
    const labels: { [key: number]: string } = {
      1: 'First Class',
      2: 'Second Class',
      3: 'Third Class'
    };
    return labels[classNum] || 'Unknown';
  }

  formatNumber(num: number): string {
    return num.toFixed(2);
  }

  formatPercentage(rate: number): string {
    return (rate * 100).toFixed(1) + '%';
  }

  refresh(): void {
    this.loadDashboardData();
  }
}
