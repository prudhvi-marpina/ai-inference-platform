# ============================================================================
# AI Inference Platform - Comprehensive Test Script
# ============================================================================
# This script tests all endpoints of the AI Inference Platform
# Run this after starting the server: uvicorn app.main:app --reload
# ============================================================================

param(
    [string]$baseUrl = "http://localhost:8000"  # Can change URL if needed
)

# Colors for output
$successColor = "Green"
$errorColor = "Red"
$warningColor = "Yellow"
$infoColor = "Cyan"

# Track test results
$testsPassed = 0
$testsFailed = 0
$testsTotal = 0

# Function to run a test
function Test-Endpoint {
    param(
        [string]$name,
        [string]$method,
        [string]$uri,
        [object]$body = $null,
        [scriptblock]$validator = $null
    )
    
    $script:testsTotal++
    Write-Host "`n$($script:testsTotal). Testing $name..." -ForegroundColor $infoColor
    
    try {
        $params = @{
            Uri = "$baseUrl$uri"
            Method = $method
        }
        
        if ($body) {
            $params.ContentType = "application/json"
            $params.Body = ($body | ConvertTo-Json)
        }
        
        $result = Invoke-RestMethod @params
        
        if ($validator) {
            $isValid = & $validator $result
            if ($isValid) {
                Write-Host "   ✅ Passed" -ForegroundColor $successColor
                $script:testsPassed++
                return $result
            } else {
                Write-Host "   ❌ Failed: Validation failed" -ForegroundColor $errorColor
                $script:testsFailed++
                return $null
            }
        } else {
            Write-Host "   ✅ Passed" -ForegroundColor $successColor
            $script:testsPassed++
            return $result
        }
    } catch {
        Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor $errorColor
        $script:testsFailed++
        return $null
    }
}

# ============================================================================
# START TESTS
# ============================================================================

Write-Host "`n========================================" -ForegroundColor $successColor
Write-Host "  AI Inference Platform Test Suite" -ForegroundColor $successColor
Write-Host "  Base URL: $baseUrl" -ForegroundColor $infoColor
Write-Host "========================================`n" -ForegroundColor $successColor

# Test 1: Health Check
$health = Test-Endpoint -name "Health Endpoint" -method "GET" -uri "/health" -validator {
    param($result)
    return $result.status -eq "healthy"
}
if ($health) {
    Write-Host "   Status: $($health.status)" -ForegroundColor $successColor
}

# Test 2: Root Endpoint
$root = Test-Endpoint -name "Root Endpoint" -method "GET" -uri "/"

# Test 3: Model Info
$modelInfo = Test-Endpoint -name "Model Info" -method "GET" -uri "/api/v1/model" -validator {
    param($result)
    return ($result.model_name -and $result.model_version)
}
if ($modelInfo) {
    Write-Host "   Model: $($modelInfo.model_name) v$($modelInfo.model_version)" -ForegroundColor $successColor
}

# Test 4: Inference - First Request (Cache Miss)
Write-Host "`n--- Testing Cache Functionality ---" -ForegroundColor $infoColor

$inferenceBody = @{
    prompt = "What is artificial intelligence?"
    max_tokens = 100
    temperature = 0.7
}

$start1 = Get-Date
$inference1 = Test-Endpoint -name "Inference (First Request - Cache Miss)" -method "POST" -uri "/api/v1/infer" -body $inferenceBody -validator {
    param($result)
    return ($result.output -and $result.tokens_used -and $result.model_version)
}
$duration1 = (Get-Date) - $start1

if ($inference1) {
    Write-Host "   Response time: $([math]::Round($duration1.TotalMilliseconds, 2))ms" -ForegroundColor $successColor
    Write-Host "   Tokens used: $($inference1.tokens_used)" -ForegroundColor $successColor
}

# Test 5: Inference - Second Request (Cache Hit)
$start2 = Get-Date
$inference2 = Test-Endpoint -name "Inference (Second Request - Cache Hit)" -method "POST" -uri "/api/v1/infer" -body $inferenceBody -validator {
    param($result)
    return ($result.output -and $result.tokens_used -and $result.model_version)
}
$duration2 = (Get-Date) - $start2

