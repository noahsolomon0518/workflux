import requests
import random
import string

URL = "http://localhost:5000/create/save-parts"

CUSTOMERS = [
    "Acme Manufacturing",
    "Boeing",
    "Lockheed Martin",
    "Raytheon",
    "SpaceX"
]

ENGINEERS = [
    "Jane Doe",
    "John Smith",
    "Alex Kim",
    "Sam Patel"
]

def rand_part_number():
    return "PN-" + "".join(random.choices(string.digits, k=5))

def rand_group_name(i):
    return f"Group-{i:02d}"

def make_part():
    return {
        "base_stock": {
            "customer_id": random.choice(CUSTOMERS),
            "external_part_number": rand_part_number(),
            "external_part_name": "Machined Shaft",
            "quantity": random.randint(1, 20),
            "extra_parts": random.randint(0, 3),
            "revision_number": random.choice(["A", "B", "C"]),
            "approval_engineer": random.choice(ENGINEERS),
        },
        "lathe_stock": {
            "overall_outer_dimensions": round(random.uniform(1.0, 4.0), 2),
            "overall_length": round(random.uniform(2.0, 12.0), 2),
            "bar_or_slug": random.choice(["bar", "slug"]),
            "workholding_grip": round(random.uniform(0.5, 2.0), 2),
            "clearance": round(random.uniform(0.05, 0.2), 3),
            "cutoff_blade_width": round(random.uniform(0.0625, 0.1875), 4),
            "clean_axial_stock": round(random.uniform(0.02, 0.1), 3),
            "clean_radial_stock": round(random.uniform(0.02, 0.1), 3),
            "round_outer_dimensions": round(random.uniform(0.9, 3.8), 2),
            "round_length": round(random.uniform(1.8, 11.5), 2)
        }
    }

def generate(num):
    for i in range(1, num+1):
        payload = {
            "group": dict(group_name=rand_group_name(i)),
            "parts": [make_part() for _ in range(random.randint(2, 5))]
        }
        resp = requests.post(URL, json=payload)

        print(f"Sent {payload['group']["group_name"]} → status {resp.status_code}")
        if resp.status_code != 200:
            print(resp.text)