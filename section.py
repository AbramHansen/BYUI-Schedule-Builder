from enum import Enum
from typing import List, Tuple

DeliveryMethod = Enum('DeliveryMethod', ['Blended', 'InPerson', 'Flex', 'Online', 'ProfessionallyMentored', 'VirtualLive'])
Block = Enum('Block', ['Full', 'First', 'Second'])

class Section:
    def __init__(self, times: List[Tuple[str, float, float]], course_code: str, section_number: str, delivery_method: DeliveryMethod, block: Block, title: str, num_credits: float):
        self.times = times
        self.course_code = course_code
        self.section_number = section_number
        self.delivery_method = delivery_method
        self.block = block
        self.title = title
        self.num_credits = num_credits

    def getSchedulerFormat(self):
        formatted_times = []
        for time in self.times:
            formatted_times.append((time[0],time[1],time[2],self.block.name))
        if len(formatted_times)==0:
            formatted_times.append(('Any',0,24,'full'))
        return (self.section_number,formatted_times)

    def __repr__(self) -> str:
        return self.__str__()

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

