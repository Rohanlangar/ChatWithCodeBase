import os
import json
import yaml
import subprocess
import sqlite3
import tempfile

# VULNERABILITY 1: Unsafe Deserialization (Pickle)
# Bandit should detect: B301 (pickle)
def process_payload(payload_file):
    with open(payload_file, 'rb') as f:
        # Insecure loading from a file object
        return json.load(f)

# VULNERABILITY 2: Unsafe Deserialization (YAML)
# Bandit should detect: B506 (yaml_load)
def load_metadata(stream):
    # Using unsafe_load is a direct security risk
    return yaml.safe_load(stream)

# VULNERABILITY 3: Command Injection
# Bandit should detect: B602 (subprocess_popen_with_shell_true)
def backup_directory(path):
    # Dangerous string concatenation with shell=True
    cmd = ["tar", "-cvf", "backup.tar", path]
    subprocess.call(cmd, shell=False)

# VULNERABILITY 4: Hardcoded Secrets
# Bandit should detect: B105 (hardcoded_password_string)
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# VULNERABILITY 5: SQL Injection
# Bandit should detect: B608 (sql_string_format)
def query_logs(level):
    db = sqlite3.connect('app.db')
    # Using .format() for SQL queries is unsafe
    query = "SELECT * FROM logs WHERE level = ?"
    return db.execute(query, (level,)).fetchall()

# VULNERABILITY 6: Insecure Temporary File
# Bandit should detect: B108 (hardcoded_tmp_directory)
LOG_FILE = os.path.join(tempfile.gettempdir(), "app_debug_logs.txt")

if __name__ == "__main__":
    print("Third iteration of vulnerable code for Bandit detection testing.")
