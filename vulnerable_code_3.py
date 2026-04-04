import os
import pickle
import yaml
import subprocess
import sqlite3

# VULNERABILITY 1: Unsafe Deserialization (Pickle)
# Bandit should detect: B301 (pickle)
def process_payload(payload_file):
    with open(payload_file, 'rb') as f:
        # Insecure loading from a file object
        return pickle.load(f)

# VULNERABILITY 2: Unsafe Deserialization (YAML)
# Bandit should detect: B506 (yaml_load)
def load_metadata(stream):
    # Using unsafe_load is a direct security risk
    return yaml.unsafe_load(stream)

# VULNERABILITY 3: Command Injection
# Bandit should detect: B602 (subprocess_popen_with_shell_true)
def backup_directory(path):
    # Dangerous string concatenation with shell=True
    cmd = "tar -cvf backup.tar " + path
    subprocess.call(cmd, shell=True)

# VULNERABILITY 4: Hardcoded Secrets
# Bandit should detect: B105 (hardcoded_password_string)
AWS_SECRET_KEY = "AKIAIMORIJ727GEXAMPLE"
DATABASE_URL = "postgres://admin:password123@localhost:5432/mydb"

# VULNERABILITY 5: SQL Injection
# Bandit should detect: B608 (sql_string_format)
def query_logs(level):
    db = sqlite3.connect('app.db')
    # Using .format() for SQL queries is unsafe
    query = "SELECT * FROM logs WHERE level = '{}'".format(level)
    return db.execute(query).fetchall()

# VULNERABILITY 6: Insecure Temporary File
# Bandit should detect: B108 (hardcoded_tmp_directory)
LOG_FILE = "/var/tmp/app_debug_logs.txt"

if __name__ == "__main__":
    print("Third iteration of vulnerable code for Bandit detection testing.")