if ($inference2) {
    Write-Host "   Response time: $([math]::Round($duration2.TotalMilliseconds, 2))ms" -ForegroundColor $successColor
    Write-Host "   Tokens used: $($inference2.tokens_used)" -ForegroundColor $successColor
    
    # Compare speeds
    if ($duration2 -lt $duration1) {
        $speedup = [math]::Round(($duration1.TotalMilliseconds / $duration2.TotalMilliseconds), 2)
        Write-Host "   ✅ Cache hit confirmed! ($speedup`x faster)" -ForegroundColor $successColor
    } else {
        Write-Host "   ⚠️  Cache may not be working (similar speed)" -ForegroundColor $warningColor
    }
}

# Test 6: Metrics Endpoint
$metrics = Test-Endpoint -name "Metrics Endpoint" -method "GET" -uri "/metrics"
if ($metrics) {
    $metricsContent = (Invoke-WebRequest -Uri "$baseUrl/metrics").Content
    
    $checks = @(
        @{name="Cache Hits"; pattern="cache_hits_total"},
        @{name="Cache Misses"; pattern="cache_misses_total"},
        @{name="Inference Requests"; pattern="inference_requests_total"},
        @{name="Request Duration"; pattern="http_request_duration_seconds"}
    )
    
    foreach ($check in $checks) {
        if ($metricsContent -match $check.pattern) {
            Write-Host "   ✅ $($check.name) metrics found" -ForegroundColor $successColor
        } else {
            Write-Host "   ⚠️  $($check.name) metrics not found" -ForegroundColor $warningColor
        }
    }
}

# Test 7: Rate Limiting (Optional - makes 11 requests)
Write-Host "`n--- Testing Rate Limiting ---" -ForegroundColor $infoColor
Write-Host "   Making 11 requests to test rate limit (limit: 10/minute)..." -ForegroundColor $infoColor

$rateLimitPassed = 0
$rateLimitBlocked = 0

for ($i = 1; $i -le 11; $i++) {
    try {
        $testBody = @{
            prompt = "Test request $i"
            max_tokens = 10
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "$baseUrl/api/v1/infer" -Method POST -ContentType "application/json" -Body $testBody -ErrorAction Stop
        $rateLimitPassed++
        Write-Host "   Request $i : ✅ Allowed" -ForegroundColor $successColor
    } catch {
        if ($_.Exception.Response.StatusCode -eq 429) {
            $rateLimitBlocked++
            Write-Host "   Request $i : 🚫 Rate Limited (429)" -ForegroundColor $warningColor
        } else {
            Write-Host "   Request $i : ❌ Error: $($_.Exception.Message)" -ForegroundColor $errorColor
        }
    }
    Start-Sleep -Milliseconds 100  # Small delay between requests
}

if ($rateLimitBlocked -gt 0) {
    Write-Host "   ✅ Rate limiting working ($rateLimitBlocked request(s) blocked)" -ForegroundColor $successColor
} else {
    Write-Host "   ⚠️  Rate limiting may not be working (no requests blocked)" -ForegroundColor $warningColor
}

# ============================================================================
# TEST SUMMARY
# ============================================================================

Write-Host "`n========================================" -ForegroundColor $successColor
Write-Host "  Test Summary" -ForegroundColor $successColor
Write-Host "========================================" -ForegroundColor $successColor
Write-Host "  Total Tests: $testsTotal" -ForegroundColor $infoColor
Write-Host "  Passed: $testsPassed" -ForegroundColor $successColor
Write-Host "  Failed: $testsFailed" -ForegroundColor $(if ($testsFailed -eq 0) { $successColor } else { $errorColor })
Write-Host "========================================`n" -ForegroundColor $successColor

if ($testsFailed -eq 0) {
    Write-Host "🎉 All tests passed!" -ForegroundColor $successColor
    exit 0
} else {
    Write-Host "❌ Some tests failed. Please check the output above." -ForegroundColor $errorColor
    exit 1
}

