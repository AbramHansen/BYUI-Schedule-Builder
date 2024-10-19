from enum import Enum

DeliveryMethod = Enum('DeliveryMethod', ['Blended', 'InPerson', 'Flex', 'Online', 'Professionally Mentored', 'Virtual Live'])
Block = Enum('Block', ['Full', 'First', 'Second'])

class Section:
    def __init__(self, times: list, course_code: str, section_number: str, delivery_method: DeliveryMethod, block: Block, title: str, num_credits: int):
        self.times = times
        self.course_code = course_code
        self.section_number = section_number
        self.delivery_method = delivery_method
        self.block = block
        self.title = title
        self.num_credits = num_credits

    def __str__(self):
        timesString = "Times("

        for time in self.times:
            timesString += " Day: " + str(time[0])
            timesString += " Start: " + str(time[1])
            timesString += " End: " + str(time[2])

        timesString += ")\nCourse Code: "
        timesString += self.course_code
        timesString += "\nSection Number: "
        timesString += self.section_number
        timesString += "\nDelivery Method: "
        timesString += str(self.delivery_method)
        timesString += "\nBlock: "
        timesString += str(self.block)
        timesString += "\nTitle: "
        timesString += self.title
        timesString += "\nNumber of Credits: "
        timesString += str(self.num_credits)
        timesString += "\n\n\n\n"

        return timesString