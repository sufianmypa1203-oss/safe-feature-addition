---
name: safe-feature-addition
description: Elite guide for shipping features without breaking production. Implements "Additive over Destructive" development, Unified Safety Auditing, and Feature Flags.
version: 3.0.0
author: sufianmypa1203-oss
quality_score: 100
triggers:
  - "how to add feature safely"
  - "don't break production"
  - "feature flags"
  - "safe rollout"
---

# 🛡️ Safe Feature Addition: Ship Without Breaking

## What This Does

This skill provides an **Elite-Grade Safety Net** for adding new features to production systems. It implements an **"Additive Development"** philosophy where new code lives alongside old code, protected by feature flags and gradual rollouts.

> [!IMPORTANT]
> **The Golden Rule:** Always favor *additive* changes over *destructive* modifications. Existing code should remain untouched and functional.

---

## 🏗️ The Production Toolkit

This skill is powered by a unified safety engine located in `production/safe-feature-addition/`:

| Tool | Purpose |
|------|---------|
| `safe-feature verify` | Ensures all flags in code are defined in config. |
| `safe-feature audit` | Scans git diff for destructive changes (signature breaks). |
| `feature-flags.yml` | Central configuration for feature toggles. |

---

## 🚀 Step 1: Additive Development

Instead of changing an existing function, extend it or create a new one.

```javascript
// ❌ DESTRUCTIVE - Breaks existing callers
function processPayment(amount) {
  return crypto(amount); 
}

// ✅ ELITE & ADDITIVE - Backward compatible
function processPayment(amount, method = 'credit-card') {
  if (method === 'crypto') return crypto(amount);
  return legacyPayment(amount);
}
```

---

## 🚩 Step 2: Feature Flags (The Kill Switch)

Wrap all new logic in feature flags. This allows you to deploy code to production while it is still "dormant".

### 1. Define the Flag
```yaml
# feature-flags.yml
new_dashboard:
  enabled: false
  rollout_percentage: 0  # Start at 0%
```

### 2. Guard the Code
```typescript
if (flags.isEnabled('new-dashboard', user.id)) {
  return <NewDashboard />;
}
return <LegacyDashboard />;
```

### 3. Verify Deployment
Before you ship, run the safety check:
```bash
python scripts/safe-feature.py verify --path ./src --config ./feature-flags.yml
```

---

## 🔍 Step 3: Git Safety Audit

Before merging your PR, run the **Safety Auditor** to detect destructive changes that might break production.

```bash
# Audits your current branch against master
python scripts/safe-feature.py audit --base master
```

**The Auditor detects:**
- Modified function signatures without default values.
- New code blocks without feature flag guards.
- Potential "Big Bang" changes that increase risk.

---

## 📈 Step 4: Gradual Rollout (Canary)

Never switch a feature to 100% on Day 1. Use a gradual schedule:

| Phase | Traffic | Duration | Goal |
|-------|---------|----------|------|
| **Canary** | 5% | 1 hour | Check for smoke/crash loops |
| **Early Bird** | 25% | 1 day | Check for performance bugs |
| **Rollout** | 50% | 2 days | Monitor business metrics |
| **GA** | 100% | Permanent | Complete the rollout |

---

## 🎯 Vue Money Example: Adding "Credit Cards"

If you are adding Credit Card support to Vue Money while it only has Auto Loans:

1.  **Don't** rewrite the `LoanCard` component.
2.  **Do** create `CreditCardSpecificCard`.
3.  **Flag it**: `enable-credit-cards`.
4.  **Audit**: Run `safe-feature audit` to ensure `getLoans()` wasn't broken by the new data.

---

## 🛠️ Performance & Safety Checklist

- [ ] Is the change **additive**? (Yes/No)
- [ ] Is there a **Feature Flag**? (Yes/No)
- [ ] Did you run `safe-feature verify`? (Yes/No)
- [ ] Is the **Database Migration** backward-compatible? (Yes/No)
- [ ] Is there a **Kill Switch**? (Yes/No)

---

**Success = Zero Downtime + Instant Rollback.** 🚀
