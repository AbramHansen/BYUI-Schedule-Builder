from flask import Flask, request, jsonify
from scraper import ScraperSession
from utils import add_class, schedule_to_json, courseToDict
from scheduler import schedule
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return("Hello Index!")

@app.route('/submitcodes', methods=['POST'])
def getSchedules():
    course_codes = request.form['course_codes']
    block = request.form['block']

    courses = []
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
        courses.append(scraper.get_sections_data(term=block, course_code=code, delivery_method="P"))

    schedule_dict = {}
    mega_dict = {}
    for course in courses:
        add_class(schedule_dict, course)
        mega_dict = courseToDict(mega_dict, course)
    
    new_schedule = schedule(schedule_dict)
    json_schedule = schedule_to_json(new_schedule, mega_dict)

    return json_schedule, 200

@app.route('/getBlocks')
def getBlocks():
    scraper = ScraperSession()

    blocks = scraper.get_available_terms()

    return jsonify(blocks), 200

def startServer():
    app.run()