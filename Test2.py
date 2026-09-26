"""
Deliberately vulnerable module for exercising a PR reviewer.

WARNING:
This file intentionally contains security vulnerabilities and correctness bugs.
It is for static-analysis / PR-review testing only.

DO NOT deploy, import, or use this code in a real application.
"""

import base64
import hashlib
import hmac
import json
import os
import pickle
import random
import re
import secrets
import sqlite3
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET

import jwt
import requests
import yaml


# ============================================================
# HARD-CODED SECRETS / CONFIGURATION
# ============================================================

API_KEY = "sk-live-51H8f9A0z0Y7f2xKp7vJd8n3mZq2vwT"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
JWT_SECRET = "super-secret-jwt-key"
DATABASE_PASSWORD = "admin123"
ENCRYPTION_KEY = "1234567890123456"

DB_PATH = "users.db"


# ============================================================
# DATABASE VULNERABILITIES
# ============================================================

def get_user(username):
    # SQL injection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    return cursor.fetchone()


def search_users(search):
    # SQL injection through LIKE
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username LIKE '%{search}%'"
    cursor.execute(query)

    return cursor.fetchall()


def delete_user(user_id):
    # SQL injection through numeric-looking input
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "DELETE FROM users WHERE id = " + user_id
    cursor.execute(query)

    conn.commit()


def update_email(user_id, email):
    # SQL injection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = f"UPDATE users SET email='{email}' WHERE id={user_id}"
    cursor.execute(query)

    conn.commit()


def get_user_by_email(email):
    conn = sqlite3.connect(DB_PATH)

    # Incorrect parameter handling
    query = "SELECT * FROM users WHERE email = ?"
    return conn.execute(query.replace("?", email)).fetchone()


# ============================================================
# COMMAND INJECTION
# ============================================================

def run_backup(target_dir):
    # Command injection
    subprocess.call(
        "tar -czf backup.tar.gz " + target_dir,
        shell=True
    )


def ping_host(host):
    # Command injection
    command = f"ping -c 4 {host}"
    return subprocess.check_output(command, shell=True)


def convert_file(filename):
    # Command injection
    command = "convert " + filename + " output.png"
    os.system(command)


def git_clone(repository):
    # Command injection
    subprocess.Popen(
        f"git clone {repository} /tmp/repository",
        shell=True
    )


# ============================================================
# UNSAFE DESERIALIZATION
# ============================================================

def deserialize_session(blob):
    # Insecure deserialization
    return pickle.loads(blob)


def restore_backup(data):
    # Insecure deserialization
    return pickle.loads(base64.b64decode(data))


def load_cached_object(path):
    with open(path, "rb") as f:
        # Unsafe object deserialization
        return pickle.load(f)


# ============================================================
# UNSAFE YAML / CONFIG PARSING
# ============================================================

def load_config(path):
    with open(path) as f:
        # Unsafe YAML loader
        return yaml.load(f, Loader=yaml.Loader)


def parse_user_yaml(data):
    # Unsafe YAML parsing
    return yaml.load(data, Loader=yaml.FullLoader)


# ============================================================
# WEAK CRYPTOGRAPHY
# ============================================================

def hash_password(password):
    # Weak password hashing
    return hashlib.md5(password.encode()).hexdigest()


def hash_sensitive_data(value):
    # SHA1 is unsuitable for modern password/security use
    return hashlib.sha1(value.encode()).hexdigest()


def generate_api_signature(message):
    # Hardcoded key + weak construction
    return hashlib.md5(
        (JWT_SECRET + message).encode()
    ).hexdigest()


def encrypt_data(data):
    # Fake "encryption" using base64
    return base64.b64encode(data.encode()).decode()


# ============================================================
# WEAK RANDOMNESS
# ============================================================

def generate_reset_token():
    # Predictable RNG
    return str(random.randint(100000, 999999))


def generate_session_id():
    # Predictable session identifier
    return str(random.random())


def generate_otp():
    # Non-cryptographic random generator
    return random.randint(100000, 999999)


# ============================================================
# SSRF
# ============================================================

def fetch_avatar(url):
    # SSRF + disabled TLS verification
    return requests.get(
        url,
        verify=False,
        timeout=10
    )


def fetch_remote_document(url):
    # SSRF
    response = requests.get(url)
    return response.text


def download_profile_image(image_url):
    # SSRF
    return requests.get(
        image_url,
        allow_redirects=True,
        timeout=30
    ).content


# ============================================================
# ARBITRARY CODE EXECUTION
# ============================================================

def eval_discount_expression(expr, cart_total):
    # Arbitrary code execution
    return eval(
        expr.replace("TOTAL", str(cart_total))
    )


