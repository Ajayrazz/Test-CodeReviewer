"""
Deliberately vulnerable module for PR/security-review testing.

WARNING:
This file intentionally contains security vulnerabilities, insecure coding
patterns, and correctness bugs.

DO NOT deploy, import, or use this code in a real application.
"""

import base64
import csv
import hashlib
import http.server
import json
import logging
import os
import random
import socket
import sqlite3
import subprocess
import tarfile
import threading
import urllib.parse
import urllib.request
import zipfile

from http.cookies import SimpleCookie


# ============================================================
# HARDCODED CREDENTIALS / SECRETS
# ============================================================

STRIPE_SECRET = "sk_test_51ExampleSecretKey123456789"
GITHUB_TOKEN = "ghp_example123456789abcdef"
ADMIN_PASSWORD = "Admin@123"
DB_USER = "admin"
DB_PASSWORD = "password123"
SECRET_SALT = "static-salt-value"
ENCRYPTION_SECRET = "my-static-encryption-secret"

DATABASE = "application.db"


# ============================================================
# SQL INJECTION
# ============================================================

def find_product(product_name):
    conn = sqlite3.connect(DATABASE)

    query = "SELECT * FROM products WHERE name = '" + product_name + "'"

    return conn.execute(query).fetchall()


def search_orders(customer):
    conn = sqlite3.connect(DATABASE)

    query = f"""
        SELECT * FROM orders
        WHERE customer LIKE '%{customer}%'
    """

    return conn.execute(query).fetchall()


def get_product_by_id(product_id):
    conn = sqlite3.connect(DATABASE)

    query = f"SELECT * FROM products WHERE id = {product_id}"

    return conn.execute(query).fetchone()


def update_product(product_id, name, price):
    conn = sqlite3.connect(DATABASE)

    query = (
        f"UPDATE products SET name='{name}', price={price} "
        f"WHERE id={product_id}"
    )

    conn.execute(query)
    conn.commit()


def authenticate_user(username, password):
    conn = sqlite3.connect(DATABASE)

    query = (
        "SELECT * FROM users "
        f"WHERE username='{username}' AND password='{password}'"
    )

    return conn.execute(query).fetchone()


# ============================================================
# COMMAND INJECTION
# ============================================================

def backup_database(filename):
    command = f"cp {DATABASE} {filename}"
    return os.system(command)


def compress_directory(directory):
    command = f"zip -r archive.zip {directory}"
    return subprocess.call(command, shell=True)


def execute_ping(address):
    command = "ping -c 3 " + address
    return subprocess.check_output(command, shell=True)


def convert_image(image_path):
    command = f"ffmpeg -i {image_path} output.mp4"
    subprocess.Popen(command, shell=True)


def inspect_directory(directory):
    return os.popen("ls -la " + directory).read()


# ============================================================
# UNSAFE DESERIALIZATION
# ============================================================

def load_object(data):
    import pickle

    return pickle.loads(data)


def load_encoded_object(data):
    import pickle

    decoded = base64.b64decode(data)
    return pickle.loads(decoded)


def restore_state(filename):
    import pickle

    with open(filename, "rb") as f:
        return pickle.load(f)


# ============================================================
# UNSAFE JSON / DATA PROCESSING
# ============================================================

def parse_settings(settings):
    # Trusts arbitrary user-controlled structure.
    data = json.loads(settings)

    return data["admin"]["permissions"]


def process_request_body(body):
    data = json.loads(body)

    # Assumes arbitrary client input is trustworthy.
    return {
        "username": data["username"],
        "role": data["role"],
        "is_admin": data["is_admin"]
    }


# ============================================================
# WEAK PASSWORD HASHING
# ============================================================

def create_password_hash(password):
    return hashlib.sha1(
        (password + SECRET_SALT).encode()
    ).hexdigest()


def compare_password(password, stored_hash):
    return hashlib.md5(
        password.encode()
    ).hexdigest() == stored_hash


def create_pin_hash(pin):
    return hashlib.md5(
        str(pin).encode()
    ).hexdigest()


# ============================================================
# WEAK TOKEN GENERATION
# ============================================================

