# Angular + TypeScript - Hands-On Exercises

Practice what you learned with these exercises! Start with Easy and work your way up.

---

## 🟢 Easy Exercises

### Exercise 1: Add a New Property

**Goal**: Display the average fare in the dashboard

**Steps:**
1. Open `dashboard.component.ts`
2. Add a method:
```typescript
getAverageFare(): number {
  return this.statistics ? this.statistics.avg_fare : 0;
}
```

3. Open `dashboard.component.html`
4. Add this in the statistics section:
```html
<div class="stat-card">
  <div class="stat-label">Average Fare</div>
  <div class="stat-value">${{ formatNumber(getAverageFare()) }}</div>
</div>
```

5. Save and see it in the browser!

---

### Exercise 2: Change Text

**Goal**: Change "Total Passengers" to "All Passengers"

**Steps:**
1. Open `dashboard.component.html`
2. Find the text "Total Passengers"
3. Change it to "All Passengers"
4. Save and refresh

**Bonus**: Change other labels too!

---

### Exercise 3: Add Console Logging

**Goal**: See what data looks like

**Steps:**
1. Open `dashboard.component.ts`
2. In `loadDashboardData()`, add:
```typescript
this.titanicService.getStatistics().subscribe({
  next: (data) => {
    console.log('📊 Statistics data:', data);  // ← Add this
    this.statistics = data;
    this.isLoading = false;
  }
});
```

3. Open browser DevTools (F12) → Console tab
4. Refresh page and see the data!

---

## 🟡 Medium Exercises

### Exercise 4: Create a New Method

**Goal**: Calculate survival percentage for males only

**Steps:**
1. Open `dashboard.component.ts`
2. Add this method:
```typescript
getMaleSurvivalRate(): number {
  if (!this.survivalByGender) return 0;
  
  const males = this.survivalByGender.find(g => g.gender === 'male');
  return males ? males.survival_rate * 100 : 0;
}
```

3. Display it in the template:
```html
<p>Male Survival Rate: {{ getMaleSurvivalRate().toFixed(1) }}%</p>
```

**Challenge**: Do the same for females!

---

### Exercise 5: Add a Button

**Goal**: Add a "Show Details" button

**Steps:**
1. Add a property in `dashboard.component.ts`:
```typescript
showDetails = false;
```

2. Add a method:
```typescript
toggleDetails(): void {
  this.showDetails = !this.showDetails;
  console.log('Details visible:', this.showDetails);
}
```

3. Add button in template:
```html
<button (click)="toggleDetails()">
  {{ showDetails ? 'Hide' : 'Show' }} Details
</button>

<div *ngIf="showDetails">
  <p>Here are the details!</p>
</div>
```

**What you learned:**
- Event binding: `(click)`
- Conditional rendering: `*ngIf`
- Ternary operator: `condition ? true : false`

---

### Exercise 6: Add Styling

**Goal**: Style the new button

**Steps:**
1. Open `dashboard.component.css`
2. Add:
```css
.details-button {
  background-color: #3498db;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.details-button:hover {
  background-color: #2980b9;
}
```

3. Update the button:
```html
<button class="details-button" (click)="toggleDetails()">
  {{ showDetails ? 'Hide' : 'Show' }} Details
</button>
```

---

## 🔴 Hard Exercises

### Exercise 7: Create a New REST API Call

**Goal**: Fetch and display individual passenger data

**Steps:**
1. Open `titanic.service.ts`
2. Add a new method:
```typescript
getPassenger(id: number): Observable<Passenger> {
  return this.http.get<Passenger>(`${this.apiUrl}/passengers/${id}`);
}
```

3. In `dashboard.component.ts`, add:
```typescript
selectedPassenger: Passenger | null = null;

loadPassenger(id: number): void {
  this.titanicService.getPassenger(id).subscribe({
    next: (passenger) => {
      this.selectedPassenger = passenger;
      console.log('Passenger loaded:', passenger);
    },
    error: (err) => {
      console.error('Failed to load passenger:', err);
    }
  });
}
```

4. In the template:
```html
<button (click)="loadPassenger(1)">Load Passenger #1</button>

<div *ngIf="selectedPassenger">
  <h3>{{ selectedPassenger.Name }}</h3>
  <p>Age: {{ selectedPassenger.Age }}</p>
  <p>Class: {{ selectedPassenger.Pclass }}</p>
  <p>Survived: {{ selectedPassenger.Survived ? 'Yes' : 'No' }}</p>
</div>
```

**Challenge**: Add an input field to let the user choose which passenger ID to load!

---

### Exercise 8: Filter Data

**Goal**: Show only survivors in the age distribution

**Steps:**
1. Add a property:
```typescript
showOnlySurvivors = false;
```

2. Add a method:
```typescript
getFilteredAgeDistribution() {
  if (!this.showOnlySurvivors) {
    return this.ageDistribution;
  }
  
  // In a real app, you'd filter by survivors
  // For now, just return all data
  return this.ageDistribution;
}
```

3. Add a checkbox:
```html
<label>
  <input type="checkbox" [(ngModel)]="showOnlySurvivors">
  Show only survivors
</label>
```

4. Update the loop:
```html
<div *ngFor="let ageGroup of getFilteredAgeDistribution()">
  <!-- ... -->
</div>
```

**Note**: You'll need to add `FormsModule` to `app.module.ts` for `[(ngModel)]` to work:
```typescript
import { FormsModule } from '@angular/forms';

@NgModule({
  imports: [
    // ... other imports
    FormsModule
  ]
})
```

---

### Exercise 9: Create a New Component

