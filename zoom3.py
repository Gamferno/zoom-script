import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import traceback
from concurrent.futures import ThreadPoolExecutor

def generate_random_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def login_process(meeting_id, password, participant_name):
    # Initialize a new driver instance for each participant with headless mode and GPU disabled
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Enable headless mode
    # chrome_options.add_argument('--disable-gpu')  # Disable GPU
    chrome_options.add_argument('--no-sandbox')  # Disables sandboxing which can cause issues in headless mode
    chrome_options.add_argument('--disable-dev-shm-usage')  # Helps with memory issues in Docker and CI/CD environments
    chrome_options.add_argument('--window-size=800,600')
    chrome_options.add_argument("--mute-audio")
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-infobars")
    # chrome_options.add_argument("--disable-software-rasterizer")    
    chrome_options.add_experimental_option(
        "prefs", {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.stylesheet": 2,
            "profile.managed_default_content_settings.fonts": 2,
        }
    )
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    sleep(5)

    try:
        # Navigate to the Zoom meeting
        driver.get(f'https://us04web.zoom.us/wc/join/{meeting_id}?')

        # Enter the password
        passcode_element = WebDriverWait(driver, 15).until(  # Increased timeout to 15 seconds
            EC.element_to_be_clickable((By.ID, "input-for-pwd"))
        )
        passcode_element.send_keys(password)
        print(f"Password entered for {participant_name}")

        sleep(2)

        # Enter the participant name
        name_element = WebDriverWait(driver, 15).until(  # Increased timeout to 15 seconds
            EC.presence_of_element_located((By.XPATH, '//*[@id="input-for-name"]'))
        )
        name_element.send_keys(participant_name)
        print(f"Name entered for {participant_name}")

        sleep(2)

        # Click the join button
        join_button = WebDriverWait(driver, 15).until(  # Increased timeout to 15 seconds
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div/div[2]/button'))
        )
        join_button.click()
        print(f"Join button clicked for {participant_name}")

        sleep(5)

        WebDriverWait(driver, 15).until(  # Increased timeout to 15 seconds
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div[1]/div[1]/footer/div[1]/div[1]/div[1]/button'))
        ).click()
        print(f"Proceeding after join button click1 for {participant_name}")

# /html/body/div[3]/div[2]/div/div[2]/div/div[1]/div[1]/footer/div[1]/div[1]/div[1]/button


        # Wait for the next join screen and click to proceed
        WebDriverWait(driver, 15).until(  # Increased timeout to 15 seconds
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div[1]/div[1]/div[8]/div[2]/div/div[3]/div/button'))
        ).click()
        print(f"Proceeding after join button click2 for {participant_name}")

    except Exception as e:
        print(f"Error in login process for {participant_name}: {e}")
        traceback.print_exc()
        driver.quit()

    return driver  # Return the driver instance for further actions