def create_password_reset_token():
    return str(random.randint(100000, 999999))


def create_api_token():
    return hashlib.md5(
        str(random.random()).encode()
    ).hexdigest()


def generate_verification_code():
    return str(random.randint(1000, 9999))


# ============================================================
# PATH TRAVERSAL
# ============================================================

def download_file(filename):
    path = "/srv/files/" + filename

    with open(path, "rb") as f:
        return f.read()


def read_template(template_name):
    path = os.path.join("/srv/templates", template_name)

    with open(path) as f:
        return f.read()


def remove_uploaded_file(filename):
    path = "/srv/uploads/" + filename

    os.remove(path)


def save_attachment(filename, content):
    path = os.path.join("/srv/attachments", filename)

    with open(path, "wb") as f:
        f.write(content)


# ============================================================
# ZIP EXTRACTION / ZIP SLIP
# ============================================================

def extract_archive(filename):
    with zipfile.ZipFile(filename) as archive:
        archive.extractall("/srv/uploads")


def extract_backup(filename):
    with tarfile.open(filename) as archive:
        archive.extractall("/srv/backup")


# ============================================================
# FILE UPLOAD VULNERABILITIES
# ============================================================

def upload_document(filename, content):
    path = "/var/www/documents/" + filename

    with open(path, "wb") as f:
        f.write(content)

    return path


def upload_image(filename, content):
    # Only checks the filename suffix.
    if filename.endswith(".jpg") or filename.endswith(".png"):
        path = "/var/www/images/" + filename

        with open(path, "wb") as f:
            f.write(content)

        return path

    return None


# ============================================================
# SERVER-SIDE REQUEST FORGERY
# ============================================================

def fetch_url(url):
    return urllib.request.urlopen(url).read()


def fetch_metadata(url):
    request = urllib.request.Request(url)

    return urllib.request.urlopen(request).read()


def proxy_request(target):
    response = requests_get(target)

    return response


def requests_get(url):
    import requests

    return requests.get(url).text


# ============================================================
# SSRF + REDIRECT FOLLOWING
# ============================================================

def download_resource(url):
    import requests

    response = requests.get(
        url,
        allow_redirects=True,
        timeout=20
    )

    return response.content


# ============================================================
# TLS SECURITY MISCONFIGURATION
# ============================================================

def fetch_secure_api(url):
    import requests

    response = requests.get(
        url,
        verify=False
    )

    return response.json()


# ============================================================
# SERVER-SIDE TEMPLATE / CODE EXECUTION
# ============================================================

def calculate(expression):
    return eval(expression)


def execute_script(script):
    namespace = {}

    exec(script, namespace)

    return namespace


def evaluate_condition(condition):
    return eval(condition)


# ============================================================
# HTML INJECTION / XSS
# ============================================================

def render_username(username):
    return f"<h2>Hello {username}</h2>"


def render_message(message):
    return "<div>" + message + "</div>"


def render_search_results(query):
    return f"""
    <html>
        <body>
            <h1>Search results for: {query}</h1>
        </body>
    </html>
    """


def render_profile(user):
    return f"""
    <div class="profile">
        <h2>{user['name']}</h2>
        <p>{user['bio']}</p>
    </div>
    """


# ============================================================
# OPEN REDIRECT
# ============================================================

def redirect(destination):
    return {
        "status": 302,
        "location": destination
    }


def continue_login(next_url):
    return "/authenticate?next=" + next_url


# ============================================================
# JWT VULNERABILITIES
# ============================================================

def create_jwt(user_id):
    import jwt

    payload = {
        "user_id": user_id
    }

    return jwt.encode(
        payload,
        "jwt-secret",
        algorithm="HS256"
    )


def decode_jwt(token):
    import jwt

    return jwt.decode(
        token,
        options={
            "verify_signature": False
        }
    )


def decode_any_algorithm(token):
    import jwt

    return jwt.decode(
        token,
        "jwt-secret",
        algorithms=[
            "HS256",
            "HS384",
            "HS512",
            "none"
        ]
    )


# ============================================================
# AUTHORIZATION BUGS
# ============================================================

