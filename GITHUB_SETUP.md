# Setting Up GitHub Repository - Step by Step Guide

## Overview
This guide will help you:
1. Commit your code locally
2. Create a GitHub repository
3. Push your code to GitHub
4. Enable CI/CD workflow

---

## Step 1: Commit Your Code Locally

### 1.1 Add All Files
```powershell
git add .
```

### 1.2 Create Initial Commit
```powershell
git commit -m "Initial commit: AI Inference Platform with CI/CD"
```

### 1.3 Verify Commit
```powershell
git log
```

You should see your commit listed.

---

## Step 2: Create GitHub Repository

### Option A: Using GitHub Website (Recommended for Beginners)

1. **Go to GitHub:**
   - Visit: https://github.com/new
   - Or: Click your profile → "+" → "New repository"

2. **Repository Settings:**
   - **Repository name:** `ai-inference-platform`
   - **Description:** `Production AI Inference Platform with Observability & Auto-Scaling`
   - **Visibility:** 
     - ✅ **Public** (if you want to show it on your profile)
     - ✅ **Private** (if you want to keep it private)
   - **DO NOT** check:
     - ❌ "Add a README file" (you already have one)
     - ❌ "Add .gitignore" (you already have one)
     - ❌ "Choose a license" (optional, can add later)

3. **Click "Create repository"**

4. **Copy the repository URL:**
   - You'll see: `https://github.com/prudhvi-marpina/ai-inference-platform.git`
   - Copy this URL

### Option B: Using GitHub CLI (Advanced)

If you have GitHub CLI installed:
```powershell
gh repo create ai-inference-platform --public --source=. --remote=origin --push
```

---

## Step 3: Connect Local Repository to GitHub

### 3.1 Add Remote Repository
```powershell
git remote add origin https://github.com/prudhvi-marpina/ai-inference-platform.git
```

**Replace `prudhvi-marpina` with your GitHub username if different!**

### 3.2 Verify Remote
```powershell
git remote -v
```

You should see:
```
origin  https://github.com/prudhvi-marpina/ai-inference-platform.git (fetch)
origin  https://github.com/prudhvi-marpina/ai-inference-platform.git (push)
```

### 3.3 Rename Branch to Main (if needed)
```powershell
git branch -M main
```

---

## Step 4: Push Code to GitHub

### 4.1 Push to GitHub
```powershell
git push -u origin main
```

**You'll be prompted for credentials:**
- **Username:** Your GitHub username (`prudhvi-marpina`)
- **Password:** Use a **Personal Access Token** (not your GitHub password)

### 4.2 Create Personal Access Token (if needed)

If you don't have a token:

1. **Go to GitHub Settings:**
   - Click your profile picture → Settings
   - Or: https://github.com/settings/tokens

2. **Create Token:**
   - Click "Developer settings" (left sidebar)
   - Click "Personal access tokens" → "Tokens (classic)"
   - Click "Generate new token" → "Generate new token (classic)"

3. **Token Settings:**
   - **Note:** `ai-inference-platform-push`
   - **Expiration:** 90 days (or your preference)
   - **Scopes:** Check `repo` (full control of private repositories)

4. **Generate and Copy Token:**
   - Click "Generate token"
   - **IMPORTANT:** Copy the token immediately (you won't see it again!)
   - Use this token as your password when pushing

---

## Step 5: Verify Push

### 5.1 Check GitHub
- Go to: https://github.com/prudhvi-marpina/ai-inference-platform
- You should see all your files!

### 5.2 Check CI/CD
- Click "Actions" tab
- You should see the workflow running (or completed)
- Green checkmark = Success! ✅

---

## Step 6: Future Updates

### To push future changes:

```powershell
# 1. Check what changed
git status

# 2. Add changes
git add .

# 3. Commit changes
git commit -m "Description of changes"

# 4. Push to GitHub
git push
```

**CI/CD will automatically run on every push!**

---

## Troubleshooting

### Problem: "remote origin already exists"

**Solution:**
```powershell
git remote remove origin
git remote add origin https://github.com/prudhvi-marpina/ai-inference-platform.git
```

### Problem: "Authentication failed"

**Solution:**
- Use Personal Access Token, not password
- Make sure token has `repo` scope
- Token might be expired (create new one)

### Problem: "Permission denied"

**Solution:**
- Check repository name matches
- Check you have access to the repository
- Verify your GitHub username

### Problem: "Branch 'main' does not exist"

**Solution:**
```powershell
git branch -M main
git push -u origin main
```

---

## Quick Reference

### Initial Setup (One Time)
```powershell
git add .
git commit -m "Initial commit: AI Inference Platform"
git remote add origin https://github.com/prudhvi-marpina/ai-inference-platform.git
git branch -M main
git push -u origin main
```

### Regular Updates
```powershell
git add .
git commit -m "Your commit message"
git push
```

---

## What Happens After Push

1. **Code is on GitHub** ✅
2. **CI/CD workflow triggers automatically** ✅
3. **Tests run** ✅
4. **Docker image builds** ✅
5. **You get results in GitHub Actions** ✅

---

## Next Steps

After pushing:
1. ✅ Check GitHub repository (all files visible)
2. ✅ Check Actions tab (workflow running)
3. ✅ Wait for green checkmark (all tests passed)
4. ✅ Celebrate! 🎉

---

## Security Notes

### ⚠️ Important:
- **Never commit `.env` file** (already in `.gitignore`)
- **Never commit secrets** (passwords, API keys)
- **Use Personal Access Tokens** for authentication
- **Keep tokens secure** (don't share them)

---

## Summary

1. ✅ Commit code locally
2. ✅ Create GitHub repository
3. ✅ Connect local to GitHub
4. ✅ Push code
5. ✅ CI/CD runs automatically

Your code is now on GitHub and CI/CD is active! 🚀

