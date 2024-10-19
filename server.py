from flask import Flask, request
from scraper import ScraperSession

app = Flask(__name__)

@app.route('/')
def index():
    return("Hello Index!")

@app.route('/submitcodes', methods=['POST'])
def getSchedules():
    course_codes = request.form['course_codes']
    block = request.form['block']

    courses = {}
    codes = []
    if course_codes != "":
        code = ""
        for character in course_codes:
            if character != ',':
                code += character
            else:
                codes.append(code)
                code = ""
        codes.append(code)

    scraper = ScraperSession()

    for code in codes:
        courses[code] = scraper.get_sections_data(term=block, course_code=code)

    print(courses)

    return "Process Success", 200

def startServer():
    app.run()