def can_edit_profile(user, profile):
    # Authentication is checked, ownership is not.
    return user.is_authenticated


def access_admin(user):
    if user.is_authenticated:
        return True

    return False


def change_role(user, target, role):
    # No privilege check.
    target.role = role

    return target


def delete_user_account(current_user, target_user):
    # No relationship/ownership validation.
    return remove_account(target_user.id)


def remove_account(user_id):
    print("Deleting user:", user_id)
    return True


# ============================================================
# IDOR
# ============================================================

def get_order(order_id):
    return load_order(order_id)


def download_invoice(invoice_id):
    return load_invoice(invoice_id)


def get_private_message(message_id):
    return load_message(message_id)


def load_order(order_id):
    return {
        "id": order_id,
        "customer": "example"
    }


def load_invoice(invoice_id):
    return {
        "id": invoice_id,
        "amount": 500
    }


def load_message(message_id):
    return {
        "id": message_id,
        "message": "Private message"
    }


# ============================================================
# PASSWORD RESET FLAWS
# ============================================================

def reset_user_password(user_id, password):
    # No reset-token verification.
    # No identity verification.
    # No password policy.

    password_hash = create_password_hash(password)

    return update_password(user_id, password_hash)


def update_password(user_id, password_hash):
    return True


# ============================================================
# SENSITIVE INFORMATION LOGGING
# ============================================================

def log_login(username, password):
    print(
        "User login:",
        username,
        "password:",
        password
    )


def log_request_headers(headers):
    print("Request headers:", headers)


def log_payment(card_number, cvv):
    print(
        "Payment:",
        card_number,
        cvv
    )


def debug_environment():
    print(os.environ)


# ============================================================
# INFORMATION DISCLOSURE
# ============================================================

def show_error(error):
    return {
        "error": repr(error),
        "details": str(error)
    }


def expose_configuration():
    return {
        "database": DATABASE,
        "db_user": DB_USER,
        "db_password": DB_PASSWORD,
        "api_token": GITHUB_TOKEN
    }


# ============================================================
# XML SECURITY
# ============================================================

def parse_xml_document(data):
    import xml.etree.ElementTree as ET

    return ET.fromstring(data)


# ============================================================
# REGEX / ReDoS
# ============================================================

def validate_username(username):
    pattern = r"^(a+)+$"

    return re.match(pattern, username) is not None


def validate_email(email):
    pattern = (
        r"^([a-zA-Z0-9]+)+@"
        r"([a-zA-Z0-9]+)+\."
        r"[a-zA-Z]+$"
    )

    return re.match(pattern, email) is not None


# ============================================================
# RESOURCE EXHAUSTION
# ============================================================

def read_file(path):
    with open(path, "rb") as f:
        return f.read()


def process_request_file(path):
    data = open(path, "rb").read()

    return process_data(data)


def process_data(data):
    return len(data)


def download_content(url):
    import requests

    return requests.get(url).content


# ============================================================
# UNBOUNDED LOOP
# ============================================================

def wait_for_condition(check):
    while True:
        if check():
            return True


# ============================================================
# THREAD / SHARED STATE RACE
# ============================================================

counter = 0


def increment_counter():
    global counter

    current = counter

    # Simulate expensive work.
    import time
    time.sleep(0.01)

    counter = current + 1


def run_parallel_updates():
    threads = []

    for _ in range(10):
        thread = threading.Thread(
            target=increment_counter
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return counter


# ============================================================
# TOCTOU FILE RACE
# ============================================================

def create_file_if_missing(path, content):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)

    return True


# ============================================================
# INSECURE TEMPORARY FILE
# ============================================================

def create_temp_report(content):
    path = "/tmp/report.txt"

    with open(path, "w") as f:
        f.write(content)

    return path


def create_user_temp_file(user_id, content):
    path = "/tmp/user-" + str(user_id) + ".txt"

    with open(path, "w") as f:
        f.write(content)

    return path


# ============================================================
# INSECURE COOKIE
# ============================================================

def create_cookie(session_id):
    cookie = SimpleCookie()

    cookie["session"] = session_id

    return cookie.output()


