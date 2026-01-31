# examples/feature-flags/implementation.py

import hashlib

class FeatureFlags:
    def __init__(self, config):
        self.config = config

    def is_enabled(self, flag_name, user_id=None):
        flag_config = self.config.get(flag_name)
        if not flag_config:
            return False
            
        # 1. Global Kill Switch
        if not flag_config.get('enabled', False):
            return False
            
        # 2. Specific User Override
        if user_id and user_id in flag_config.get('enabled_users', []):
            return True
            
        # 3. Gradual Rollout (Deterministic Hash)
        if user_id and 'rollout_percentage' in flag_config:
            user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
            bucket = user_hash % 100
            return bucket < flag_config['rollout_percentage']
            
        return flag_config.get('enabled', False)

# Example Config
config = {
    'new_hero_section': {
        'enabled': True,
        'rollout_percentage': 10,  # 10% of users
        'enabled_users': ['admin_user_7']
    }
}

# Usage
flags = FeatureFlags(config)
print(f"User 1: {flags.is_enabled('new_hero_section', 'user_1')}")
print(f"Admin: {flags.is_enabled('new_hero_section', 'admin_user_7')}")