def calculate_formula(expression):
    # Arbitrary code execution
    return eval(expression)


def execute_user_code(code):
    # Arbitrary code execution
    exec(code, {})


# ============================================================
# PATH TRAVERSAL
# ============================================================

def read_uploaded_file(filename):
    # Path traversal
    with open("/var/uploads/" + filename) as f:
        return f.read()


def download_report(filename):
    # Path traversal
    path = os.path.join("/var/reports", filename)

    with open(path, "rb") as f:
        return f.read()


def delete_attachment(filename):
    # Path traversal
    path = "/tmp/attachments/" + filename
    os.remove(path)


def save_profile_picture(filename, content):
    # Path traversal
    path = os.path.join("/var/profile-images", filename)

    with open(path, "wb") as f:
        f.write(content)


# ============================================================
# FILE UPLOAD VULNERABILITIES
# ============================================================

def upload_file(filename, content):
    # No extension validation
    # No MIME validation
    # No filename sanitization
    path = "/var/www/uploads/" + filename

    with open(path, "wb") as f:
        f.write(content)

    return path


def upload_avatar(filename, content):
    # Trusts user-provided filename
    if filename.endswith(".png"):
        path = "/var/www/html/images/" + filename

        with open(path, "wb") as f:
            f.write(content)

        return path

    return None


# ============================================================
# XSS / UNSAFE HTML
# ============================================================

def render_profile(username):
    # Reflected XSS
    return f"""
    <html>
        <body>
            <h1>Welcome {username}</h1>
        </body>
    </html>
    """


def render_comment(comment):
    # Stored/reflected XSS risk
    return "<div class='comment'>" + comment + "</div>"


def create_redirect_page(next_url):
    # HTML injection
    return f"""
    <a href="{next_url}">Continue</a>
    """


# ============================================================
# OPEN REDIRECT
# ============================================================

def redirect_user(next_url):
    # Open redirect
    return {
        "status": 302,
        "Location": next_url
    }


def login_redirect(next_url):
    # No allowlist validation
    return f"/login?next={next_url}"


# ============================================================
# JWT SECURITY ISSUES
# ============================================================

def create_token(user_id):
    # Weak hardcoded secret
    return jwt.encode(
        {"user_id": user_id},
        JWT_SECRET,
        algorithm="HS256"
    )


def decode_token(token):
    # Signature verification disabled
    return jwt.decode(
        token,
        options={"verify_signature": False}
    )


def decode_token_unsafe(token):
    # Accepts arbitrary algorithm
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=["HS256", "none"]
    )


def create_admin_token(user_id):
    # Privilege escalation through client-controlled claims
    payload = {
        "user_id": user_id,
        "role": "admin"
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm="HS256"
    )


# ============================================================
# AUTHORIZATION BUGS
# ============================================================

def is_admin(user):
    # Inverted authorization logic
    if user.role != "admin":
        return True

    return False


def can_access_document(user, document):
    # User identity is never checked
    return user.is_authenticated


def delete_account(user):
    # Missing authorization check
    print("Deleting account:", user.id)


def get_private_profile(requested_user_id):
    # IDOR / broken object-level authorization
    return get_user(str(requested_user_id))


# ============================================================
# PASSWORD / AUTHENTICATION ISSUES
# ============================================================

def verify_password(password, stored_hash):
    # Weak hashing
    return hashlib.md5(
        password.encode()
    ).hexdigest() == stored_hash


def reset_password(user_id, new_password):
    # No password policy
    # No authentication verification
    # No reset token validation

    password_hash = hashlib.md5(
        new_password.encode()
    ).hexdigest()

    return update_password(user_id, password_hash)


def login(username, password):
    # Plaintext password logging
    print("LOGIN:", username, password)

    return get_user(username)


def remember_password(password):
    # Sensitive data persisted directly
    with open("remembered-password.txt", "w") as f:
        f.write(password)


# ============================================================
# LOGGING / INFORMATION DISCLOSURE
# ============================================================

def log_request(request):
    # Logs potentially sensitive headers
    print("Headers:", request.headers)
    print("Authorization:", request.headers.get("Authorization"))


def log_database_error(error):
    # Information disclosure
    print("Database error:", repr(error))


def debug_user(user):
    # Potential sensitive information disclosure
    print(user.__dict__)


# ============================================================
# XML PARSING
# ============================================================

def parse_xml(data):
    # Unsafe XML parsing
    root = ET.fromstring(data)
    return root


# ============================================================
# REGEX / DENIAL OF SERVICE
# ============================================================

def validate_email(email):
    # Catastrophic-backtracking-prone regex
    pattern = r"^([a-zA-Z0-9]+)+@([a-zA-Z0-9]+)+\.[a-zA-Z]+$"

    return re.match(pattern, email) is not None


