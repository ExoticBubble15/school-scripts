import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def findBeg(str, txt):
    return str.index(txt)

def findEnd(str, txt):
    return findBeg(str, txt)+len(txt)

def grab_details(file, newFileName):
    print("running...")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    file = open(file, "r")
    fileText = file.read()
    fileTextArr = fileText.split("\n")

    newFile = open(f'{newFileName}.txt', "w")

    for i in range(len(fileTextArr)):
        if i % 20 == 0: print(f'{i}/{len(fileTextArr)}')

        line = fileTextArr[i]
        try:
            courseNum = line[0:findBeg(line, " ")]
            driver.get(f'https://www.bu.edu/academics/cas/courses/cas-cs-{courseNum}')
            content = driver.find_element(By.ID, "course-content").text
            preReqs = content[findEnd(content, "Undergraduate Prerequisites:")+1:findBeg(content, "-")-1]
            line += f' | {preReqs}\n'
            newFile.write(line)
        except:
            line += f' | no data\n'
            newFile.write(line)

    print("finished!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f'Too many args: {len(sys.argv)-1} passed, 2 required')
        print("Call with: python find_prereqs <input_file> <output_file>")
        sys.exit(1)
    grab_details(sys.argv[1], sys.argv[2])