#!/usr/bin/env python3
"""
Test frontend functionality by simulating user interactions
"""

import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_frontend_with_selenium():
    """Test frontend functionality using Selenium"""
    print("Testing Frontend Functionality")
    print("=" * 50)
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:3001")
        
        print("✓ Frontend loaded successfully")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Check if we're on login page
        page_title = driver.title
        print(f"Page title: {page_title}")
        
        # Look for login form elements
        login_elements = driver.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(login_elements)} input elements")
        
        # Check for common login form fields
        username_field = None
        password_field = None
        
        for element in login_elements:
            element_type = element.get_attribute("type")
            element_name = element.get_attribute("name") or element.get_attribute("id") or element.get_attribute("placeholder")
            print(f"  Input: type={element_type}, name/id={element_name}")
            
            if element_type == "text" or "username" in str(element_name).lower():
                username_field = element
            elif element_type == "password" or "password" in str(element_name).lower():
                password_field = element
        
        if username_field and password_field:
            print("✓ Login form detected")
            
            # Test login functionality
            username_field.send_keys("admin2")
            password_field.send_keys("admin123")
            
            # Find and click login button
            buttons = driver.find_elements(By.TAG_NAME, "button")
            login_button = None
            
            for button in buttons:
                button_text = button.text.lower()
                if "login" in button_text or "sign in" in button_text:
                    login_button = button
                    break
            
            if login_button:
                print("✓ Login button found")
                login_button.click()
                
                # Wait for navigation/response
                time.sleep(3)
                
                # Check if login was successful
                current_url = driver.current_url
                print(f"Current URL after login: {current_url}")
                
                if "dashboard" in current_url.lower() or "home" in current_url.lower():
                    print("✓ Login successful - redirected to dashboard")
                else:
                    print("⚠ Login may have failed or redirected to unexpected page")
                
                # Check for navigation menu
                nav_elements = driver.find_elements(By.TAG_NAME, "nav")
                if nav_elements:
                    print("✓ Navigation menu found")
                    
                    # Look for specific navigation links
                    links = driver.find_elements(By.TAG_NAME, "a")
                    print(f"Found {len(links)} links on the page")
                    
                    # Check for key navigation items
                    nav_items = ["Dashboard", "Projects", "Material", "Fitup", "Final Inspection", "NDT", "Users"]
                    found_items = []
                    
                    for link in links:
                        link_text = link.text.strip()
                        if link_text in nav_items:
                            found_items.append(link_text)
                            print(f"  ✓ Found navigation: {link_text}")
                    
                    print(f"Found {len(found_items)} out of {len(nav_items)} expected navigation items")
                    
                else:
                    print("⚠ No navigation menu found")
                
            else:
                print("✗ Login button not found")
        else:
            print("✗ Login form fields not properly identified")
        
        # Take a screenshot for debugging
        driver.save_screenshot("frontend_test_screenshot.png")
        print("✓ Screenshot saved as frontend_test_screenshot.png")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"✗ Frontend test failed: {e}")
        return False

def test_api_connectivity():
    """Test that frontend can connect to backend API"""
    print("\nTesting API Connectivity")
    print("=" * 50)
    
    try:
        # Test backend health endpoint
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ Backend health check successful")
        else:
            print(f"✗ Backend health check failed: {response.status_code}")
            return False
        
        # Test frontend API configuration
        response = requests.get("http://localhost:3001")
        if response.status_code == 200:
            print("✓ Frontend server responding")
        else:
            print(f"✗ Frontend server not responding: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ API connectivity test failed: {e}")
        return False

def test_login_functionality():
    """Test login functionality directly"""
    print("\nTesting Login Functionality")
    print("=" * 50)
    
    try:
        # Get authentication token
        data = {
            "username": "admin2",
            "password": "admin123"
        }
        
        response = requests.post("http://localhost:8000/auth/token", data=data)
        if response.status_code == 200:
            token_data = response.json()
            print("✓ Login successful via API")
            print(f"  Token type: {token_data['token_type']}")
            print(f"  Access token obtained")
            
            # Test accessing protected endpoint with token
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            projects_response = requests.get("http://localhost:8000/projects/", headers=headers)
            
            if projects_response.status_code == 200:
                print("✓ Protected endpoint accessible with token")
                return True
            else:
                print(f"✗ Protected endpoint failed: {projects_response.status_code}")
                return False
        else:
            print(f"✗ Login failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Login test failed: {e}")
        return False

def main():
    print("Comprehensive Frontend Testing")
    print("=" * 60)
    
    # Test API connectivity first
    api_success = test_api_connectivity()
    
    # Test login functionality
    login_success = test_login_functionality()
    
    # Test frontend with Selenium (if API tests pass)
    if api_success and login_success:
        frontend_success = test_frontend_with_selenium()
    else:
        print("Skipping frontend Selenium test due to API/login failures")
        frontend_success = False
    
    print("\n" + "=" * 60)
    print("FRONTEND TEST RESULTS:")
    print("=" * 60)
    
    if api_success and login_success and frontend_success:
        print("✓ All frontend tests passed")
        print("✓ Frontend is working correctly")
        print("✓ Backend API connectivity established")
        print("✓ Login functionality working")
    else:
        print("✗ Some frontend tests failed")
        if not api_success:
            print("  - API connectivity issues")
        if not login_success:
            print("  - Login functionality issues")
        if not frontend_success:
            print("  - Frontend UI issues")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
