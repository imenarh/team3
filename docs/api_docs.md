# MoMo Data API Documentation

**Base URL:** `http://localhost:8080`

**Authentication:** All endpoints require HTTP Basic Authentication.

| Username | Password      |
|----------|---------------|
| admin    | momo2026      |

---

## Endpoints

### 1. GET /transactions

Retrieve all transactions.

**Request Example:**

```bash
curl -u admin:momo2026 http://localhost:8080/transactions
```

**Sample Response (200 OK):**

```json
[
  {
    "id": 1,
    "reference_id": "76662021700",
    "amount": 2000,
    "fee": 0,
    "status": "SUCCESS",
    "category": "INCOMING_MONEY",
    "timestamp": "2024-05-10T16:30:51",
    "raw_sms_text": "You have received 2000 RWF from Jane Smith (*********013)..."
  },
  {
    "id": 2,
    "reference_id": "73214484437",
    "amount": 1000,
    "fee": 0,
    "status": "SUCCESS",
    "category": "PAYMENT",
    "timestamp": "2024-05-10T16:31:39",
    "raw_sms_text": "TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith 12845..."
  }
]
```

---

### 2. GET /transactions/{id}

Retrieve a single transaction by its ID.

**Request Example:**

```bash
curl -u admin:momo2026 http://localhost:8080/transactions/1
```

**Sample Response (200 OK):**

```json
{
  "id": 1,
  "reference_id": "76662021700",
  "amount": 2000,
  "fee": 0,
  "status": "SUCCESS",
  "category": "INCOMING_MONEY",
  "timestamp": "2024-05-10T16:30:51",
  "raw_sms_text": "You have received 2000 RWF from Jane Smith (*********013)..."
}
```

**Sample Response (404 Not Found):**

```json
{
  "error": "Transaction not found"
}
```

---

### 3. POST /transactions

Create a new transaction. All fields are required.

**Required Fields:**

| Field          | Type   | Description                        |
|----------------|--------|------------------------------------|
| reference_id   | string | Unique transaction reference       |
| amount         | number | Transaction amount in RWF          |
| fee            | number | Transaction fee in RWF             |
| status         | string | Transaction status (e.g. SUCCESS)  |
| category       | string | Transaction type (e.g. P2P, CASH_OUT) |
| timestamp      | string | Date/time of the transaction       |
| raw_sms_text   | string | Original SMS text                  |

**Request Example:**

```bash
curl -u admin:momo2026 -X POST http://localhost:8080/transactions \
  -H "Content-Type: application/json" \
  -d '{"reference_id": "51732411227", "amount": 600, "fee": 0, "status": "SUCCESS", "category": "PAYMENT", "timestamp": "2024-05-10T21:32:32", "raw_sms_text": "TxId: 51732411227. Your payment of 600 RWF to Samuel Carter 95464..."}'
```

**Sample Response (201 Created):**

```json
{
  "id": 3,
  "reference_id": "51732411227",
  "amount": 600,
  "fee": 0,
  "status": "SUCCESS",
  "category": "PAYMENT",
  "timestamp": "2024-05-10T21:32:32",
  "raw_sms_text": "TxId: 51732411227. Your payment of 600 RWF to Samuel Carter 95464..."
}
```

**Sample Response (400 Bad Request):**

```json
{
  "error": "Missing fields: fee, category"
}
```

---

### 4. PUT /transactions/{id}

Update an existing transaction. All fields are required.

**Request Example:**

```bash
curl -u admin:momo2026 -X PUT http://localhost:8080/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{"reference_id": "76662021700", "amount": 3000, "fee": 10, "status": "SUCCESS", "category": "INCOMING_MONEY", "timestamp": "2024-05-10T16:30:51", "raw_sms_text": "You have received 3000 RWF from Jane Smith (*********013)..."}'
```

**Sample Response (200 OK):**

```json
{
  "id": 1,
  "reference_id": "76662021700",
  "amount": 3000,
  "fee": 10,
  "status": "SUCCESS",
  "category": "INCOMING_MONEY",
  "timestamp": "2024-05-10T16:30:51",
  "raw_sms_text": "You have received 3000 RWF from Jane Smith (*********013)..."
}
```

**Sample Response (400 Bad Request):**

```json
{
  "error": "Missing fields: amount"
}
```

**Sample Response (404 Not Found):**

```json
{
  "error": "Transaction not found"
}
```

---

### 5. DELETE /transactions/{id}

Delete a transaction by its ID.

**Request Example:**

```bash
curl -u admin:momo2026 -X DELETE http://localhost:8080/transactions/1
```

**Sample Response (200 OK):**

```json
{
  "message": "Transaction 1 deleted"
}
```

**Sample Response (404 Not Found):**

```json
{
  "error": "Transaction not found"
}
```

---

## Error Codes Summary

| Code | Meaning               | When It Occurs                              |
|------|-----------------------|---------------------------------------------|
| 200  | OK                    | Successful GET, PUT, or DELETE               |
| 201  | Created               | Successful POST (new transaction created)    |
| 400  | Bad Request           | Missing required fields in POST or PUT body  |
| 401  | Unauthorized          | Missing or invalid authentication credentials|
| 404  | Not Found             | Transaction ID does not exist or invalid path|
