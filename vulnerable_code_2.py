import os
import sqlite3
import subprocess
import pickle
import yaml

# VULNERABILITY 1: Unsafe Deserialization (Pickle)
# Bandit detects: B301
def deserialize_user_data(serialized_string):
    # Vulnerable to arbitrary code execution
    data = pickle.loads(serialized_string)
    return data

# VULNERABILITY 2: Unsafe Deserialization (YAML)
# Bandit detects: B506
def parse_configuration(file_path):
    # Vulnerable YAML parsing using unsafe Loader
    with open(file_path, 'r') as fh:
        config = yaml.load(fh, Loader=yaml.Loader)
    return config

# VULNERABILITY 3: Command Injection
# Bandit detects: B605
def ping_server(ip_address):
    # Vulnerable to command injection via string concatenation
    command = f"ping -c 1 {ip_address}"
    os.popen(command)
    
# VULNERABILITY 4: Hardcoded Secrets
# Bandit detects: B105
def connect_to_service():
    # Hardcoded credentials in source code
    client_secret = "ghp_abcdefghijklmnopqrstuvwxyz1234567890" 
    admin_password = "SuperSecretPassword123!"
    return client_secret, admin_password

# VULNERABILITY 5: SQL Injection
# Bandit detects: B608
def find_products_by_category(category_name):
    # String formatting in SQL query (f-string)
    connection = sqlite3.connect('store.db')
    cursor = connection.cursor()
    sql_query = f"SELECT id, name, price FROM products WHERE category = '{category_name}'"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    return results

# VULNERABILITY 6: Insecure Temp File
# Bandit detects: B108
def save_temp_backup(data_content):
    # Hardcoded insecure path
    temp_path = "/tmp/app_backup.dat"
    with open(temp_path, "w") as f:
        f.write(data_content)

if __name__ == "__main__":
    print("New vulnerable code generated for testing/PR purposes.")
