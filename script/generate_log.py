import random
import json
import os
from datetime import datetime, timedelta

random.seed(42)

METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
ENDPOINTS = [
    "/api/users",
    "/api/users/12",
    "/api/login",
    "/api/orders",
    "/api/products",
    "/api/health",
]
IPS = ["192.168.1.42", "10.0.0.7", "172.16.0.3", "192.168.1.99"]
STATUS_CODES = [200, 200, 200, 201, 301, 400, 401, 403, 404, 500, 503]

lines = []
base_time = datetime(2024, 3, 15, 14, 0, 0)

# --- 60 standard lines (ISO timestamp) ---
for i in range(60):
    ts = (base_time + timedelta(seconds=i * 3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ip = random.choice(IPS)
    method = random.choice(METHODS)
    path = random.choice(ENDPOINTS)
    status = random.choice(STATUS_CODES)
    ms = random.randint(20, 800)
    lines.append(f"{ts} {ip} {method} {path} {status} {ms}ms")

# --- 15 lines with alternate timestamp (2024/03/15 14:23:01) ---
for i in range(15):
    ts = (base_time + timedelta(seconds=i * 7)).strftime("%Y/%m/%d %H:%M:%S")
    ip = random.choice(IPS)
    method = random.choice(METHODS)
    path = random.choice(ENDPOINTS)
    status = random.choice(STATUS_CODES)
    ms = random.randint(20, 600)
    lines.append(f"{ts} {ip} {method} {path} {status} {ms}ms")

# --- 10 lines with response time in seconds ---
for i in range(10):
    ts = (base_time + timedelta(seconds=i * 5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ip = random.choice(IPS)
    method = random.choice(METHODS)
    path = random.choice(ENDPOINTS)
    status = random.choice(STATUS_CODES)
    s = round(random.uniform(0.05, 2.5), 3)
    lines.append(f"{ts} {ip} {method} {path} {status} {s}s")

# --- 5 lines with Unix epoch timestamp ---
for i in range(5):
    epoch = 1710512581 + (i * 10)
    ip = random.choice(IPS)
    method = random.choice(METHODS)
    path = random.choice(ENDPOINTS)
    status = random.choice(STATUS_CODES)
    ms = random.randint(20, 400)
    lines.append(f"{epoch} {ip} {method} {path} {status} {ms}ms")

# --- 5 lines with missing status code ---
for i in range(5):
    ts = (base_time + timedelta(seconds=i * 11)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ip = random.choice(IPS)
    method = random.choice(METHODS)
    path = random.choice(ENDPOINTS)
    ms = random.randint(50, 300)
    lines.append(f"{ts} {ip} {method} {path} - {ms}ms")

# --- 4 JSON lines (2 normal, 2 with errors) ---
lines.append('{"level":"info","message":"Server started","port":8080}')
lines.append('{"level":"info","message":"Cache warmed up","keys":1024}')
lines.append('{"level":"error","message":"Database connection failed","host":"db-primary"}')
lines.append('{"level":"critical","message":"Out of memory exception","service":"worker"}')

# --- 3 stack trace fragments ---
lines.append("at com.example.UserService.getUser(UserService.java:42)")
lines.append("at com.example.ApiController.handle(ApiController.java:88)")
lines.append("\tat java.base/java.lang.Thread.run(Thread.java:834)")

# --- 3 error text lines ---
lines.append("2024-03-15T15:00:00Z ERROR NullPointerException at UserService line 42")
lines.append("2024-03-15T15:01:00Z CRITICAL database connection timeout after 30s")
lines.append("2024-03-15T15:02:00Z ERROR failed to parse request body")

# --- 5 blank lines ---
lines += [""] * 5

# --- 3 malformed/partial lines ---
lines.append("%%^&")
lines.append("--")
lines.append("??")

# Shuffle so deviations are spread throughout
random.shuffle(lines)

# Write output
output_path = os.path.join(os.path.dirname(__file__), "sample.log")
with open(output_path, "w") as f:
    for line in lines:
        f.write(line + "\n")

print(f"Generated {len(lines)} lines -> {output_path}")