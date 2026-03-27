---
name: database-design
description: MongoDB schema design, indexing, and data modeling patterns. Use when designing schemas, optimizing queries, creating indexes, or structuring MongoDB collections. Triggers on "schema", "model", "collection", "index", "MongoDB", "database", "query performance", "aggregation".
user_invocable: true
---

# Database Design (MongoDB)

## Schema Design Principles

### 1. Model for your queries, not your entities
MongoDB is not relational. Design schemas around how your app reads data, not how an ER diagram looks.

### 2. Embed vs Reference

| Embed (subdocument) | Reference (ObjectId) |
|---------------------|---------------------|
| Data read together | Data read independently |
| 1:1 or 1:few | 1:many or many:many |
| Rarely changes | Changes frequently |
| < 16MB total | Can grow unbounded |

**Rule of thumb:** If you always need the data together, embed it. If it lives its own lifecycle, reference it.

### 3. Common Patterns

**Subset Pattern** — Embed only the most recent/relevant items:
```javascript
// User has 10,000 orders but dashboard shows last 5
{
  _id: ObjectId,
  name: "Alice",
  recentOrders: [/* last 5 orders */],  // embedded subset
  // Full orders in separate collection
}
```

**Computed Pattern** — Pre-compute expensive aggregations:
```javascript
{
  _id: ObjectId,
  productId: "abc",
  totalReviews: 342,        // pre-computed
  averageRating: 4.2,       // pre-computed
  // Updated on each new review via $inc
}
```

**Bucket Pattern** — Group time-series data:
```javascript
{
  sensorId: "temp-01",
  date: ISODate("2026-03-17"),
  readings: [
    { time: "08:00", value: 22.1 },
    { time: "08:05", value: 22.3 },
    // ... up to 288 readings per day
  ],
  count: 288,
  avg: 22.4
}
```

## Indexing

### Must-have indexes:
```javascript
// Every query field that appears in find(), sort(), or match stage
db.users.createIndex({ email: 1 }, { unique: true })

// Compound index — order matters (ESR: Equality, Sort, Range)
db.orders.createIndex({ userId: 1, createdAt: -1, status: 1 })

// Text search
db.products.createIndex({ name: "text", description: "text" })

// TTL — auto-delete expired docs
db.sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 })
```

### Index rules:
- Every query should use an index (check with `.explain("executionStats")`)
- Compound indexes: put equality fields first, sort fields second, range fields last
- No more than 5-7 indexes per collection (writes get slower)
- Partial indexes to save space: `{ partialFilterExpression: { status: "active" } }`
- Cover your queries: if the index contains all needed fields, MongoDB skips reading documents

### Checking index usage:
```javascript
db.collection.find(query).explain("executionStats")
// Look for: "stage": "IXSCAN" (good) vs "COLLSCAN" (bad)
// Check: "totalDocsExamined" should be close to "nReturned"
```

## Schema Validation

```javascript
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "passwordHash", "createdAt"],
      properties: {
        email: { bsonType: "string", pattern: "^.+@.+\\..+$" },
        passwordHash: { bsonType: "string", minLength: 60 },
        role: { enum: ["user", "admin", "moderator"] },
        createdAt: { bsonType: "date" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
})
```

## Mongoose Best Practices

```javascript
// Schema with lean defaults and indexes
const userSchema = new Schema({
  email: { type: String, required: true, unique: true, lowercase: true, trim: true },
  passwordHash: { type: String, required: true, select: false },
  profile: {
    name: { type: String, trim: true },
    avatar: String,
  },
  role: { type: String, enum: ['user', 'admin'], default: 'user' },
}, {
  timestamps: true,
  toJSON: { virtuals: true, versionKey: false },
})

// Always use .lean() for read-only queries (5-10x faster)
const users = await User.find({ role: 'admin' }).lean()

// Use projection to fetch only needed fields
const user = await User.findById(id).select('email profile.name role')
```

## Anti-Patterns
- **Unbounded arrays** — Arrays that grow forever (e.g., all user activity). Use bucket pattern or separate collection.
- **Deep nesting** — >3 levels deep is a code smell. Flatten or reference.
- **No indexes** — Every COLLSCAN is a ticking time bomb as data grows.
- **Over-normalizing** — This isn't SQL. Don't create 15 collections for what could be 3 with embedded docs.
- **Ignoring document size** — 16MB limit. If you're close, restructure.

## Migration Strategy
1. Add new fields with defaults (backwards compatible)
2. Write migration script that updates existing docs in batches
3. Never rename fields — add new, migrate data, remove old
4. Use `bulkWrite()` for batch operations (not loops with `updateOne`)