if __name__ == '__main__':

    meeting_id = input("Enter Meeting ID: ")
    meeting_id = "89262232749"
    # a=input("You want 8pm or 10pm (1 or 2) : ")
    # if a == 1:
    #     meeting_id = "89262232749"
    #     password_here="aiwt"
    # elif a==2: 
    #     meeting_id = "83012036919"
    #     password_here = "112233"
    # else:
    #     print("WARNING: WRONG INPUT! CODE WILL NOT WORK")
    #     quit()
    password_here = input("Enter Password: ")
    password_here = "aiwt"
    members = int(input("Enter no. of members: "))
    
    # List of random participant names
    # names = [
    #     "Aarav Sharma", "Priya Patel", "Vijay Reddy", "Ananya Kumar", "Rahul Singh", 
    #     "Neha Gupta", "Aditya Verma", "Aishwarya Desai", "Manish Mehta", "Sneha Nair", 
    #     "Rohan Joshi", "Pooja Shah", "Siddharth Iyer", "Simran Bhatia", "Karthik Agarwal", 
    #     "Anjali Choudhury", "Varun Kapoor", "Radhika Soni", "Aryan Pandey", "Shruti Jain", 
    #     "Aman Khanna", "Kritika Das", "Arjun Malhotra", "Swati Saxena", "Kiran Rao", 
    #     "Harsh Yadav", "Neelam Bhardwaj", "Tarun Gupta", "Kavya Rani", "Vivek Sharma", 
    #     "Tanya Mehra", "Pranav Chawla", "Divya Bajaj", "Sameer Saini", "Rakhi Prasad", 
    #     "Nikhil Deshmukh", "Komal Kapoor", "Gaurav Bhagat", "Richa Pandey", "Shubham Joshi", 
    #     "Aarti Yadav", "Deepak Singh", "Shalini Tyagi", "Rajesh Rao", "Snehal Chavan", 
    #     "Sahil Agarwal", "Pankaj Sharma", "Seema Rathi", "Tanvi Bansal", "Sandeep Kumar",
    #     "Devansh Mehta", "Kiran Patel", "Rhea Agarwal", "Nitin Kapoor", "Simran Singh"
    # ]



   # first_names = ["Aryan", "Anika", "Ishaan", "Riya", "Aditya", "Aisha", "Vihaan", "Sia", "Vivaan", "Diya", "Aarav", "Ira", "Ved", "Aanya", "Vivaan", "Avni", "Atharv", "Kiara", "Neil", "Saanvi", "Aarush", "Ananya", "Ayush", "Disha", "Vivaan", "Arya", "Advik", "Sanvi", "Kabir", "Mehak", "Shaurya", "Zoya", "Vivaan", "Esha", "Arjun", "Pari", "Vivaan", "Anika", "Rajveer", "Naina", "Vivaan", "Aanya", "Yash", "Anika", "Vivaan", "Aisha", "Aman", "Anamika", "Ananya", "Arnav", "Ayush", "Bhavya", "Daksh", "Diya", "Eshaan", "Hansika", "Harsh", "Ishan", "Ishita", "Jai", "Janvi", "Kaavya", "Kabir", "Krishna", "Lakshya", "Mihika", "Nandini", "Niyati", "Ojas", "Pari", "Pranav", "Rhea", "Ridhima", "Sahil", "Saumya", "Shaurya", "Shreya", "Siddhant", "Siya", "Tanisha", "Vivaan", "Yash", "Zara"]
    first_names= ['Aanya', 'Aarav', 'Aarush', 'Aditya', 'Advik', 'Aisha', 'Aman', 'Anamika', 'Ananya', 'Anika', 'Arjun', 'Arnav', 'Arya', 'Aryan', 'Atharv', 'Avni', 'Ayush', 'Bhavya', 'Daksh', 'Disha', 'Diya', 'Esha', 'Eshaan', 'Hansika', 'Harsh', 'Ira', 'Ishaan', 'Ishan', 'Ishita', 'Jai', 'Janvi', 'Kaavya', 'Kabir', 'Kiara', 'Krishna', 'Lakshya', 'Mehak', 'Mihika', 'Naina', 'Nandini', 'Neil', 'Niyati', 'Ojas', 'Pari', 'Pranav', 'Rajveer', 'Rhea', 'Ridhima', 'Riya', 'Saanvi', 'Sahil', 'Sanvi', 'Saumya', 'Shaurya', 'Shreya', 'Sia', 'Siddhant', 'Siya', 'Tanisha', 'Ved', 'Vihaan', 'Vivaan', 'Yash', 'Zara', 'Zoya']

    last_names=['Agarwal', 'Anand', 'Bhatia', 'Bhatt', 'Chaturvedi', 'Chauhan', 'Chopra', 'Dixit', 'Dubey', 'Dwivedi', 'Gaur', 'Gupta', 'Jaiswal', 'Joshi', 'Kapoor', 'Kar', 'Kashyap', 'Kaul', 'Kaur', 'Khaitan', 'Khanna', 'Khatri', 'Kohli', 'Kumar', 'Kushwaha', 'Maheshwari', 'Malhotra', 'Maurya', 'Mehra', 'Mehta', 'Mishra', 'Mittal', 'Modi', 'Mukherjee', 'Nagpal', 'Nanda', 'Narang', 'Nigam', 'Pal', 'Pandey', 'Parikh', 'Paswan', 'Patel', 'Purohit', 'Rai', 'Rajput', 'Ram', 'Rao', 'Rastogi', 'Rawat', 'Sahni', 'Sahu', 'Saxena', 'Shah', 'Shankar', 'Sharma', 'Shukla', 'Singh', 'Srivastava', 'Thakur', 'Tiwari', 'Trivedi', 'Verma', 'Yadav']
    #last_names = ["Sharma", "Kumar", "Patel", "Singh", "Verma", "Gupta", "Pandey", "Mishra", "Trivedi", "Joshi", "Dixit", "Tiwari", "Dwivedi", "Chaturvedi", "Srivastava", "Shukla", "Maurya", "Sahu", "Rai", "Thakur", "Jaiswal", "Yadav", "Singh", "Kushwaha", "Maurya", "Chauhan", "Pal", "Paswan", "Sahni", "Khatri", "Kaur", "Singh", "Bhatia", "Kapoor", "Anand", "Chopra", "Kohli", "Khanna", "Mehra", "Sharma", "Verma", "Gupta", "Pandey", "Mishra", "Agarwal", "Bhatt", "Chauhan", "Dubey", "Dwivedi", "Gaur", "Jaiswal", "Joshi", "Kapoor", "Kar", "Kashyap", "Kaul", "Khaitan", "Khanna", "Khatri", "Kohli", "Kumar", "Maheshwari", "Malhotra", "Mehra", "Mehta", "Mishra", "Mittal", "Modi", "Mukherjee", "Nagpal", "Nanda", "Narang", "Nigam", "Pandey", "Parikh", "Patel", "Purohit", "Rai", "Rajput", "Ram", "Rao", "Rastogi", "Rawat", "Saxena", "Sharma", "Shah", "Shankar", "Sharma", 

    names = [generate_random_name() for _ in range(members)]

    # Launch each participant concurrently using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        drivers = list(executor.map(lambda name: login_process(meeting_id, password_here, name), names))

    # After login, we can proceed to gather participant info
    # for driver in drivers:
    #     after_login(driver)

    # Keep the browsers open
    try:
        while True:
            sleep(1)  # Sleep to prevent high CPU usage
    except KeyboardInterrupt:
        # Close all browsers when stopping the script manually
        for driver in drivers:
            driver.quit()
