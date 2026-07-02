# Assessment Submission

This repository contains my answers to the assessment questions, along with the code for Question 1.

## Contents

| Path                                         | Description                                                                    |
| -------------------------------------------- | ------------------------------------------------------------------------------ |
| `README.md`                                  | This file — written answers to all four questions, plus setup/run instructions |
| [`question_1/main.go`](./question_1/main.go) | Go program for Question 1 (dedupe + sort)                                      |

---

## Question 1 — Duplicate Removal & Sorting (Go Program)

The full program is in [`question_1/main.go`](./question_1/main.go). See [Running the Code](#running-the-code) below for setup instructions.

**Approach:**

Given the list `12, 7, 12, 3, 5, 7, 8, 3, 9`, the program:

1. **Removes duplicates** by inserting every value into a `map[int]struct{}`. Map keys are inherently unique, so re-inserting an existing value is a no-op , as a result there's no need to use a nested loop to do comparisons and remove the duplicates. My approach has a time-complexity of O(n).
2. **Converts the map back into a slice**, since maps in Go have no guaranteed iteration order and can't be sorted directly.
3. **Sorts the slice** in ascending order using the standard library's `sort.Ints`, which runs in O(n log n) rather than hand-rolling an O(n²) algorithm like bubble sort.

Overall complexity is O(n log n), dominated by the sort step.

### Running the Code

**Prerequisites:** [Go](https://go.dev/dl/) installed (version 1.22 or later recommended). Verify with:

```bash
go version
```

**Setup & run:**

```bash
git clone github.com/mbeka02/enclan_africa_assessment
cd enclan_africa_assessment/question_1
go run main.go
```

**Expected output:**

```
[3 5 7 8 9 12]
```

---

## Question 2 — Django API Development

_(space reserved — to be filled in)_

---

## Question 3 — Mobile App Design (Shop Sales App)

**Scenario:** A simple mobile app for a small shop in Kenya that lets the owner add products, record sales, and view today's total sales.

### 1. Screens

- **Add Product** — for creating new products in the shop's catalog.
- **Record Sale** — for logging a sale against an existing product.
- **Today's Sales** — a dashboard/summary of the day's activity.

Three screens is intentionally minimal , a shop owner using this between customers needs to get in, complete a task, and get out, not navigate a deep nested menu.

### 2. Information on each screen

**Add Product**

- Product name
- Price
- Quantity in stock
- A "Save Product" button

**Record Sale**

- A searchable/scrollable list (or grid) of existing products to pick from — not a free-text field
- Quantity being sold (defaults to 1, with +/- steppers)
- Auto-calculated total (price × quantity), computed by the app, not typed in
- A "Complete Sale" button, followed by a confirmation step

**Today's Sales**

- Total sales amount for today, shown prominently at the top
- Number of transactions today
- A simple list of today's individual sales (product, quantity, amount, time), most recent first

### 3. Two things to make it easy for a non-technical owner

1. **Pick, don't type.** Recording a sale should be selection-based (tap a product from a list/grid, adjust quantity with +/- buttons) rather than requiring the owner to type product names or prices from memory. This removes typos and the need to remember exact spelling or pricing, and it's much faster during a busy moment at the till.
2. **Large, icon-led, single-purpose buttons.** Big touch targets with a short label and a simple icon (e.g. a "+" for Add Product, a shopping cart for Record Sale) reduce reliance on reading and interpreting text, and lower the chance of mis-taps. Keeping each screen to one clear task (rather than combining, say, "add product" and "record sale" on the same screen) also reduces cognitive load for someone who isn't used to navigating apps.

### 4. A possible mistake and how the app prevents it

**Mistake:** Recording the wrong quantity for a sale , for example, meaning to sell 1 unit but accidentally tapping to increase the quantity to 10, or double-tapping "Complete Sale" and logging the same sale twice. Either mistake silently inflates the day's sales total and stock deductions, and might not be noticed until the owner reconciles cash at the end of the day.

**How the app prevents/corrects it:**

- Show a **confirmation screen or modal/popup** before finalizing a sale: "Sell 1 × Sugar 1kg for KES 150?" with clear Confirm/Cancel options — rather than completing the sale the instant a button is tapped. This catches accidental quantity changes or accidental taps before they're recorded.
- Allow the owner to **edit or delete a sale** from the Today's Sales list (e.g. within the same day, or with a simple undo right after recording it), so an error that does slip through can be corrected without needing to contact support or leave the total permanently wrong.

---

## Question 4 — Relational Databases

**Scenario:** A school needs to track students, courses, and which students are enrolled in which courses.

### 1. Tables

Three tables are needed:

- `Students` — one row per student
- `Courses` — one row per course
- `Enrollments` — one row per student-course enrollment (the junction/join table connecting the two)

### 2. Columns

**`Students`**

- `StudentID`
- `FirstName`
- `LastName`
- `Email`
- `Gender`
- `DateOfBirth`
  **`Courses`**
- `CourseID`
- `CourseName`
- `Description` (optional)
  **`Enrollments`**
- `EnrollmentID`
- `StudentID` (foreign key → `Students.StudentID`)
- `CourseID` (foreign key → `Courses.CourseID`)
- `EnrollmentDate` (optional, but useful for tracking when enrollment happened)

### 3. Primary keys

- `Students.StudentID` is the primary key of `Students`.
- `Courses.CourseID` is the primary key of `Courses`.
- `Enrollments.EnrollmentID` is the primary key of `Enrollments`. A surrogate key like this is preferable to a composite key of `(StudentID, CourseID)` because it gives every enrollment a single, stable identifier , this is useful if the school later needs to reference a specific enrollment record directly (e.g. for a grade or an attendance record tied to that enrollment), without having to carry both foreign keys around as a compound reference.

### 4. Connecting students to courses

Since a student can enroll in many courses, and a course can have many students, this is a **many-to-many relationship**. A many-to-many relationship can't be represented with a simple foreign key on either the `Students` or `Courses` table — it requires a **junction (join) table**, `Enrollments`, that sits between them.

`Enrollments` holds:

- `StudentID` — foreign key referencing `Students.StudentID`
- `CourseID` — foreign key referencing `Courses.CourseID`
  Each row in `Enrollments` represents one student's enrollment in one course. This lets a single student have multiple rows (one per course) and a single course have multiple rows (one per enrolled student), without duplicating student or course data.

### SQL query — list all students enrolled in "Introduction to Programming"

```sql
SELECT Students.FirstName, Students.LastName, Courses.CourseName
FROM Enrollments
JOIN Students ON Enrollments.StudentID = Students.StudentID
JOIN Courses ON Enrollments.CourseID = Courses.CourseID
WHERE Courses.CourseName = 'Introduction to Programming';
```

**My Reasoning:**

- The query starts from `Enrollments` since that's the table that actually links students to courses.
- It joins in `Students` and `Courses` to pull in the human-readable fields (name, course name) that aren't stored in `Enrollments` itself.
- The `WHERE` clause filters on `Courses.CourseName` directly, rather than a hardcoded `CourseID`. Filtering by name is more robust and directly answers what was asked — it doesn't depend on already knowing the numeric ID assigned to "Introduction to Programming".
