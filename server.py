from flask import Flask, request

class Server:
    __codes = []

    __app = Flask(__name__)

    @__app.route('/')
    def index(self):
        return("Hello Index!")

    @__app.route('/submitcodes', methods=['POST'])
    def getSchedules(self):
        course_codes = request.form['course_codes']
        block = request.form['block']

        self.__codes = []
        if course_codes != "":
            code = ""
            for character in course_codes:
                if character != ',':
                    code += character
                else:
                    self.__codes.append(code)
                    code = ""
            self.__codes.append(code)

        print(self.__codes)

        return "Process Success", 200

    def start(self):
        self.__app.run()