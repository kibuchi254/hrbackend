"""
Simple test script to verify the API is working correctly
Run this after starting the server to test basic functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(test_name, response):
    """Print test result and response"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")

def main():
    """Run basic API tests"""
    print("\n" + "="*60)
    print("HR & Payroll SaaS API - Basic Tests")
    print("="*60)

    # 1. Health Check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response("Health Check", response)
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return

    # 2. Root Endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response("Root Endpoint", response)
    except Exception as e:
        print(f"❌ Root Endpoint Failed: {e}")

    # 3. Admin Login
    admin_token = None
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/admin/login",
            data={
                "username": "admin@hrpayroll.com",
                "password": "admin123"
            }
        )
        print_response("Admin Login", response)
        if response.status_code == 200:
            admin_token = response.json()["access_token"]
            print(f"✅ Admin login successful! Token: {admin_token[:50]}...")
        else:
            print("❌ Admin login failed!")
            return
    except Exception as e:
        print(f"❌ Admin Login Failed: {e}")
        return

    # 4. Get Admin Info
    if admin_token:
        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/auth/me",
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            print_response("Get Admin Info", response)
        except Exception as e:
            print(f"❌ Get Admin Info Failed: {e}")

    # 5. List Companies
    if admin_token:
        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/admin/companies",
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            print_response("List Companies", response)
        except Exception as e:
            print(f"❌ List Companies Failed: {e}")

    # 6. Create a Test Company
    company_id = None
    if admin_token:
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/admin/companies",
                headers={
                    "Authorization": f"Bearer {admin_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "name": "Test Company",
                    "business_email": "test@testcompany.com",
                    "phone": "+1234567890",
                    "owner_email": "testowner@testcompany.com",
                    "owner_password": "test123",
                    "owner_full_name": "Test Owner"
                }
            )
            print_response("Create Company", response)
            if response.status_code == 200:
                company_id = response.json()["id"]
                print(f"✅ Company created with ID: {company_id}")
        except Exception as e:
            print(f"❌ Create Company Failed: {e}")

    # 7. Login as Company Owner
    owner_token = None
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={
                "username": "testowner@testcompany.com",
                "password": "test123"
            }
        )
        print_response("Company Owner Login", response)
        if response.status_code == 200:
            owner_token = response.json()["access_token"]
            print(f"✅ Owner login successful! Token: {owner_token[:50]}...")
    except Exception as e:
        print(f"❌ Owner Login Failed: {e}")

    # 8. Get Company Dashboard Stats
    if owner_token:
        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/company/dashboard/stats",
                headers={"Authorization": f"Bearer {owner_token}"}
            )
            print_response("Get Dashboard Stats", response)
        except Exception as e:
            print(f"❌ Get Dashboard Stats Failed: {e}")

    # 9. Create a Department
    department_id = None
    if owner_token:
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/company/departments",
                headers={
                    "Authorization": f"Bearer {owner_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "name": "Engineering",
                    "description": "Software Development Team"
                }
            )
            print_response("Create Department", response)
            if response.status_code == 200:
                department_id = response.json()["id"]
                print(f"✅ Department created with ID: {department_id}")
        except Exception as e:
            print(f"❌ Create Department Failed: {e}")

    # 10. List Departments
    if owner_token:
        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/company/departments",
                headers={"Authorization": f"Bearer {owner_token}"}
            )
            print_response("List Departments", response)
        except Exception as e:
            print(f"❌ List Departments Failed: {e}")

    print("\n" + "="*60)
    print("Tests Complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
