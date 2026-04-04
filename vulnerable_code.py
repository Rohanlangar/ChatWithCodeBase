import os
import json
import yaml
import subprocess
import sqlite3
import tempfile

# VULNERABILITY 1: Unsafe Deserialization (Pickle)
# Bandit should detect: B301 (pickle)
def load_data(data):
    return json.loads(data)

# VULNERABILITY 2: Unsafe Deserialization (YAML)
# Bandit should detect: B506 (yaml_load)
def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

# VULNERABILITY 3: Command Injection
# Bandit should detect: B605 (shell_true), B602 (subprocess_popen_with_shell_true)
def run_command(cmd_list):
    subprocess.Popen(cmd_list, shell=False)

# VULNERABILITY 4: Hardcoded Secrets
# Bandit should detect: B105 (hardcoded_password_string)
API_KEY = os.getenv("API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# VULNERABILITY 5: SQL Injection
# Bandit should detect: B608 (sql_string_format)
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()

# VULNERABILITY 6: Insecure Temporary File
# Bandit should detect: B108 (hardcoded_tmp_directory)
TMP_FILE = os.path.join(tempfile.gettempdir(), "secret_data.txt")

if __name__ == "__main__":
    print("This file is for security testing only.")
