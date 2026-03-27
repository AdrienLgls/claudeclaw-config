---
name: security-auditor
description: Security audit checklist for web applications. Use when reviewing security, checking for vulnerabilities, auditing auth, or hardening an app. Triggers on "security", "vulnerability", "audit securite", "OWASP", "XSS", "injection", "auth bypass".
user_invocable: true
---

# Security Auditor

Run this checklist against the target application. Flag issues by severity: CRITICAL / HIGH / MEDIUM / LOW.

## 1. Authentication & Session Management

- [ ] Passwords hashed with bcrypt/argon2 (NOT md5/sha1/sha256)
- [ ] JWT tokens: short expiry, httpOnly cookie, secure flag, sameSite
- [ ] No secrets in client-side code or git history
- [ ] Rate limiting on login/register/reset endpoints
- [ ] Account lockout after N failed attempts
- [ ] Session invalidation on password change
- [ ] CSRF protection on state-changing endpoints

## 2. Authorization

- [ ] Every API endpoint checks user permissions (not just auth)
- [ ] No IDOR — users can't access other users' data by changing IDs
- [ ] Admin routes protected server-side (not just hidden in UI)
- [ ] Role checks on both frontend AND backend
- [ ] File upload paths don't allow directory traversal

## 3. Input Validation & Injection

- [ ] All user input validated server-side (never trust the client)
- [ ] SQL/NoSQL injection: parameterized queries, no string concatenation
- [ ] XSS: output encoding, Content-Security-Policy header
- [ ] Command injection: no `exec()` / `eval()` with user input
- [ ] Path traversal: sanitize file paths, no `../` allowed
- [ ] Prototype pollution: `Object.freeze`, no `__proto__` access
- [ ] ReDoS: no complex regex on user input

## 4. API Security

- [ ] CORS configured restrictively (not `*`)
- [ ] Rate limiting on all public endpoints
- [ ] Request size limits (body parser limits)
- [ ] No sensitive data in URL query strings (use POST body)
- [ ] API versioning strategy
- [ ] Error messages don't leak stack traces or internal paths
- [ ] Helmet.js or equivalent security headers

## 5. Data Protection

- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced (HSTS header)
- [ ] No secrets in `.env` committed to git
- [ ] `.gitignore` covers: `.env`, `node_modules`, `*.pem`, `*.key`
- [ ] PII handling compliant with privacy requirements
- [ ] Database backups encrypted

## 6. Dependencies

- [ ] `npm audit` / `pnpm audit` — 0 critical/high vulnerabilities
- [ ] No outdated packages with known CVEs
- [ ] Lock file (`pnpm-lock.yaml`) committed
- [ ] No unnecessary dependencies

## 7. Infrastructure

- [ ] MongoDB: authentication enabled, no public exposure
- [ ] Docker: non-root user, minimal base image, no secrets in Dockerfile
- [ ] Nginx: security headers, rate limiting, SSL config grade A+
- [ ] PM2: log rotation, error handling
- [ ] Firewall: only necessary ports open

## Output Format

```
## Security Audit Report — [App Name]
Date: [date]

### CRITICAL (fix immediately)
- [finding]

### HIGH (fix this sprint)
- [finding]

### MEDIUM (fix this month)
- [finding]

### LOW (tech debt)
- [finding]

### PASSED
- [list of checks that passed]
```

## Rules
- NEVER run actual exploits against production systems
- Flag potential issues even if you can't confirm exploitability
- Check git history for accidentally committed secrets: `git log --all -p | grep -i "password\|secret\|key\|token"`
- Always recommend the fix, not just the problem
