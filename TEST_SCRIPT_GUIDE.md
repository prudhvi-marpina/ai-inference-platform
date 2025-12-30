# Complete Beginner's Guide to Writing Test Scripts

## What is a Test Script?

A test script is a program that automatically tests your application to make sure it works correctly. Think of it as a robot that clicks buttons and checks results for you.

---

## Why Write Test Scripts?

### 1. **Saves Time**
- Manual testing: 10 minutes
- Script testing: 10 seconds

### 2. **Finds Bugs Early**
- Catch problems before users do
- Test after every code change

### 3. **Consistent**
- Same tests every time
- No human mistakes

### 4. **Documentation**
- Shows how your API works
- Examples for other developers

---

## General Structure of a Test Script

Every test script follows this pattern:

```
1. Setup (prepare for testing)
2. Run Tests (test each feature)
3. Check Results (verify it worked)
4. Report (show what happened)
```

---

## PowerShell Basics for Testing

### 1. Making HTTP Requests

**GET Request (read data):**
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
```

**POST Request (send data):**
```powershell
$body = @{
    name = "John"
    age = 30
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/users" -Method POST -ContentType "application/json" -Body $body
```

### 2. Displaying Output

```powershell
Write-Host "Hello World"                    # Basic output
Write-Host "Success!" -ForegroundColor Green   # Colored output
Write-Host "Error!" -ForegroundColor Red
```

### 3. Variables

```powershell
$name = "John"              # Store value
$age = 30                   # Store number
$result = $name + " is " + $age  # Use variables
```

### 4. Conditions (if/else)

```powershell
if ($result.status -eq "ok") {
    Write-Host "✅ Success"
} else {
    Write-Host "❌ Failed"
}
```

### 5. Measuring Time

```powershell
$start = Get-Date
# ... do something ...
$duration = (Get-Date) - $start
Write-Host "Took $($duration.TotalMilliseconds)ms"
```

---

## Step-by-Step: Our Test Script Explained

### Line 1-2: Header
```powershell
# Quick test script for Step 13
Write-Host "=== Testing AI Inference Platform ===" -ForegroundColor Green
```
**What it does:** Shows a title when script starts
**Why:** Makes output clear and organized

---

### Line 4-7: Test 1 - Health Check
```powershell
Write-Host "`n1. Testing Health Endpoint..." -ForegroundColor Yellow
$health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
Write-Host "   Status: $($health.status)" -ForegroundColor Green
```

**Breaking it down:**
- `Write-Host "`n1. Testing..."` - Shows test number (`\n` = new line)
- `$health = Invoke-RestMethod...` - Makes GET request, stores result
- `$health.status` - Gets the "status" field from response
- `Write-Host "Status: ..."` - Displays the result

**What it tests:** Is the API running?
**Expected result:** `Status: healthy`

---

### Line 9-12: Test 2 - Model Info
```powershell
Write-Host "`n2. Testing Model Info Endpoint..." -ForegroundColor Yellow
$modelInfo = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/model" -Method GET
Write-Host "   Model: $($modelInfo.model_name) v$($modelInfo.model_version)" -ForegroundColor Green
```

**Breaking it down:**
- Same pattern as Test 1
- Gets model information
- Displays model name and version

**What it tests:** Does model service work?
**Expected result:** `Model: default-model v1.0.0`

---

### Line 14-26: Test 3 - First Inference Request
```powershell
Write-Host "`n3. Testing Inference (First Request - Cache Miss)..." -ForegroundColor Yellow
$body = @{
    prompt = "What is AI?"
    max_tokens = 100
    temperature = 0.7
} | ConvertTo-Json

$start = Get-Date
$result1 = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/infer" -Method POST -ContentType "application/json" -Body $body
$duration1 = (Get-Date) - $start
Write-Host "   Response received in $($duration1.TotalMilliseconds)ms" -ForegroundColor Green
Write-Host "   Tokens used: $($result1.tokens_used)" -ForegroundColor Cyan
```

**Breaking it down:**

**Line 16-20: Create request body**
```powershell
$body = @{
    prompt = "What is AI?"
    max_tokens = 100
    temperature = 0.7
} | ConvertTo-Json
```
- `@{...}` - Creates a hashtable (dictionary)
- `| ConvertTo-Json` - Converts to JSON string
- Result: `{"prompt":"What is AI?","max_tokens":100,"temperature":0.7}`

**Line 22: Start timer**
```powershell
$start = Get-Date
```
- Records current time

**Line 23: Make POST request**
```powershell
$result1 = Invoke-RestMethod -Uri "..." -Method POST -ContentType "application/json" -Body $body
```
- `-Method POST` - POST request (sends data)
- `-ContentType "application/json"` - Tells server it's JSON
- `-Body $body` - The data to send

**Line 24: Calculate duration**
```powershell
$duration1 = (Get-Date) - $start
```
- Current time minus start time = how long it took

**Line 25-26: Display results**
```powershell
Write-Host "   Response received in $($duration1.TotalMilliseconds)ms"
Write-Host "   Tokens used: $($result1.tokens_used)"
```
- Shows time taken
- Shows tokens used from response

**What it tests:** Does inference work? How fast?
**Expected result:** Response with output, ~100ms, tokens used

---

### Line 28-40: Test 4 - Second Request (Cache Test)
```powershell
Write-Host "`n4. Testing Inference (Second Request - Cache Hit)..." -ForegroundColor Yellow
$start = Get-Date
$result2 = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/infer" -Method POST -ContentType "application/json" -Body $body
$duration2 = (Get-Date) - $start
Write-Host "   Response received in $($duration2.TotalMilliseconds)ms" -ForegroundColor Green
Write-Host "   Tokens used: $($result2.tokens_used)" -ForegroundColor Cyan

if ($duration2 -lt $duration1) {
    Write-Host "   ✅ Cache hit confirmed (faster response)!" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Cache may not be working (similar speed)" -ForegroundColor Yellow
}
```

**Breaking it down:**
- Same request as Test 3 (uses same `$body`)
- Measures time again
- Compares: Is second request faster?

**Line 36-40: Compare speeds**
```powershell
if ($duration2 -lt $duration1) {
    # Second is faster = cache worked!
} else {
    # Similar speed = cache might not work
}
```
- `-lt` means "less than"
- If second is faster → cache hit ✅
- If similar → cache might not work ⚠️

**What it tests:** Does caching work?
**Expected result:** Second request is faster (cache hit)

---

### Line 42-55: Test 5 - Metrics Check
```powershell
Write-Host "`n5. Checking Metrics..." -ForegroundColor Yellow
$metrics = Invoke-WebRequest -Uri "http://localhost:8000/metrics" -Method GET
$metricsContent = $metrics.Content

if ($metricsContent -match "cache_hits_total") {
    Write-Host "   ✅ Cache metrics found" -ForegroundColor Green
}
if ($metricsContent -match "cache_misses_total") {
    Write-Host "   ✅ Cache miss metrics found" -ForegroundColor Green
}
if ($metricsContent -match "inference_requests_total") {
    Write-Host "   ✅ Inference metrics found" -ForegroundColor Green
}
```

**Breaking it down:**

**Line 44: Get metrics**
```powershell
$metrics = Invoke-WebRequest -Uri "http://localhost:8000/metrics" -Method GET
```
- `Invoke-WebRequest` (not RestMethod) - Gets raw text
- Metrics endpoint returns text, not JSON

**Line 45: Get content**
```powershell
$metricsContent = $metrics.Content
```
- Extracts the text content

**Line 47-55: Check for keywords**
```powershell
if ($metricsContent -match "cache_hits_total") {
    Write-Host "✅ Cache metrics found"
}
```
- `-match` - Searches for text in string
- If found → metrics are working ✅

**What it tests:** Are metrics being collected?
**Expected result:** All three metrics found ✅

---

## How to Write Test Scripts for ANY Project

### Step 1: Identify What to Test

Ask yourself:
- What are the main features?
- What should work correctly?
- What could break?

**Example for a blog API:**
- Create post
- Get post
- Update post
- Delete post
- List all posts

---

### Step 2: Write Test for Each Feature

**Template:**
```powershell
# Test: [Feature Name]
Write-Host "`nTesting [Feature]..." -ForegroundColor Yellow

# Prepare test data
$testData = @{
    field1 = "value1"
    field2 = "value2"
} | ConvertTo-Json

# Make request
$result = Invoke-RestMethod -Uri "http://localhost:8000/endpoint" -Method POST -ContentType "application/json" -Body $testData

# Check result
if ($result.status -eq "success") {
    Write-Host "   ✅ Passed" -ForegroundColor Green
} else {
    Write-Host "   ❌ Failed" -ForegroundColor Red
}
```

---

### Step 3: Add Error Handling

**Better version:**
```powershell
try {
    $result = Invoke-RestMethod -Uri "http://localhost:8000/endpoint" -Method GET
    Write-Host "   ✅ Success: $($result.message)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}
```

**What `try/catch` does:**
- `try` - Try to run code
- `catch` - If error happens, handle it gracefully
- Prevents script from crashing

---

## Examples for Different Projects

### Example 1: E-Commerce API

```powershell
# Test: Create Product
Write-Host "`n1. Testing Create Product..." -ForegroundColor Yellow
$product = @{
    name = "Laptop"
    price = 999.99
    category = "Electronics"
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://localhost:8000/products" -Method POST -ContentType "application/json" -Body $product
Write-Host "   Product ID: $($result.id)" -ForegroundColor Green

# Test: Get Product
Write-Host "`n2. Testing Get Product..." -ForegroundColor Yellow
$product = Invoke-RestMethod -Uri "http://localhost:8000/products/$($result.id)" -Method GET
Write-Host "   Product: $($product.name) - $($product.price)" -ForegroundColor Green

# Test: Add to Cart
Write-Host "`n3. Testing Add to Cart..." -ForegroundColor Yellow
$cartItem = @{
    product_id = $result.id
    quantity = 2
} | ConvertTo-Json

$cart = Invoke-RestMethod -Uri "http://localhost:8000/cart" -Method POST -ContentType "application/json" -Body $cartItem
Write-Host "   Cart total: $($cart.total)" -ForegroundColor Green
```

---

### Example 2: User Authentication API

```powershell
# Test: Register User
Write-Host "`n1. Testing User Registration..." -ForegroundColor Yellow
$user = @{
    email = "test@example.com"
    password = "SecurePass123"
    name = "Test User"
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://localhost:8000/register" -Method POST -ContentType "application/json" -Body $user
Write-Host "   User ID: $($result.user_id)" -ForegroundColor Green

# Test: Login
Write-Host "`n2. Testing Login..." -ForegroundColor Yellow
$login = @{
    email = "test@example.com"
    password = "SecurePass123"
} | ConvertTo-Json

$auth = Invoke-RestMethod -Uri "http://localhost:8000/login" -Method POST -ContentType "application/json" -Body $login
$token = $auth.token
Write-Host "   Token received: $($token.Substring(0, 20))..." -ForegroundColor Green

# Test: Get Profile (with token)
Write-Host "`n3. Testing Get Profile..." -ForegroundColor Yellow
$headers = @{
    Authorization = "Bearer $token"
}
$profile = Invoke-RestMethod -Uri "http://localhost:8000/profile" -Method GET -Headers $headers
Write-Host "   Profile: $($profile.name) - $($profile.email)" -ForegroundColor Green
```

---

### Example 3: File Upload API

```powershell
# Test: Upload File
Write-Host "`n1. Testing File Upload..." -ForegroundColor Yellow

# Create a test file
$testContent = "This is a test file"
$testFile = "test.txt"
$testContent | Out-File $testFile

# Upload file
$form = @{
    file = Get-Item $testFile
}
$result = Invoke-RestMethod -Uri "http://localhost:8000/upload" -Method POST -Form $form
Write-Host "   File ID: $($result.file_id)" -ForegroundColor Green

# Cleanup
Remove-Item $testFile
```

---

## Common Patterns

### Pattern 1: Test Sequence (Create → Read → Update → Delete)

```powershell
# 1. Create
$item = Invoke-RestMethod -Uri "http://localhost:8000/items" -Method POST -Body $data
$id = $item.id

# 2. Read
$read = Invoke-RestMethod -Uri "http://localhost:8000/items/$id" -Method GET

# 3. Update
$update = Invoke-RestMethod -Uri "http://localhost:8000/items/$id" -Method PUT -Body $newData

# 4. Delete
Invoke-RestMethod -Uri "http://localhost:8000/items/$id" -Method DELETE
```

---

### Pattern 2: Performance Testing

```powershell
Write-Host "`nPerformance Test..." -ForegroundColor Yellow

$times = @()
for ($i = 1; $i -le 10; $i++) {
    $start = Get-Date
    Invoke-RestMethod -Uri "http://localhost:8000/endpoint" -Method GET
    $duration = (Get-Date) - $start
    $times += $duration.TotalMilliseconds
}

$average = ($times | Measure-Object -Average).Average
$min = ($times | Measure-Object -Minimum).Minimum
$max = ($times | Measure-Object -Maximum).Maximum

Write-Host "   Average: $average ms" -ForegroundColor Green
Write-Host "   Min: $min ms" -ForegroundColor Green
Write-Host "   Max: $max ms" -ForegroundColor Green
```

---

### Pattern 3: Validation Testing

```powershell
# Test: Invalid Input
Write-Host "`nTesting Invalid Input..." -ForegroundColor Yellow
$invalid = @{
    email = "not-an-email"  # Invalid email
    age = -5                 # Invalid age (negative)
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "http://localhost:8000/users" -Method POST -Body $invalid
    Write-Host "   ❌ Should have failed!" -ForegroundColor Red
} catch {
    if ($_.Exception.Response.StatusCode -eq 400) {
        Write-Host "   ✅ Correctly rejected invalid input" -ForegroundColor Green
    }
}
```

---

## Tips for Writing Good Test Scripts

### 1. **Use Clear Names**
```powershell
# Good
$userResponse = Invoke-RestMethod ...

# Bad
$x = Invoke-RestMethod ...
```

### 2. **Add Comments**
```powershell
# Test user registration with valid data
$user = @{...}
```

### 3. **Handle Errors**
```powershell
try {
    # Test code
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
```

### 4. **Use Colors**
```powershell
Write-Host "✅ Success" -ForegroundColor Green
Write-Host "❌ Failed" -ForegroundColor Red
Write-Host "⚠️ Warning" -ForegroundColor Yellow
```

### 5. **Organize Tests**
```powershell
# Group related tests
Write-Host "`n=== User Tests ===" -ForegroundColor Cyan
# ... user tests ...

Write-Host "`n=== Product Tests ===" -ForegroundColor Cyan
# ... product tests ...
```

---

## Running Your Test Script

### Method 1: Direct Execution
```powershell
.\test_endpoints.ps1
```

### Method 2: With Parameters
```powershell
# Script with parameters
param(
    [string]$baseUrl = "http://localhost:8000"
)

Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
```

Run with:
```powershell
.\test_endpoints.ps1 -baseUrl "http://localhost:9000"
```

---

## Summary

**Test Script Structure:**
1. Header (title)
2. Test 1 (feature 1)
3. Test 2 (feature 2)
4. ... more tests ...
5. Summary

**Key Commands:**
- `Invoke-RestMethod` - Make HTTP requests
- `Write-Host` - Display output
- `Get-Date` - Measure time
- `if/else` - Check conditions
- `try/catch` - Handle errors

**Best Practices:**
- Clear test names
- Add comments
- Handle errors
- Use colors
- Organize tests

Now you can write test scripts for any project! 🎉

