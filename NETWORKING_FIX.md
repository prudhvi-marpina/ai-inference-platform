# Docker Networking Fix Guide for Windows

## Problem
Container is running and healthy, but can't be accessed from Windows host.

## ✅ What's Already Fixed

1. **Redis Connection**: ✅ Fixed
   - Using `host.docker.internal` to access host Redis
   - Container can now connect to Redis on your host

2. **Container Status**: ✅ Working
   - Container is healthy
   - API works inside container
   - Health checks passing

## 🔧 Solutions for External Access

### Solution 1: Use Browser (Easiest)

**Just open in your browser:**
```
http://localhost:8001/health
http://localhost:8001/docs
http://localhost:8001/api/v1/model
```

Browsers usually work even when PowerShell doesn't!

---

### Solution 2: Restart Docker Desktop

1. Close Docker Desktop completely
2. Restart Docker Desktop
3. Wait for it to fully start
4. Try accessing again

**Why:** Sometimes Docker Desktop networking needs a restart.

---

### Solution 3: Check Port Binding

Verify port is correctly mapped:

```powershell
docker ps --filter "name=ai-api"
```

Should show: `0.0.0.0:8001->8000/tcp`

If not, restart container:
```powershell
docker stop ai-api
docker rm ai-api
docker run -d -p 8001:8000 --name ai-api -e REDIS_URL=redis://host.docker.internal:6379/0 ai-inference-platform
```

---

### Solution 4: Use Docker Compose (Best Solution)

Docker Compose handles networking automatically. This is Step 15, but you can do it now:

```powershell
# Stop current container
docker stop ai-api
docker rm ai-api

# Use Docker Compose (runs everything together)
docker-compose up -d
```

This will:
- Run API container
- Run Redis container
- Connect them automatically
- Fix all networking issues

---

### Solution 5: Check Windows Firewall

1. Open Windows Defender Firewall
2. Check if port 8001 is blocked
3. Allow if needed

Or temporarily disable firewall to test:
```powershell
# Check firewall status
Get-NetFirewallProfile | Select-Object Name, Enabled
```

---

### Solution 6: Use Different Port

Try a different port that's definitely free:

```powershell
docker stop ai-api
docker rm ai-api
docker run -d -p 9000:8000 --name ai-api -e REDIS_URL=redis://host.docker.internal:6379/0 ai-inference-platform
```

Then access: `http://localhost:9000`

---

## Current Status

✅ **Container Running**: Healthy
✅ **Redis Connected**: Using `host.docker.internal`
✅ **API Working**: Inside container
⚠️ **External Access**: PowerShell having issues (browser should work)

---

## Quick Test Commands

### Test from inside container (works):
```powershell
docker exec ai-api python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read().decode())"
```

### Test from browser:
```
http://localhost:8001/health
http://localhost:8001/docs
```

### Check container status:
```powershell
docker ps --filter "name=ai-api"
docker logs ai-api --tail 20
```

---

## Recommended Next Step

**Use Docker Compose (Step 15)** - It handles all networking automatically and is the production-ready solution.

---

## Summary

- ✅ Redis connection: Fixed with `host.docker.internal`
- ✅ Container: Running and healthy
- ⚠️ External access: Try browser first, then Docker Compose