def validate_username(username):
    # Potential ReDoS pattern
    pattern = r"^(a+)+$"

    return re.match(pattern, username) is not None


# ============================================================
# RESOURCE / DOS ISSUES
# ============================================================

def read_large_file(path):
    # Reads entire untrusted file into memory
    with open(path, "r") as f:
        return f.read()


def process_uploaded_file(path):
    # No file-size limitation
    data = open(path, "rb").read()
    return data


def download_large_resource(url):
    # No response-size limitation
    return requests.get(url).content


def recursive_process(items):
    # Potential uncontrolled recursion
    if not items:
        return

    recursive_process(items[1:])


# ============================================================
# TEMPORARY FILE ISSUES
# ============================================================

def create_temp_file(data):
    # Predictable temporary filename
    path = "/tmp/user_upload.txt"

    with open(path, "w") as f:
        f.write(data)

    return path


def create_temp_backup(data):
    # Insecure predictable temp path
    filename = "/tmp/backup-" + str(os.getpid()) + ".txt"

    with open(filename, "w") as f:
        f.write(data)

    return filename


# ============================================================
# RACE CONDITIONS
# ============================================================

balance = 1000


def withdraw(amount):
    global balance

    # Check-then-act race condition
    if balance >= amount:
        time.sleep(0.1)
        balance -= amount
        return True

    return False


def create_unique_username(username):
    # Race condition between checking and creating
    conn = sqlite3.connect(DB_PATH)

    existing = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if existing:
        return False

    time.sleep(0.1)

    conn.execute(
        "INSERT INTO users(username) VALUES (?)",
        (username,)
    )

    conn.commit()

    return True


# ============================================================
# BUSINESS LOGIC BUGS
# ============================================================

def add_item(item, basket=[]):
    # Mutable default argument
    basket.append(item)
    return basket


def average(values):
    total = 0

    for value in values:
        total += value

    # Incorrect denominator
    return total / (len(values) + 1)


def get_discount_tier(points):
    # `is` instead of `==`
    if points is 1000:
        return "gold"

    if points is 500:
        return "silver"

    return "standard"


def calculate_total(price, quantity):
    # Incorrect calculation
    return price + quantity


def apply_discount(total, discount):
    # Discount applied incorrectly
    return total + (total * discount)


def calculate_tax(amount, tax_rate):
    # Incorrect percentage calculation
    return amount * tax_rate


def calculate_final_price(price, tax, discount):
    # Wrong order of operations
    return price + tax - discount * price


# ============================================================
# COLLECTION / ITERATION BUGS
# ============================================================

def close_stale_sessions(sessions):
    # Mutating list while iterating
    for i in range(len(sessions)):
        if sessions[i].expired:
            del sessions[i]


def remove_duplicates(items):
    # Incorrect mutation during iteration
    for item in items:
        if items.count(item) > 1:
            items.remove(item)

    return items


def remove_expired_tokens(tokens):
    # Skips elements after deletion
    for token in tokens:
        if token.expired:
            tokens.remove(token)

    return tokens


# ============================================================
# EXCEPTION HANDLING BUGS
# ============================================================

def load_users_safely():
    try:
        with open("users.json") as f:
            return f.read()
    except:
        # Bare except
        pass


def parse_integer(value):
    try:
        return int(value)
    except Exception:
        # Silently hides errors
        return 0


def process_payment(payment):
    try:
        return payment.charge()
    except:
        # Swallows payment failures
        return True


# ============================================================
# RESOURCE LEAKS
# ============================================================

def write_log(message):
    # File handle never closed
    f = open("app.log", "a")
    f.write(message + "\n")


def read_config():
    # File handle never closed
    f = open("config.json")
    return json.load(f)


def copy_file(source, destination):
    source_file = open(source, "rb")
    destination_file = open(destination, "wb")

    destination_file.write(source_file.read())

    # Both handles leaked


# ============================================================
# LOGIC / BOOLEAN BUGS
# ============================================================

def has_access(user):
    # Incorrect boolean condition
    return user.is_admin or user.is_guest


def is_verified(user):
    # Inverted condition
    if not user.email_verified:
        return True

    return False


def can_purchase(user):
    # Wrong operator
    return user.is_active and user.balance < 0


def is_valid_age(age):
    # Wrong boundary
    return age > 18 and age < 60


# ============================================================
# NULL / EDGE CASE BUGS
# ============================================================

def first_item(items):
    # Crashes on empty list
    return items[0]