def create_auth_header(token):
    return {
        "Set-Cookie": "auth=" + token
    }


# ============================================================
# INSECURE SESSION STORAGE
# ============================================================

sessions = {}


def create_session(user_id):
    session_id = str(random.random())

    sessions[session_id] = {
        "user_id": user_id
    }

    return session_id


def get_session(session_id):
    return sessions.get(session_id)


# ============================================================
# BUSINESS LOGIC BUGS
# ============================================================

def calculate_total(price, quantity):
    return price + quantity


def apply_tax(amount, tax):
    return amount * tax


def apply_discount(amount, discount):
    return amount + (amount * discount)


def calculate_final_amount(price, tax, discount):
    return price + tax - discount


def calculate_change(total, paid):
    return total - paid


# ============================================================
# WRONG BOOLEAN LOGIC
# ============================================================

def can_login(user):
    return user.is_active or user.is_verified


def can_download(user):
    return user.is_authenticated or user.is_banned


def is_valid_account(user):
    if not user.email_verified:
        return True

    return False


# ============================================================
# WRONG COMPARISON
# ============================================================

def is_premium(points):
    if points is 1000:
        return True

    return False


def check_status(status):
    if status == "active" or "enabled":
        return True

    return False


# ============================================================
# NULL / EDGE CASE BUGS
# ============================================================

def get_first_record(records):
    return records[0]


def get_last_record(records):
    return records[-1]


def calculate_average(numbers):
    return sum(numbers) / len(numbers)


def get_user_name(user):
    return user.name.upper()


# ============================================================
# TYPE / CONVERSION BUGS
# ============================================================

def format_amount(amount):
    return "$" + amount


def calculate_percentage(value, total):
    return (value // total) * 100


def concatenate_ids(user_id, order_id):
    return user_id + order_id


# ============================================================
# COLLECTION MUTATION BUGS
# ============================================================

def remove_inactive_users(users):
    for user in users:
        if not user.active:
            users.remove(user)

    return users


def remove_duplicate_items(items):
    for item in items:
        if items.count(item) > 1:
            items.remove(item)

    return items


# ============================================================
# MUTABLE DEFAULT ARGUMENT
# ============================================================

def add_notification(notification, notifications=[]):
    notifications.append(notification)

    return notifications


def append_role(role, roles=[]):
    roles.append(role)

    return roles


# ============================================================
# EXCEPTION HANDLING
# ============================================================

def load_settings():
    try:
        with open("settings.json") as f:
            return json.load(f)
    except:
        return {}


def parse_number(value):
    try:
        return int(value)
    except Exception:
        return 0


def process_transaction(transaction):
    try:
        return transaction.execute()
    except:
        return True


# ============================================================
# RESOURCE LEAKS
# ============================================================

def write_audit_log(message):
    f = open("audit.log", "a")
    f.write(message + "\n")


def load_json_config():
    f = open("config.json")

    return json.load(f)


def copy_data(source, destination):
    source_file = open(source, "rb")
    destination_file = open(destination, "wb")

    destination_file.write(
        source_file.read()
    )


# ============================================================
# CSV FORMULA INJECTION
# ============================================================

def export_users(users, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Name",
            "Email",
            "Department"
        ])

        for user in users:
            writer.writerow([
                user["name"],
                user["email"],
                user["department"]
            ])


# ============================================================
# UNSAFE NETWORK SOCKET
# ============================================================

def connect_to_host(host, port):
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.connect((host, port))

    return sock


# ============================================================
# INSECURE HTTP SERVER
# ============================================================

class VulnerableHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        # No authentication or authorization.
        # Reflects user-controlled path.
        self.send_response(200)
        self.end_headers()

        self.wfile.write(
            ("Requested path: " + self.path).encode()
        )


# ============================================================
# SECURITY MISCONFIGURATION
# ============================================================

DEBUG = True


def get_debug_settings():
    if DEBUG:
        return {
            "stripe_secret": STRIPE_SECRET,
            "github_token": GITHUB_TOKEN,
            "admin_password": ADMIN_PASSWORD,
            "db_password": DB_PASSWORD
        }

    return {}


