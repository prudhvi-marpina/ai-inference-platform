# CI/CD Pipeline Documentation

This directory contains GitHub Actions workflows for automated testing and deployment.

## Workflows

### `ci.yml` - Main CI/CD Pipeline

**Triggers:**
- Push to `main` or `master` branch
- Pull requests to `main` or `master`
- Manual trigger (workflow_dispatch)

**What it does:**
1. **Test Job**: Runs all pytest tests
2. **Build Job**: Builds Docker image (only if tests pass)
3. **Optional**: Security scanning, coverage reports

**Jobs:**
- `test`: Runs automated tests
- `build`: Builds Docker image with caching

## How to Use

### 1. Push Code
```bash
git add .
git commit -m "Add new feature"
git push origin main
```

GitHub Actions will automatically:
- Run tests
- Build Docker image
- Report results

### 2. Check Status
- Go to your GitHub repository
- Click "Actions" tab
- See workflow runs and results

### 3. View Logs
- Click on a workflow run
- Click on a job (e.g., "Run Tests")
- See detailed logs

## Configuration

### Enable Docker Registry Push

To push images to Docker Hub or GitHub Container Registry:

1. **Add Secrets** (in GitHub repo settings):
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password/token

2. **Uncomment in `ci.yml`**:
   ```yaml
   - name: Log in to Docker Hub
     uses: docker/login-action@v3
     with:
       username: ${{ secrets.DOCKER_USERNAME }}
       password: ${{ secrets.DOCKER_PASSWORD }}
   ```

3. **Change push to true**:
   ```yaml
   push: true  # Push to registry
   ```

### Enable Test Coverage

1. **Uncomment in `ci.yml`**:
   ```yaml
   - name: Generate coverage report
     run: |
       pip install pytest-cov
       pytest --cov=app --cov-report=xml
   ```

2. **Add Codecov integration** (optional):
   - Sign up at codecov.io
   - Connect your GitHub repo
   - Uncomment Codecov upload step

## Workflow Concepts

### Jobs
- **Independent tasks** that can run in parallel
- Example: `test` and `build` are separate jobs
- `build` depends on `test` (runs only if tests pass)

### Steps
- **Individual actions** within a job
- Run sequentially
- Example: Checkout code → Install dependencies → Run tests

### Actions
- **Reusable components** from GitHub Actions marketplace
- Example: `actions/checkout@v4` downloads your code
- Example: `actions/setup-python@v5` sets up Python

### Secrets
- **Secure storage** for sensitive data
- Example: Docker Hub credentials
- Never hardcode secrets in workflow files!

### Caching
- **Speed up builds** by caching dependencies
- Example: Python packages, Docker layers
- Reduces build time significantly

## Common Workflow Patterns

### Run Tests Only on PRs
```yaml
test:
  if: github.event_name == 'pull_request'
```

### Build Only on Main Branch
```yaml
build:
  if: github.ref == 'refs/heads/main'
```

### Skip CI on Documentation Changes
```yaml
on:
  push:
    paths-ignore:
      - 'docs/**'
      - '*.md'
```

## Troubleshooting

### Tests Fail
- Check test logs in GitHub Actions
- Run tests locally: `pytest -v`
- Fix failing tests before pushing

### Docker Build Fails
- Check Dockerfile syntax
- Verify all files are present
- Check build logs for errors

### Workflow Doesn't Trigger
- Check file paths in `paths:` filter
- Verify branch names match
- Check workflow file syntax (YAML)

## Best Practices

1. **Always run tests before building**
   - Use `needs: test` in build job

2. **Cache dependencies**
   - Use `cache: 'pip'` for Python
   - Use `cache-from` for Docker

3. **Use secrets for credentials**
   - Never hardcode passwords
   - Use GitHub Secrets

4. **Fail fast**
   - Stop on first error
   - Don't continue if tests fail

5. **Keep workflows simple**
   - One job per major task
   - Clear step names
   - Add comments for clarity

## Next Steps

1. **Enable Docker registry push** (if needed)
2. **Add security scanning** (Trivy, Snyk)
3. **Add deployment** (deploy to staging/production)
4. **Add notifications** (Slack, email on failures)

