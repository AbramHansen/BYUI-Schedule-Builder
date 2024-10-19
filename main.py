from section import Section, DeliveryMethod, Block

def test():
    cppSections = []
    dataStructuresSections = []
    psycologySections = []
    programmingWithClassesSections = []

    cppSections.append(Section([],'CSE 220C', 'A1', DeliveryMethod.Online, Block.Second, "C++ Language", 1))
    cppSections.append(Section([('W',13.25,14.25)],'CSE 220C', 'A2', DeliveryMethod.InPerson, Block.First, "C++ Language", 1))
    cppSections.append(Section([('W',13.25,14.25)],'CSE 220C', 'A3', DeliveryMethod.InPerson, Block.Second, "C++ Language", 1))
    cppSections.append(Section([],'CSE 220C', 'A4', DeliveryMethod.Online, Block.Second, "C++ Language", 1))

    dataStructuresSections.append(Section([
        ('M',14.5,16), ('W',14.5,16)
    ],'CSE 336', 'B3', DeliveryMethod.InPerson, Block.First, "Data Structures", 3))
    dataStructuresSections.append(Section([
        ('T',14.5,16), ('R',14.5,16)
    ],'CSE 336', 'B5', DeliveryMethod.InPerson, Block.Second, "Data Structures", 3))
    dataStructuresSections.append(Section([
        ('T',9,10), ('R',9,10)
    ],'CSE 336', 'B7', DeliveryMethod.InPerson, Block.First, "Data Structures", 3))
    dataStructuresSections.append(Section([
        ('T',10.25,11.25), ('R',10.25,11.25)
    ],'CSE 336', 'B9', DeliveryMethod.InPerson, Block.Second, "Data Structures", 3))

    psycologySections.append(Section([],'PSY 101', 'A15', DeliveryMethod.Online, Block.Full, "Intro to Psycology", 3))
    psycologySections.append(Section([
        ('M',9,10.5), ('W',9,10.5), ('F',9,10.5)
    ],'PSY 101', 'A14', DeliveryMethod.InPerson, Block.Full, "Intro to Psycology", 3))
    psycologySections.append(Section([
        ('M',10.5,12), ('W',10.5,12), ('F',10.5,12)
    ],'PSY 101', 'A15', DeliveryMethod.InPerson, Block.Full, "Intro to Psycology", 3))
    psycologySections.append(Section([
        ('M',14.5,16), ('W',14.5,16), ('F',14.5,16)
    ],'PSY 101', 'A17', DeliveryMethod.InPerson, Block.Full, "Intro to Psycology", 3))

    programmingWithClassesSections.append(Section([
        ('M',10.25,11.25), ('W',15,18), ('F',10.25,11.25)
    ],'CSE 220C', 'C4', DeliveryMethod.Flex, Block.Full, "Programming with Classes", 2))

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

def main():
    test()

if __name__=="__main__":
    main()