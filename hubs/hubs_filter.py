import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def grab_hubs(newFileName):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    outputFile = open(f'{newFileName}.txt', "w")

    driver.get("https://www.bu.edu/hub/hub-courses/communication/")
    courses = driver.find_elements(By.CLASS_NAME, "cf-exp-col")

    wic = courses[1].find_element(By.ID, "wic")

    courses = (wic.find_elements(By.CLASS_NAME, "cf-course"))
    counter = 1

    for course in courses:
        print(counter)
        h3s = course.find_elements(By.TAG_NAME, "h3")

        courseString = ""
        for i in range(len(h3s)):
            elem = h3s[i]
            if i == 0:
                courseString += elem.find_element(By.CLASS_NAME, "cf-course-college").get_attribute('innerHTML')
                courseString += f' {elem.find_element(By.CLASS_NAME, "cf-course-dept").get_attribute('innerHTML')}'
                courseString += f' {elem.find_element(By.CLASS_NAME, "cf-course-number").get_attribute('innerHTML')}'
            else:
                courseString += f' - {elem.get_attribute("innerHTML")} | '
        
        hubs = course.find_elements(By.TAG_NAME, "li")
        for j in hubs:
            courseString += f'{j.get_attribute("innerHTML")}, '

        if "Global Citizenship and Intercultural Literacy" in courseString:
            outputFile.write(f'{courseString}\n')
        counter += 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Too many args: {len(sys.argv)} passed, 1 required')
        print("Call with: python hubs_filter <output_file>")
        sys.exit(1)
    grab_hubs(sys.argv[1], sys.argv[2])