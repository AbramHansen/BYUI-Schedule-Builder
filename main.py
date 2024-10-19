from section import Section, DeliveryMethod, Block
from scheduler import schedule
from scraper import ScraperSession
from server import Server

def test():
    cppSections = []
    dataStructuresSections = []
    psycologySections = []
    programmingWithClassesSections = []

    cppSections.append(Section([],'CSE 220C', 'A1', DeliveryMethod.Online, Block.second, "C++ Language", 1))
    cppSections.append(Section([('W',13.25,14.25)],'CSE 220C', 'A2', DeliveryMethod.InPerson, Block.first, "C++ Language", 1))
    cppSections.append(Section([('W',13.25,14.25)],'CSE 220C', 'A3', DeliveryMethod.InPerson, Block.second, "C++ Language", 1))
    cppSections.append(Section([],'CSE 220C', 'A4', DeliveryMethod.Online, Block.second, "C++ Language", 1))

    dataStructuresSections.append(Section([
        ('M',14.5,16), ('W',14.5,16)
    ],'CSE 336', 'B3', DeliveryMethod.InPerson, Block.first, "Data Structures", 3))
    dataStructuresSections.append(Section([
        ('T',14.5,16), ('R',14.5,16)
    ],'CSE 336', 'B5', DeliveryMethod.InPerson, Block.second, "Data Structures", 3))
    dataStructuresSections.append(Section([
        ('T',9,10), ('R',9,10)
    ],'CSE 336', 'B7', DeliveryMethod.InPerson, Block.first, "Data Structures", 3))
    dataStructuresSections.append(Section([
        ('T',10.25,11.25), ('R',10.25,11.25)
    ],'CSE 336', 'B9', DeliveryMethod.InPerson, Block.second, "Data Structures", 3))

    psycologySections.append(Section([],'PSY 101', 'A15', DeliveryMethod.Online, Block.full, "Intro to Psycology", 3))
    psycologySections.append(Section([
        ('M',9,10.5), ('W',9,10.5), ('F',9,10.5)
    ],'PSY 101', 'A14', DeliveryMethod.InPerson, Block.full, "Intro to Psycology", 3))
    psycologySections.append(Section([
        ('M',10.5,12), ('W',10.5,12), ('F',10.5,12)
    ],'PSY 101', 'A13', DeliveryMethod.InPerson, Block.full, "Intro to Psycology", 3))
    psycologySections.append(Section([
        ('M',14.5,16), ('W',14.5,16), ('F',14.5,16)
    ],'PSY 101', 'A17', DeliveryMethod.InPerson, Block.full, "Intro to Psycology", 3))

    programmingWithClassesSections.append(Section([
        ('M',10.25,11.25), ('W',15,18), ('F',10.25,11.25)
    ],'CSE 210', 'C4', DeliveryMethod.Flex, Block.full, "Programming with Classes", 2))

    testSections = {}
    testSections['C++ Language'] = cppSections
    testSections['Data Structures'] = dataStructuresSections
    testSections['Intro to Psycology'] = psycologySections
    testSections['Programming with Classes'] = programmingWithClassesSections
    
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


def scraper_schedule_test():
    scraper = ScraperSession()
    pwc = scraper.get_sections_data(term="2024;FA", course_code="cse 210")
    pwf = scraper.get_sections_data(term="2024;FA", course_code="cse 111")
    pwd = scraper.get_sections_data(term="2024;FA", course_code="cse 212")

    # print(pwc)
    print(pwf)
    print(pwd)

    classes = {}
    add_class(classes, pwc)
    add_class(classes, pwf)
    add_class(classes, pwd)
    schedule(classes)

def main():
    scraper_schedule_test()
    server = Server()
    server.start()

if __name__=="__main__":
    main()