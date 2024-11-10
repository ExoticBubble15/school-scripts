import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def findBeg(str, txt):
    return str.index(txt)

def findEnd(str, txt):
    return findBeg(str, txt)+len(txt)

def grab_details(file, newFileName):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    file = open(file, "r")
    fileText = file.read()
    fileTextArr = fileText.split("\n")

    newFile = open(f'{newFileName}.txt', "w")

    for i in range(len(fileTextArr)):
        line = fileTextArr[i]
        try:
            print(f'line {i} start: {line}')
            courseNum = line[0:findBeg(line, " ")]
            driver.get(f'https://www.bu.edu/academics/cas/courses/cas-cs-{courseNum}')
            content = driver.find_element(By.ID, "course-content").text
            preReqs = content[findEnd(content, "Undergraduate Prerequisites:")+1:findBeg(content, "-")-1]
            line += f' | {preReqs}\n'
            newFile.write(line)
            print(f'line {i} done\n')
        except:
            line += f' | no data\n'
            newFile.write(line)
            print(f'line {i} ERROR\n')
    totalTime = time.time()-startTime
    print(f'total running time: {totalTime}s')
    print(f'average time per line: {totalTime/len(fileTextArr)}s')

if __name__ == "__main__":
    startTime = time.time()
    if len(sys.argv) != 3:
        print(f'Too many args: {len(sys.argv)} passed, 2 required')
        print("Call with: python find_prereqs <input_file> <output_file>")
        sys.exit(1)
    grab_details(sys.argv[1], sys.argv[2])