import json
from section import Section

def add_class(classes_dict, class_section_list):
    class_name = class_section_list[0].course_code
    sections = {}
    for course in class_section_list:
        time_stuff = course.getSchedulerFormat()
        sections[time_stuff[0]]=time_stuff[1]
    classes_dict[class_name] = sections


def schedule_to_json(new_schedule, classes_dict):
    course_list = []
    for code,section in new_schedule:
        course_list.append((classes_dict[code][section]).getSelfAsDict())
    return json.dumps(course_list)


def courseToDict(class_dict, section_list):
    section_dict = {}
    course_code = section_list[0].course_code
    for item in section_list:
        section_dict[item.section_number] = item
    class_dict[course_code] = section_dict
    return class_dict