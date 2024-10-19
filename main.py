from section import Section, DeliveryMethod, Block

def test():
    testSection = []

    testSection.append(Section([],'CSE 220C', 'A1', DeliveryMethod.Online, Block.Second, "C++ Language", 1))
    testSection.append(Section([
        ('T',14.5,16), ('R',14.5,16)
    ],'CSE 336', 'B3', DeliveryMethod.InPerson, Block.First, "Data Structures", 3))
    testSection.append(Section([
        ('M',10.25,11.25), ('W',10.25,11.25), ('F',10.25,11.25)
    ],'PSY 101', 'A15', DeliveryMethod.InPerson, Block.Full, "Intro to Psycology", 3))
    testSection.append(Section([
        ('M',10.25,11.25), ('W',15,18), ('F',10.25,11.25)
    ],'CSE 220C', 'C4', DeliveryMethod.Flex, Block.Full, "Programming with Classes", 2))

    for section in testSection:
        print(section)

def main():
    test()

if __name__=="__main__":
    main()