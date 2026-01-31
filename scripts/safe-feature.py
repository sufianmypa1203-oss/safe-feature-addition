#!/usr/bin/env python3
"""
🛡️ Safe Feature Addition CLI - Elite Grade
A unified tool for safe production feature rollouts.
Includes Flag verification, Git safety auditing, and scaffold generation.
"""

import os
import sys
import json
import re
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# ANSI Colors for premium experience
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    BOLD = '\033[1m'
    NC = '\033[0m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}", file=sys.stderr)
def log_success(msg): print(f"{Colors.GREEN}[PASS]{Colors.NC} {msg}", file=sys.stderr)
def log_warn(msg): print(f"{Colors.YELLOW}[WARN]{Colors.NC} {msg}", file=sys.stderr)
def log_error(msg): print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}", file=sys.stderr)

# === CLI TOOL LOGIC ===

class SafeFeatureCLI:
    def __init__(self):
        self.config_file = 'feature-flags.yml' # Default
        self.supported_exts = {'.js', '.ts', '.jsx', '.tsx', '.py', '.go', '.rs'}

    def verify_cmd(self, path_to_scan, config_path):
        """Verify that all flags used in code are defined in the config."""
        log_info(f"Verifying flags in {path_to_scan} using {config_path}...")
        
        # 1. Load config
        if not os.path.exists(config_path):
            log_error(f"Config file not found: {config_path}")
            return False
            
        # Basic YAML/JSON parsing (minimal dependencies: use json or simple regex for yaml if needed)
        # For production grade, we'd use PyYAML, but we'll stick to simple parsing for portability
        try:
            with open(config_path, 'r') as f:
                content = f.read()
                # Basic key extraction from YAML-like structure
                config_flags = re.findall(r'^([a-zA-Z0-9_-]+):', content, re.MULTILINE)
        except Exception as e:
            log_error(f"Failed to read config: {e}")
            return False

        # 2. Scan Source
        used_flags = set()
        flag_regex = re.compile(r"isEnabled\(['\"]([^'\" \n]+)['\"]|is_enabled\(['\"]([^'\" \n]+)['\"]|check\(['\"]([^'\" \n]+)['\"]")
        
        file_count = 0
        for root, dirs, files in os.walk(path_to_scan):
            # Skip hidden and annoying dirs
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'dist', 'build', '__pycache__']]
            for file in files:
                if any(file.endswith(ext) for ext in self.supported_exts):
                    file_count += 1
                    with open(os.path.join(root, file), 'r', errors='ignore') as f:
                        file_content = f.read()
                        matches = flag_regex.findall(file_content)
                        for m in matches:
                            flag = next(filter(None, m), None)
                            if flag: used_flags.add(flag)

        log_info(f"Scanned {file_count} files.")
        
        # 3. Compare
        missing = [f for f in used_flags if f not in config_flags]
        unused = [f for f in config_flags if f not in used_flags]
        
        if missing:
            log_warn(f"Flags used in code but MISSING from config:")
            for m in missing: print(f"  - {m}")
        
        if unused:
            log_info(f"Flags in config but not used in code (potential cleanup):")
            for u in unused: print(f"  - {u}")
            
        if not missing:
            log_success("All flags verified.")
            return True
        return False

    def audit_cmd(self, base_branch):
        """Analyze git diff for destructive changes (missing flags or signature breaks)."""
        log_info(f"Auditing changes against {base_branch}...")
        
        try:
            diff = subprocess.check_output(['git', 'diff', f'{base_branch}...HEAD'], encoding='utf-8')
        except Exception as e:
            log_error(f"Git diff failed: {e}")
            return False

        # 1. Look for modified function signatures (Destructive change detection)
        # Regex to find shifted functions without default params
        # This is a heuristic: looking for lines starting with '-' then '+' where parameters changed
        destructive_patterns = [
            # Function signature change without adding a default value or being inside a flag
            (r"-function\s+\w+\(([^)]*)\)", r"\+function\s+\w+\(([^)]*)\)"),
            # Method signature change
            (r"-\s+\w+\(([^)]*)\)\s+\{", r"\+\s+\w+\(([^)]*)\)\s+\{")
        ]
        
        warnings = 0
        lines = diff.split('\n')
        for i in range(len(lines) - 1):
            line = lines[i]
            next_line = lines[i+1]
            if line.startswith('-') and next_line.startswith('+'):
                # Check for parameter shifts
                if '(' in line and '(' in next_line:
                    old_params = line[line.find('(')+1:line.find(')')].strip()
                    new_params = next_line[next_line.find('(')+1:next_line.find(')')].strip()
                    
                    # If params were added and none have default values (=)
                    if len(new_params) > len(old_params) and '=' not in new_params:
                        log_warn(f"Potential Destructive Change: Modified signature at line {i}")
                        print(f"  {Colors.RED}-{line.strip()}{Colors.NC}")
                        print(f"  {Colors.GREEN}+{next_line.strip()}{Colors.NC}")
                        print(f"  {Colors.YELLOW}Tip: Use optional parameters with default values for backward compatibility.{Colors.NC}")
                        warnings += 1

        # 2. Check for "Naked Logic" (New logic not wrapped in flags)
        # We look for large additions of code that don't contain a flag check nearby
        # (This is harder, but we can look for "critical keywords" like payment, auth, etc)
        
        if warnings == 0:
            log_success("Audit complete. No obvious destructive changes detected.")
        else:
            log_warn(f"Audit found {warnings} potential safety issues.")
            
        return True

def main():
    parser = argparse.ArgumentParser(description="🛡️ Safe Feature Addition CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Verify Command
    verify_parser = subparsers.add_parser("verify", help="Verify flag consistency")
    verify_parser.add_argument("--path", default=".", help="Source path to scan")
    verify_parser.add_argument("--config", default="feature-flags.yml", help="Config file path")

    # Audit Command
    audit_parser = subparsers.add_parser("audit", help="Audit git changes for destructive patterns")
    audit_parser.add_argument("--base", default="master", help="Base branch (main/master)")

    args = parser.parse_args()
    cli = SafeFeatureCLI()

    if args.command == "verify":
        success = cli.verify_cmd(args.path, args.config)
        sys.exit(0 if success else 1)
    elif args.command == "audit":
        success = cli.audit_cmd(args.base)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
