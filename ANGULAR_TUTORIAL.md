# Angular + TypeScript Tutorial - Titanic Dashboard Frontend

## Table of Contents
1. [Project Structure](#project-structure)
2. [TypeScript Basics](#typescript-basics)
3. [Angular Architecture](#angular-architecture)
4. [Services - Data Layer](#services)
5. [Components - UI Layer](#components)
6. [Observables & RxJS](#observables-rxjs)
7. [HTTP Requests](#http-requests)
8. [WebSocket Integration](#websocket-integration)
9. [Template Syntax](#template-syntax)
10. [Component Lifecycle](#component-lifecycle)

---

## Project Structure

```
frontend/src/app/
├── services/
│   └── titanic.service.ts      # Data fetching & WebSocket
├── dashboard/
│   ├── dashboard.component.ts   # Logic
│   ├── dashboard.component.html # Template
│   └── dashboard.component.css  # Styles
├── app.component.ts             # Root component
└── app.module.ts                # Module configuration
```

**Key Concept**: Angular separates concerns
- **Services** = Business logic & data
- **Components** = UI & presentation
- **Modules** = Package related code together

---

## TypeScript Basics

### What is TypeScript?

TypeScript = JavaScript + Types

```typescript
// JavaScript (no types)
let name = "John";
name = 42; // OK in JS, but confusing!

// TypeScript (with types)
let name: string = "John";
name = 42; // ERROR! Type 'number' is not assignable to type 'string'
```

### Types in Our Code

```typescript
// From titanic.service.ts

// Interface - defines the shape of an object
export interface Passenger {
  PassengerId: number;      // Must be a number
  Survived: number;         // Must be a number
  Pclass: number;           // Must be a number
  Name: string;             // Must be a string
  Sex: string;              // Must be a string
  Age: number;              // Must be a number
  SibSp: number;            // Must be a number
  Parch: number;            // Must be a number
  Fare: number;             // Must be a number
  Embarked: string;         // Must be a string
}
```

**Why use interfaces?**
- Autocomplete in your editor
- Catch errors before runtime
- Self-documenting code
- Refactoring is safer

### Example: Interface Benefits

```typescript
// Without interface (JavaScript)
function displayPassenger(passenger) {
  console.log(passenger.name); // Typo! Should be 'Name'
  // No error until runtime!
}

// With interface (TypeScript)
function displayPassenger(passenger: Passenger) {
  console.log(passenger.name); // ERROR! Property 'name' does not exist
  console.log(passenger.Name); // ✅ Correct!
}
```

---

## Angular Architecture

### The Big Picture

```
┌─────────────────────────────────────────┐
│           Browser (User)                │
└─────────────────────────────────────────┘
                 ▲  │
                 │  ▼
┌─────────────────────────────────────────┐
│         Component (UI Logic)            │
│  - dashboard.component.ts               │
│  - Handles user interactions            │
│  - Prepares data for display            │
└─────────────────────────────────────────┘
                 ▲  │
                 │  ▼
┌─────────────────────────────────────────┐
│         Service (Data Logic)            │
│  - titanic.service.ts                   │
│  - Makes HTTP requests                  │
│  - Manages WebSocket connection         │
└─────────────────────────────────────────┘
                 ▲  │
                 │  ▼
┌─────────────────────────────────────────┐
│         Backend API                     │
│  - Flask server on port 8000            │
└─────────────────────────────────────────┘
```

### Key Principles

1. **Separation of Concerns**
   - Components = UI
   - Services = Data
   - Don't mix them!

2. **Dependency Injection**
   - Angular provides services to components
   - No need to manually create instances

3. **Reactive Programming**
   - Data flows through Observables
   - Components subscribe to changes

---

## Services - Data Layer

### What is a Service?

A service is a class that:
- Fetches data from APIs
- Manages state
- Provides reusable logic
- Is **injected** into components

### Service Anatomy

```typescript
// From titanic.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'  // ← Makes this service available app-wide
})
export class TitanicService {
  private apiUrl = 'http://localhost:8000/api';
  
  constructor(private http: HttpClient) {
    // HttpClient is INJECTED by Angular
    // We don't create it manually!
  }
  
  // Method to get data
  getStatistics(): Observable<Statistics> {
    return this.http.get<Statistics>(`${this.apiUrl}/statistics`);
  }
}
```

### Breaking It Down

#### 1. The `@Injectable` Decorator

```typescript
@Injectable({
  providedIn: 'root'
})
```

**What it means:**
- "This class can be injected into other classes"
- `providedIn: 'root'` means it's a **singleton** (only one instance)
- Available everywhere in the app

#### 2. Dependency Injection

```typescript
constructor(private http: HttpClient) { }
```

**What's happening:**
- Angular sees "I need HttpClient"
- Angular creates/provides HttpClient automatically
- We can now use `this.http` throughout the service

**No need to do this:**
```typescript
// DON'T DO THIS! Angular does it for you
const httpClient = new HttpClient(...);
```

#### 3. Private vs Public

```typescript
private apiUrl = 'http://localhost:8000/api';  // Only this class can access
public liveMetrics$ = this.liveMetricsSubject.asObservable();  // Other classes can access
```

---

## Components - UI Layer

### What is a Component?

A component is:
- TypeScript class (logic)
- HTML template (structure)
- CSS file (styling)

Think of it as a custom HTML element!

### Component Anatomy

```typescript
// From dashboard.component.ts

import { Component, OnInit, OnDestroy } from '@angular/core';
import { TitanicService, Statistics } from '../services/titanic.service';

@Component({
  selector: 'app-dashboard',              // ← HTML tag name
  templateUrl: './dashboard.component.html',  // ← HTML file
  styleUrls: ['./dashboard.component.css']    // ← CSS file
})
export class DashboardComponent implements OnInit, OnDestroy {
  // Properties (data)
  statistics: Statistics | null = null;
  isLoading = true;
  
  // Constructor (dependency injection)
  constructor(private titanicService: TitanicService) {}
  
  // Lifecycle hooks
  ngOnInit(): void {
    this.loadDashboardData();
  }
  
  ngOnDestroy(): void {
    // Cleanup
  }
  
  // Methods (functions)
  loadDashboardData(): void {
    // Load data...
  }
}
```

### Breaking It Down

#### 1. The `@Component` Decorator

```typescript
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
```

**What it means:**
- `selector`: Use `<app-dashboard></app-dashboard>` in HTML
- `templateUrl`: Points to HTML template
- `styleUrls`: Points to CSS file(s)

#### 2. Component Properties

```typescript
statistics: Statistics | null = null;
isLoading = true;
error: string | null = null;
```

**Type annotations:**
- `Statistics | null` means "Statistics object OR null"
- `= null` is the initial value
- These are accessible in the template!

#### 3. Constructor with Injection

```typescript
constructor(private titanicService: TitanicService) {}
```

**What happens:**
1. Angular creates TitanicService (or reuses existing one)
2. Injects it into the component
3. Available as `this.titanicService`

#### 4. Lifecycle Hooks

```typescript
ngOnInit(): void {
  this.loadDashboardData();
}

ngOnDestroy(): void {
  if (this.metricsSubscription) {
    this.metricsSubscription.unsubscribe();
  }
}
```

**Component Lifecycle:**
```
Component Created
       ↓
ngOnInit() ← Do initialization here (load data)
       ↓
Component Running (user interacts)
       ↓
ngOnDestroy() ← Clean up here (unsubscribe, etc.)
       ↓
Component Destroyed
```

---

## Observables & RxJS

### What is an Observable?

Think of it like a **stream of data over time**:

```
Timeline: ─────────────────────────────────────→
Data:     ───①───②───③───④───⑤───⑥───────────→
          
① First data arrives
② Second data arrives
③ Third data arrives
... and so on
```

### Example: HTTP Request

```typescript
// Service
getStatistics(): Observable<Statistics> {
  return this.http.get<Statistics>(`${this.apiUrl}/statistics`);
}

// Component
this.titanicService.getStatistics().subscribe({
  next: (data) => {
    // ✅ Success! Data arrived
    this.statistics = data;
  },
  error: (err) => {
    // ❌ Error occurred
    this.error = 'Failed to load';
  }
});
```

**What's happening:**
1. Component calls `getStatistics()`
2. Returns an Observable (not the data itself!)
3. Component **subscribes** to the Observable
4. When data arrives, `next` callback runs
5. If error occurs, `error` callback runs

### Observable vs Promise

```typescript
// Promise (one value, then done)
fetch('/api/data')
  .then(data => console.log(data))  // Gets data once
  .catch(err => console.error(err));

// Observable (multiple values over time)
dataStream$
  .subscribe(data => console.log(data));  // Can receive many values
  // Value 1 arrives → callback runs
  // Value 2 arrives → callback runs
  // Value 3 arrives → callback runs
  // etc...
```

### Subject (Special Observable)

```typescript
// From titanic.service.ts
private liveMetricsSubject = new Subject<LiveMetrics>();
public liveMetrics$ = this.liveMetricsSubject.asObservable();
```

**Subject is like a pipe:**
```
WebSocket → Subject → Multiple Subscribers
                │
                ├→ Component 1
                ├→ Component 2
                └→ Component 3
```

**How it works:**
```typescript
// Service pushes data into the Subject
this.socket.on('live_metrics', (metrics: LiveMetrics) => {
  this.liveMetricsSubject.next(metrics);  // Push data
});

// Component subscribes to the Observable
this.titanicService.liveMetrics$.subscribe(metrics => {
  this.liveMetrics = metrics;  // Receive data
});
```

---

## HTTP Requests

### Basic HTTP GET

```typescript
// Service method
getStatistics(): Observable<Statistics> {
  return this.http.get<Statistics>(`${this.apiUrl}/statistics`);
}

// Component usage
this.titanicService.getStatistics().subscribe({
  next: (data) => {
    this.statistics = data;
    this.isLoading = false;
  },
  error: (err) => {
    this.error = 'Failed to load statistics';
    this.isLoading = false;
  }
});
```

### HTTP GET with Parameters

```typescript
// Service
getPassengers(page: number = 1, perPage: number = 10): Observable<PaginatedResponse> {
  const params = new HttpParams()
    .set('page', page.toString())
    .set('per_page', perPage.toString());
  
  return this.http.get<PaginatedResponse>(`${this.apiUrl}/passengers`, { params });
}

// Component
this.titanicService.getPassengers(1, 20).subscribe(data => {
  console.log(data.data);  // Array of passengers
});
```

**URL generated:** `http://localhost:8000/api/passengers?page=1&per_page=20`

### Type Safety with Generics

```typescript
// Generic syntax: get<TypeYouExpect>()
this.http.get<Statistics>(`${this.apiUrl}/statistics`)
//             ↑
//             Tells TypeScript what type to expect

// Now TypeScript knows the response type!
.subscribe(data => {
  console.log(data.total_passengers);  // ✅ Autocomplete works!
  console.log(data.wrongProperty);     // ❌ Error! Property doesn't exist
});
```

---

## WebSocket Integration

### Setting Up WebSocket

```typescript
import { io, Socket } from 'socket.io-client';

export class TitanicService {
  private socket: Socket;
  
  constructor(private http: HttpClient) {
    // Create WebSocket connection
    this.socket = io('http://localhost:8000', {
      transports: ['websocket', 'polling'],  // Try WebSocket first, fallback to polling
      reconnection: true,                     // Auto-reconnect if disconnected
      reconnectionDelay: 1000,                // Wait 1 second between reconnection attempts
      reconnectionAttempts: 5                 // Try 5 times
    });
    
    this.setupSocketListeners();
  }
}
```

### Listening to Events

```typescript
private setupSocketListeners(): void {
  // When connection is established
  this.socket.on('connect', () => {
    console.log('✅ Connected to WebSocket server');
  });
  
  // When server sends 'live_metrics' event
  this.socket.on('live_metrics', (metrics: LiveMetrics) => {
    console.log('📊 Live metrics received:', metrics);
    this.liveMetricsSubject.next(metrics);  // Push to subscribers
  });
  
  // When disconnected
  this.socket.on('disconnect', () => {
    console.log('⚠️ Disconnected from WebSocket server');
  });
  
  // When connection error occurs
  this.socket.on('connect_error', (error: any) => {
    console.error('❌ WebSocket connection error:', error);
  });
}
```

### Sending Events to Server

```typescript
requestLiveMetrics(): void {
  this.socket.emit('request_live_metrics');  // Send event to server
}
```

### WebSocket Flow

```
Component                Service                 Backend
   │                       │                       │
   │ requestLiveMetrics()  │                       │
   ├──────────────────────>│                       │
   │                       │ emit('request...')    │
   │                       ├──────────────────────>│
   │                       │                       │
   │                       │ on('live_metrics')    │
   │                       │<──────────────────────┤
   │                       │                       │
   │  liveMetrics$        │ subject.next()        │
   │<──────────────────────┤                       │
   │                       │                       │
   │ (update UI)           │                       │
```

---

## Template Syntax

### Interpolation (Display Data)

```html
<!-- dashboard.component.html -->

<!-- Display property -->
<h1>{{ statistics.total_passengers }}</h1>

<!-- Call method -->
<p>{{ formatPercentage(statistics.survival_rate) }}</p>

<!-- Expression -->
<p>{{ statistics.survived + statistics.perished }}</p>
```

### Property Binding

```html
<!-- Bind to HTML attribute -->
<div [style.width.%]="survivalRate * 100"></div>

<!-- Bind to class -->
<div [class.active]="isActive"></div>

<!-- Bind to disabled state -->
<button [disabled]="isLoading">Submit</button>
```

### Event Binding

```html
<!-- Click event -->
<button (click)="refresh()">Refresh</button>

<!-- Mouse events -->
<div (mouseenter)="onHover()" (mouseleave)="onLeave()">Hover me</div>

<!-- Input event -->
<input (input)="onInputChange($event)">
```

### Structural Directives

#### *ngIf (Conditional Rendering)

```html
<!-- Show element if condition is true -->
<div *ngIf="isLoading">
  <p>Loading...</p>
</div>

<!-- Show one thing or another -->
<div *ngIf="!isLoading && !error">
  <p>Data loaded successfully!</p>
</div>

<div *ngIf="error">
  <p>{{ error }}</p>
</div>
```

**What TypeScript sees:**
```typescript
isLoading = true;  // Show loading message
isLoading = false; // Hide loading message
```

#### *ngFor (Loop Through Array)

```html
<!-- Loop through array -->
<div *ngFor="let passenger of passengers">
  <h3>{{ passenger.Name }}</h3>
  <p>Age: {{ passenger.Age }}</p>
</div>

<!-- With index -->
<div *ngFor="let passenger of passengers; let i = index">
  <p>{{ i + 1 }}. {{ passenger.Name }}</p>
</div>
```

**What TypeScript sees:**
```typescript
passengers = [
  { Name: 'John', Age: 30 },
  { Name: 'Jane', Age: 25 }
];
```

### Pipes (Transform Data)

```html
<!-- Format date -->
<p>{{ timestamp | date:'short' }}</p>
<!-- Output: 2/8/26, 3:45 PM -->

<!-- Uppercase -->
<p>{{ name | uppercase }}</p>
<!-- Output: JOHN DOE -->

<!-- Currency -->
<p>{{ price | currency:'USD' }}</p>
<!-- Output: $42.00 -->

<!-- Custom pipe -->
<p>{{ value | formatNumber }}</p>
```

---

## Component Lifecycle

### Lifecycle Hooks in Order

```typescript
export class DashboardComponent implements OnInit, OnDestroy {
  constructor() {
    console.log('1. Constructor called');
    // Component is being created
  }
  
  ngOnInit(): void {
    console.log('2. ngOnInit called');
    // Component is initialized - DO YOUR SETUP HERE
    this.loadDashboardData();
  }
  
  ngOnDestroy(): void {
    console.log('3. ngOnDestroy called');
    // Component is about to be destroyed - CLEANUP HERE
    if (this.metricsSubscription) {
      this.metricsSubscription.unsubscribe();
    }
  }
}
```

### Full Lifecycle

```
1. constructor()        ← Component created, inject dependencies
2. ngOnInit()          ← Component initialized, load data
3. Component renders   ← Display on screen
4. User interacts      ← Component is active
5. ngOnDestroy()       ← Component is destroyed, cleanup
```

### Best Practices

```typescript
// ✅ DO: Initialize in ngOnInit
ngOnInit(): void {
  this.loadData();
  this.subscribeToUpdates();
}

// ❌ DON'T: Initialize in constructor
constructor(private service: Service) {
  this.loadData();  // BAD! Component not ready yet
}

// ✅ DO: Cleanup in ngOnDestroy
ngOnDestroy(): void {
  this.subscription.unsubscribe();
  this.socket.disconnect();
}

// ❌ DON'T: Forget to cleanup
// Memory leaks! Subscriptions keep running even after component is destroyed
```

---

## Real Example Walkthrough

Let's trace what happens when you load the dashboard:

### Step 1: Component is Created

```typescript
// dashboard.component.ts
constructor(private titanicService: TitanicService) {}
```

- Angular creates DashboardComponent
- Angular injects TitanicService
- Constructor runs (but don't load data yet!)

### Step 2: Component Initializes

```typescript
ngOnInit(): void {
  this.loadDashboardData();
  this.setupLiveMetrics();
}
```

- Component is ready
- Call initialization methods

### Step 3: Load Dashboard Data

```typescript
loadDashboardData(): void {
  this.isLoading = true;
  this.error = null;

  // Make HTTP request
  this.titanicService.getStatistics().subscribe({
    next: (data) => {
      this.statistics = data;  // Store data
      this.isLoading = false;  // Hide loading
    },
    error: (err) => {
      this.error = 'Failed to load statistics';
      this.isLoading = false;
    }
  });
}
```

**Flow:**
```
1. Set isLoading = true (show "Loading..." in UI)
2. Call service.getStatistics()
3. Service makes HTTP GET to backend
4. Backend responds with JSON data
5. Subscribe callback runs with data
6. Store data in this.statistics
7. Set isLoading = false (hide "Loading...", show data)
```

### Step 4: Setup WebSocket

```typescript
setupLiveMetrics(): void {
  // Subscribe to live metrics stream
  this.metricsSubscription = this.titanicService.liveMetrics$.subscribe({
    next: (metrics) => {
      this.liveMetrics = metrics;  // Update UI automatically!
    },
    error: (err) => {
      console.error('Error receiving live metrics:', err);
    }
  });

  // Request server to start sending metrics
  this.titanicService.requestLiveMetrics();
}
```

**Flow:**
```
1. Subscribe to liveMetrics$ Observable
2. Send 'request_live_metrics' event to server
3. Server starts sending metrics every 3 seconds
4. Each time data arrives, subscribe callback runs
5. Update this.liveMetrics
6. Angular automatically updates the UI!
```

### Step 5: Template Renders

```html
<!-- Show loading state -->
<div *ngIf="isLoading">
  <p>Loading dashboard data...</p>
</div>

<!-- Show data when loaded -->
<div *ngIf="!isLoading && !error">
  <h2>Total Passengers: {{ statistics.total_passengers }}</h2>
</div>

<!-- Show live metrics (updates every 3 seconds) -->
<div *ngIf="liveMetrics">
  <p>Active Queries: {{ liveMetrics.active_queries }}</p>
</div>
```

**Rendering Flow:**
```
Initial:
  isLoading = true
  → Shows "Loading..."

Data arrives:
  isLoading = false
  statistics = { total_passengers: 891, ... }
  → Shows statistics

Live metrics arrive (every 3 seconds):
  liveMetrics = { active_queries: 42, ... }
  → Updates numbers automatically
```

### Step 6: Component Destroyed

```typescript
ngOnDestroy(): void {
  if (this.metricsSubscription) {
    this.metricsSubscription.unsubscribe();
  }
  this.titanicService.disconnectWebSocket();
}
```

- User navigates away
- Component is destroyed
- Cleanup: unsubscribe, disconnect WebSocket
- Prevents memory leaks!

---

## Key Concepts Summary

### 1. TypeScript = JavaScript + Types
```typescript
let name: string = "John";  // Type annotation
```

### 2. Services = Data Logic
```typescript
@Injectable({ providedIn: 'root' })
export class TitanicService { }
```

### 3. Components = UI Logic
```typescript
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent { }
```

### 4. Dependency Injection
```typescript
constructor(private service: TitanicService) { }
// Angular provides the service automatically
```

### 5. Observables = Data Streams
```typescript
this.service.getData().subscribe(data => {
  console.log(data);  // Runs when data arrives
});
```

### 6. Template Syntax
```html
{{ variable }}           <!-- Display data -->
[property]="value"       <!-- Bind property -->
(event)="method()"       <!-- Handle event -->
*ngIf="condition"        <!-- Conditional -->
*ngFor="let item of items"  <!-- Loop -->
```

### 7. Component Lifecycle
```typescript
ngOnInit()    → Initialize
ngOnDestroy() → Cleanup
```

---

## Common Patterns

### Pattern 1: Load Data on Init

```typescript
export class MyComponent implements OnInit {
  data: any;
  
  constructor(private service: MyService) {}
  
  ngOnInit(): void {
    this.service.getData().subscribe(data => {
      this.data = data;
    });
  }
}
```

### Pattern 2: Handle Loading & Errors

```typescript
export class MyComponent {
  data: any;
  isLoading = true;
  error: string | null = null;
  
  loadData(): void {
    this.isLoading = true;
    this.error = null;
    
    this.service.getData().subscribe({
      next: (data) => {
        this.data = data;
        this.isLoading = false;
      },
      error: (err) => {
        this.error = 'Failed to load';
        this.isLoading = false;
      }
    });
  }
}
```

### Pattern 3: Cleanup Subscriptions

```typescript
export class MyComponent implements OnDestroy {
  private subscription: Subscription;
  
  ngOnInit(): void {
    this.subscription = this.service.getData().subscribe(...);
  }
  
  ngOnDestroy(): void {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}
```

---

## Next Steps

To continue learning:

1. **Experiment**: Modify the code and see what happens
2. **Read**: Angular docs at angular.io
3. **Build**: Create a new component or service
4. **Debug**: Use browser DevTools and console.log()

Happy coding! 🚀