**Goal**: Create a separate component for passenger details

**Steps:**
1. Create new files:
   - `passenger-detail.component.ts`
   - `passenger-detail.component.html`
   - `passenger-detail.component.css`

2. In `passenger-detail.component.ts`:
```typescript
import { Component, Input } from '@angular/core';
import { Passenger } from '../services/titanic.service';

@Component({
  selector: 'app-passenger-detail',
  templateUrl: './passenger-detail.component.html',
  styleUrls: ['./passenger-detail.component.css']
})
export class PassengerDetailComponent {
  @Input() passenger: Passenger | null = null;
}
```

3. In `passenger-detail.component.html`:
```html
<div *ngIf="passenger" class="passenger-card">
  <h3>{{ passenger.Name }}</h3>
  <p>Age: {{ passenger.Age }}</p>
  <p>Class: {{ passenger.Pclass }}</p>
  <p>Survived: {{ passenger.Survived ? '✅ Yes' : '❌ No' }}</p>
</div>
```

4. Register in `app.module.ts`:
```typescript
import { PassengerDetailComponent } from './passenger-detail/passenger-detail.component';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    PassengerDetailComponent  // ← Add this
  ],
  // ...
})
```

5. Use it in dashboard template:
```html
<app-passenger-detail [passenger]="selectedPassenger"></app-passenger-detail>
```

**What you learned:**
- Component creation
- Input properties: `@Input()`
- Component communication

---

### Exercise 10: Add Error Handling UI

**Goal**: Show a nice error message when API fails

**Steps:**
1. Add to `dashboard.component.css`:
```css
.error-message {
  background-color: #e74c3c;
  color: white;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
  text-align: center;
}

.retry-button {
  background-color: white;
  color: #e74c3c;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  font-weight: bold;
}
```

2. Update template:
```html
<div *ngIf="error" class="error-message">
  <h3>⚠️ Oops! Something went wrong</h3>
  <p>{{ error }}</p>
  <button class="retry-button" (click)="refresh()">Try Again</button>
</div>
```

3. Test by stopping the backend and clicking refresh!

---

## 🚀 Advanced Challenges

### Challenge 1: Implement Search

Create a search box that filters passengers by name.

**Hints:**
- Add an input field with `[(ngModel)]="searchTerm"`
- Create a method `filterPassengers()`
- Use `Array.filter()` in TypeScript

---

### Challenge 2: Add Pagination

Show 10 passengers per page with previous/next buttons.

**Hints:**
- Track `currentPage`
- Calculate which passengers to show
- Implement `nextPage()` and `previousPage()` methods

---

### Challenge 3: Create a Chart

Use a library like Chart.js to visualize the age distribution.

**Hints:**
- Install: `npm install chart.js`
- Import in component
- Create canvas in template
- Initialize chart in `ngOnInit()`

---

### Challenge 4: Add Sorting

Allow users to sort passengers by age, class, or name.

**Hints:**
- Add dropdown to select sort field
- Create `sortPassengers(field: string)` method
- Use `Array.sort()`

---

### Challenge 5: Implement Local Storage

Save user preferences (like "show only survivors") to localStorage.

**Hints:**
```typescript
// Save
localStorage.setItem('showSurvivors', JSON.stringify(this.showOnlySurvivors));

// Load
const saved = localStorage.getItem('showSurvivors');
if (saved) {
  this.showOnlySurvivors = JSON.parse(saved);
}
```

---

## 💡 Tips for Success

### 1. Use Console.log Everywhere
```typescript
console.log('Data received:', data);
console.log('Current state:', this.someProperty);
```

### 2. Check the Browser Console
- Press F12
- Go to Console tab
- Look for errors (red text)
- Look for your console.log messages

### 3. Use Angular DevTools
- Install "Angular DevTools" Chrome extension
- Inspect component properties in real-time
- See the component tree

### 4. Read Error Messages
They usually tell you exactly what's wrong:
```
ERROR: Cannot read property 'Name' of null
→ You're trying to access passenger.Name but passenger is null
→ Solution: Add *ngIf="passenger" to check first
```

### 5. Start Small
- Make one small change
- Test it
- Make sure it works
- Then add more

### 6. Use TypeScript's Help
```typescript
// Hover over variables in VS Code to see their type
const passenger = ...;  // Hover here
//    ↑ VS Code shows: const passenger: Passenger

// Ctrl+Click on types to see their definition
Passenger  // Ctrl+Click to see interface definition
```

### 7. Format Your Code
- Install Prettier extension
- It auto-formats on save
- Makes code readable

---

## 📚 Additional Resources

### Official Docs
- **Angular**: https://angular.io/docs
- **TypeScript**: https://www.typescriptlang.org/docs
- **RxJS**: https://rxjs.dev/guide/overview

### Tutorials
- **Angular Tour of Heroes**: https://angular.io/tutorial
- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/intro.html

### Videos
- **Angular University** (YouTube)
- **Academind** (YouTube)
- **Fireship** (YouTube) - Quick, concise tutorials

---

## 🎯 Challenge Yourself

After completing these exercises, try:

1. **Build a new page**: Create a "Passengers List" page
2. **Add routing**: Navigate between Dashboard and Passengers pages
3. **Create a form**: Add new passengers (even if not saved to backend)
4. **Style everything**: Make it look professional
5. **Add animations**: Use Angular animations library

---

## ✅ Solutions

Need help? Check the `ANGULAR_TUTORIAL.md` file for concepts, or look at the existing code for patterns!

Remember: The best way to learn is by doing! Don't be afraid to break things - you can always revert with git or re-download the project.

Happy coding! 🚀
