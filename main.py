from section import Section, DeliveryMethod, Block
from scheduler import schedule
from scraper import ScraperSession
from server import startServer
import json

def test():
    cppSections = {}
    dataStructuresSections = {}
    psycologySections = {}
    programmingWithClassesSections = {}

    cppSections['A1'] = Section([], 'CSE 220C', 'A1', DeliveryMethod.Online, Block.second, "C++ Language", 1)
    cppSections['A2'] = Section([('W', 13.25, 14.25)], 'CSE 220C', 'A2', DeliveryMethod.InPerson, Block.first, "C++ Language", 1)
    cppSections['A3'] = Section([('W', 13.25, 14.25)], 'CSE 220C', 'A3', DeliveryMethod.InPerson, Block.second, "C++ Language", 1)
    cppSections['A4'] = Section([], 'CSE 220C', 'A4', DeliveryMethod.Online, Block.second, "C++ Language", 1)

    dataStructuresSections['B3'] = Section([
        ('M', 14.5, 16), ('W', 14.5, 16)
    ], 'CSE 336', 'B3', DeliveryMethod.InPerson, Block.first, "Data Structures", 3)
    dataStructuresSections['B5'] = Section([
        ('T', 14.5, 16), ('R', 14.5, 16)
    ], 'CSE 336', 'B5', DeliveryMethod.InPerson, Block.second, "Data Structures", 3)
    dataStructuresSections['B7'] = Section([
        ('T', 9, 10), ('R', 9, 10)
    ], 'CSE 336', 'B7', DeliveryMethod.InPerson, Block.first, "Data Structures", 3)
    dataStructuresSections['B9'] = Section([
        ('T', 10.25, 11.25), ('R', 10.25, 11.25)
    ], 'CSE 336', 'B9', DeliveryMethod.InPerson, Block.second, "Data Structures", 3)

    psycologySections['A15'] = Section([], 'PSY 101', 'A15', DeliveryMethod.Online, Block.full, "Intro to Psychology", 3)
    psycologySections['A14'] = Section([
        ('M', 9, 10.5), ('W', 9, 10.5), ('F', 9, 10.5)
    ], 'PSY 101', 'A14', DeliveryMethod.InPerson, Block.full, "Intro to Psychology", 3)
    psycologySections['A13'] = Section([
        ('M', 10.5, 12), ('W', 10.5, 12), ('F', 10.5, 12)
    ], 'PSY 101', 'A13', DeliveryMethod.InPerson, Block.full, "Intro to Psychology", 3)
    psycologySections['A17'] = Section([
        ('M', 14.5, 16), ('W', 14.5, 16), ('F', 14.5, 16)
    ], 'PSY 101', 'A17', DeliveryMethod.InPerson, Block.full, "Intro to Psychology", 3)

    programmingWithClassesSections['C4'] = Section([
        ('M', 10.25, 11.25), ('W', 15, 18), ('F', 10.25, 11.25)
    ], 'CSE 210', 'C4', DeliveryMethod.Flex, Block.full, "Programming with Classes", 2)

    testSections = {}
    testSections['CSE 220C'] = cppSections
    testSections['CSE 336'] = dataStructuresSections
    testSections['PSY 101'] = psycologySections
    testSections['CSE 210'] = programmingWithClassesSections
    
    for course in testSections:
        print("\t\t\t\t" + course + "\n")
        for section in testSections[course]: 
            print(section)
        print("\n\n\n\n")


    classes = {}
    add_class(classes, cppSections)
    add_class(classes, dataStructuresSections)
    add_class(classes, psycologySections)
    add_class(classes, programmingWithClassesSections)

    for key, value in classes.items():
        print(f"{key}: {value}")
        print("")

    schedule(classes)

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

def scraper_schedule_test():
    scraper = ScraperSession()
    all_classes = {}
    pwc = scraper.get_sections_data(term="2024;FA", course_code="cse 210")
    pwf = scraper.get_sections_data(term="2024;FA", course_code="cse 111")
    pwd = scraper.get_sections_data(term="2024;FA", course_code="cse 212")
    pwi = scraper.get_sections_data(term="2024;FA", course_code="cse 110")
    rel = scraper.get_sections_data(term="2024;FA", course_code="REL 225c")

    
    # print(pwc)
    print(pwf)
    print(pwd)

    classes = {}
    add_class(classes, pwc)
    add_class(classes, pwf)
    add_class(classes, pwd)
    add_class(classes,pwi)
    add_class(classes,rel)

    all_classes = courseToDict(all_classes, pwc)
    all_classes = courseToDict(all_classes, pwf)
    all_classes = courseToDict(all_classes, pwd)
    all_classes = courseToDict(all_classes, pwi)
    all_classes = courseToDict(all_classes, rel)


    # New schedule is a list of tuples of course code and section
    new_schedule = schedule(classes)

    # print(new_schedule)

    json_schedule = schedule_to_json(new_schedule, all_classes)
    print(json_schedule)

def main():
    #scraper_schedule_test()
    startServer()

if __name__=="__main__":
    main()