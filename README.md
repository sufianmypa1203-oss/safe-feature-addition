# 🌌 Safe Feature Addition Toolkit
> **Ship Without Breaking: The Ultimate Production Guide**

This toolkit provides a comprehensive set of patterns, scripts, and examples for adding new features to existing production software with zero downtime and minimal risk.

## 🏗 What's Inside?

- **[SKILL.md](./SKILL.md)**: The core AI-agentic skill for safe development.
- **[scripts/](./scripts/)**: Automation tools for verifying flag usage and managing rollouts.
  - `verify-flags.js`: Scans for undeclared feature flags.
  - `canary-rollout.sh`: Template for gradual deployment management.
- **[examples/](./examples/)**: Ready-to-use patterns for major refactors.
  - `strangler-fig/`: Moving from monolith to service.
  - `branch-by-abstraction/`: Component replacement strategy.
  - `feature-flags/`: Basic vs. Advanced flag implementations.

## 🚀 Quick Start

1.  **Plan**: Use the `safe-feature-addition` skill to design your rollout strategy.
2.  **Toggle**: Integrate feature flags using the examples in `examples/feature-flags`.
3.  **Verify**: Run the verification script before shipping:
    ```bash
    node scripts/verify-flags.js --path ./src --config ./feature-flags.yml
    ```
4.  **Deploy**: Use `scripts/canary-rollout.sh` as a template for your CI/CD pipeline.

## 🛡 Security & Safety
Always ensure your feature flags have a "kill switch" and automatic rollback triggers based on error rate metrics.

---
*Created with The Premiere Skill Factory* 🏭