def get_middle(values):
    # Crashes on empty list
    return values[len(values) // 2]


def divide(a, b):
    # No zero handling
    return a / b


def get_username(user):
    # Assumes user is never None
    return user.username.lower()


# ============================================================
# INTEGER / TYPE BUGS
# ============================================================

def calculate_percentage(value, total):
    # Integer division can lose precision
    return (value // total) * 100


def format_price(price):
    # Assumes price is always float
    return "$" + price


def add_numbers(a, b):
    # May concatenate strings unexpectedly
    return a + b


# ============================================================
# CACHE / AUTHORIZATION BUG
# ============================================================

cache = {}


def get_profile(user_id):
    # Cache is not scoped by authorization context
    if user_id in cache:
        return cache[user_id]

    profile = load_profile_from_db(user_id)
    cache[user_id] = profile

    return profile


# ============================================================
# INSECURE DIRECT OBJECT ACCESS
# ============================================================

def get_invoice(invoice_id):
    # No authorization check
    return load_invoice(invoice_id)


def download_document(document_id):
    # Direct object reference without ownership validation
    return load_document(document_id)


# ============================================================
# UNSAFE DESKTOP / OS OPERATIONS
# ============================================================

def open_document(path):
    # Arbitrary local file access
    return os.popen("cat " + path).read()


def check_file(filename):
    # User-controlled command
    return os.system("ls -l " + filename)


# ============================================================
# HTTP SECURITY MISCONFIGURATION
# ============================================================

def call_internal_service(url):
    # TLS verification disabled
    response = requests.get(
        url,
        verify=False
    )

    return response.json()


def send_data(url, data):
    # Sends sensitive data to arbitrary URL
    return requests.post(
        url,
        json=data
    )


# ============================================================
# INSECURE COOKIE / SESSION EXAMPLE
# ============================================================

def create_session_response(session_id):
    # Missing Secure / HttpOnly / SameSite protections
    return {
        "Set-Cookie":
            f"session={session_id}"
    }


# ============================================================
# SECURITY MISCONFIGURATION
# ============================================================

DEBUG = True


def get_debug_info():
    # Sensitive information exposed in production
    if DEBUG:
        return {
            "api_key": API_KEY,
            "database_password": DATABASE_PASSWORD,
            "jwt_secret": JWT_SECRET
        }

    return {}


# ============================================================
# INCORRECT AUTHORIZATION CHECK
# ============================================================

def access_admin_panel(user):
    # Checks only authentication, not authorization
    if user.is_authenticated:
        return "Welcome to admin panel"

    return "Unauthorized"


def change_user_role(current_user, target_user, new_role):
    # Missing privilege check
    target_user.role = new_role
    return target_user


# ============================================================
# LOGIC BUG: WRONG COMPARISON
# ============================================================

def check_balance(balance):
    # Incorrect comparison
    if balance <= 0:
        return "sufficient"

    return "insufficient"


# ============================================================
# LOGIC BUG: WRONG RETURN VALUE
# ============================================================

def validate_password(password):
    if len(password) >= 8:
        return False

    return True


# ============================================================
# LOGIC BUG: ALWAYS TRUE CONDITION
# ============================================================

def check_role(role):
    if role == "admin" or "user":
        return True

    return False


# ============================================================
# LOGIC BUG: UNREACHABLE CODE
# ============================================================

def get_status(user):
    if user.is_active:
        return "active"
        print("This will never execute")

    return "inactive"


# ============================================================
# LOGIC BUG: VARIABLE SHADOWING
# ============================================================

def calculate_scores(scores):
    total = 0

    for scores in scores:
        total += scores

    # Original list variable has been shadowed
    return total


# ============================================================
# LOGIC BUG: OFF-BY-ONE
# ============================================================

def get_last_three(items):
    result = []

    for i in range(len(items) - 3):
        result.append(items[i])

    return result


# ============================================================
# LOGIC BUG: WRONG LOOP CONDITION
# ============================================================

def find_user(users, username):
    i = 0

    while i <= len(users):
        if users[i].username == username:
            return users[i]

        i += 1

    return None


# ============================================================
# LOGIC BUG: SHALLOW COPY
# ============================================================

def duplicate_user_profile(profile):
    # Nested objects remain shared
    return profile.copy()


# ============================================================
# LOGIC BUG: MUTABLE GLOBAL STATE
# ============================================================

active_users = []


def register_user(user):
    # Global mutable state
    active_users.append(user)

    return active_users


# ============================================================
# PLACEHOLDER FUNCTIONS USED BY BROKEN EXAMPLES
# ============================================================

def update_password(user_id, password_hash):
    return True


def load_profile_from_db(user_id):
    return {
        "id": user_id,
        "name": "Example User"
    }


def load_invoice(invoice_id):
    return {
        "id": invoice_id,
        "amount": 100
    }


def load_document(document_id):
    return {
        "id": document_id,
        "content": "document"
    }