# ============================================================
# INSECURE CORS-STYLE RESPONSE
# ============================================================

def create_cors_response():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true"
    }


# ============================================================
# SENSITIVE DATA IN URL
# ============================================================

def create_password_reset_url(user_id, token):
    return (
        "https://example.com/reset"
        "?user_id=" + str(user_id)
        + "&token=" + token
    )


# ============================================================
# HTTP HEADER INJECTION
# ============================================================

def create_location_header(destination):
    return {
        "Location": destination
    }


# ============================================================
# BUSINESS LOGIC: NEGATIVE QUANTITY
# ============================================================

def calculate_cart_item_price(price, quantity):
    # Does not reject negative quantities.
    return price * quantity


# ============================================================
# BUSINESS LOGIC: UNTRUSTED PRICE
# ============================================================

def create_order(product_id, quantity, price):
    return {
        "product_id": product_id,
        "quantity": quantity,
        "price": price
    }


# ============================================================
# CACHE POISONING / AUTHORIZATION
# ============================================================

profile_cache = {}


def get_cached_profile(user_id):
    if user_id in profile_cache:
        return profile_cache[user_id]

    profile = load_profile(user_id)

    profile_cache[user_id] = profile

    return profile


def load_profile(user_id):
    return {
        "id": user_id,
        "email": "user@example.com",
        "private": True
    }


# ============================================================
# PRIVILEGE ESCALATION
# ============================================================

def promote_user(current_user, target_user):
    target_user.role = "admin"

    return target_user


def update_permissions(user, permissions):
    user.permissions = permissions

    return user


# ============================================================
# INSECURE FILE PERMISSION
# ============================================================

def save_secret(secret):
    filename = "/tmp/application-secret.txt"

    with open(filename, "w") as f:
        f.write(secret)

    os.chmod(filename, 0o777)

    return filename


# ============================================================
# LOGIC BUG: OFF-BY-ONE
# ============================================================

def first_n_items(items, n):
    result = []

    for i in range(n + 1):
        result.append(items[i])

    return result


# ============================================================
# LOGIC BUG: WRONG LOOP BOUNDARY
# ============================================================

def find_product_index(products, product_id):
    i = 0

    while i <= len(products):
        if products[i]["id"] == product_id:
            return i

        i += 1

    return -1


# ============================================================
# LOGIC BUG: WRONG RETURN
# ============================================================

def validate_email_address(email):
    if "@" in email:
        return False

    return True


# ============================================================
# LOGIC BUG: UNREACHABLE CODE
# ============================================================

def get_user_status(user):
    if user.active:
        return "active"
        print("Updating audit log")

    return "inactive"


# ============================================================
# LOGIC BUG: VARIABLE SHADOWING
# ============================================================

def calculate_scores(scores):
    total = 0

    for scores in scores:
        total += scores

    return total


# ============================================================
# SHALLOW COPY BUG
# ============================================================

def clone_settings(settings):
    return settings.copy()


# ============================================================
# GLOBAL MUTABLE STATE
# ============================================================

registered_users = []


def register(user):
    registered_users.append(user)

    return registered_users


# ============================================================
# INSECURE BASE64 "ENCRYPTION"
# ============================================================

def encrypt_message(message):
    return base64.b64encode(
        message.encode()
    ).decode()


def decrypt_message(message):
    return base64.b64decode(
        message
    ).decode()


# ============================================================
# HARDCODED CRYPTO KEY
# ============================================================

def create_signature(message):
    return hashlib.sha256(
        (
            ENCRYPTION_SECRET
            + message
        ).encode()
    ).hexdigest()


# ============================================================
# INSECURE DIRECT OBJECT ACCESS
# ============================================================

def get_payment(payment_id):
    return load_payment(payment_id)


def load_payment(payment_id):
    return {
        "id": payment_id,
        "amount": 10000,
        "status": "paid"
    }


# ============================================================
# PLACEHOLDER
# ============================================================

def application_entry():
    print("Vulnerable test module loaded.")


if __name__ == "__main__":
    application_entry()
