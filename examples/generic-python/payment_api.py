"""
🐍 Generic Python Backend - Safe Feature Addition Example
Requirement: Add a new "Crypto" payment processor to a REST API.
"""

import os

# 1. Universal Feature Flag Logic
class FeatureFlags:
    @staticmethod
    def is_enabled(flag_name, context=None):
        # In production, check Redis, LaunchDarkly, or Env Vars
        env_flag = os.getenv(f"FLAG_{flag_name.upper()}", "false")
        return env_flag.lower() == "true"

# 2. Existing Logic (Untouched)
def process_standard_payment(amount, user_id):
    print(f"💰 Processing ${amount} via Credit Card for User {user_id}")
    return {"status": "success", "provider": "stripe"}

# 3. New Logic (Isolated)
def process_crypto_payment(amount, user_id):
    print(f"🪙 Processing ${amount} via Bitcoin/Ethereum for User {user_id}")
    return {"status": "success", "provider": "coinbase-commerce"}

# 4. The Unified Gateway (Safe & Additive)
def payment_handler(amount, user_id, method="credit_card"):
    """
    Main entry point for payments.
    Safe: Checks flags before routing to new features.
    """
    
    # 🛡️ FEATURE FLAG GUARD
    if method == "crypto":
        if FeatureFlags.is_enabled("enable_crypto_payments"):
            return process_crypto_payment(amount, user_id)
        else:
            return {"status": "error", "message": "Crypto payments are currently in maintenance."}
            
    # 🚀 DEFAULT PATH (Always working)
    return process_standard_payment(amount, user_id)

# Test the safe rollout
if __name__ == "__main__":
    print("--- 1. Standard Payment ---")
    print(payment_handler(100, "user_123"))

    print("\n--- 2. Crypto Payment (Flag OFF) ---")
    print(payment_handler(50, "user_123", method="crypto"))

    print("\n--- 3. Crypto Payment (Flag ON) ---")
    os.environ["FLAG_ENABLE_CRYPTO_PAYMENTS"] = "true"
    print(payment_handler(75, "user_123", method="crypto"))
