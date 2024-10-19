import requests
from bs4 import BeautifulSoup
from section import Section, Block, DeliveryMethod

_delivery_conversion = {
    "Blended": DeliveryMethod.Blended,
    "In-Person": DeliveryMethod.InPerson,
    "In-Person OR Virtual Live (Flex)": DeliveryMethod.Flex,
    "Online": DeliveryMethod.Online,
    "Professionally Mentored": DeliveryMethod.ProfessionallyMentored,
    "Virtual Live": DeliveryMethod.VirtualLive,
}

class ScraperSession:
    VAR_PREFIX = "pg0$V$"
    SEARCH_PREFIX = f"{VAR_PREFIX}tabSearch$"
    DROPDOWN_PREFIX = f"{SEARCH_PREFIX}ddl"
    TEXT_PREFIX = f"{SEARCH_PREFIX}txt"
    CHECKBOX_PREFIX = f"{SEARCH_PREFIX}chk"
    BUTTON_PREFIX = f"{SEARCH_PREFIX}btn"

    def __init__(self):
        self._session = requests.Session()
        self._url = "https://student.byui.edu/ICS/Class_Schedule/"
        self._init = False
        
        self._viewstate: str | None = None
        self._viewstate_generator: str | None = None
        self._browser_refresh: str | None = None

    def _grab_hidden_data(self, html: str) -> dict[str, str]:
        """
        Grab the hidden data from the given html.

        :param html: The html to grab the hidden data from.
        :return: The hidden data.
        """

        soup = BeautifulSoup(html, "html.parser")

        hidden_inputs = soup.find_all("input", attrs={"type": "hidden"})

        hidden_data = {}
        for hidden_input in hidden_inputs:
            hidden_data[hidden_input["name"]] = hidden_input["value"]

        return hidden_data

    def _update_hidden_data(self, html: str):
        """
        Update the hidden data from the given html.

        :param html: The html to update the hidden data from.
        """

        hidden_data = self._grab_hidden_data(html)

        self._viewstate = hidden_data["__VIEWSTATE"]
        self._viewstate_generator = hidden_data["__VIEWSTATEGENERATOR"]
        self._browser_refresh = hidden_data["___BrowserRefresh"]

    def init_connection(self):
        res = self._session.get(self._url)
        self._init = True

        # Access important session info used by ASP.NET
        # soup = BeautifulSoup(res.text, "html.parser")

        # hidden_inputs = soup.find_all("input", attrs={"type": "hidden"})

        # hidden_data = {}
        # for hidden_input in hidden_inputs:
        #     hidden_data[hidden_input["name"]] = hidden_input["value"]

        self._update_hidden_data(res.text)

        # hidden_data = self._grab_hidden_data(res.text)

        # self._viewstate = hidden_data["__VIEWSTATE"]
        # self._viewstate_generator = hidden_data["__VIEWSTATEGENERATOR"]
        # self._browser_refresh = hidden_data["___BrowserRefresh"]
        
    def get_page(
            self,
            term: str,
            delivery_method: str = "",
            discipline: str = "",
            course_code: str = "",
            title: str = "",
            exclude_waitlisted: str = "on",
    ) -> str:
        """
        Get the HTML of the page for the given search parameters.
        At least term and one other parameter must be provided.

        :param term: The term to search for.
        :param delivery_method: The delivery method to search for.
        :param discipline: The discipline to search for.
        :param course_code: The course code to search for.
        :param exclude_waitlisted: Whether to exclude waitlisted courses.
        :return: The HTML of the page.
        """

        if not self._init:
            self.init_connection()

        # Check that term and at least one other parameter is provided
        if term == "":
            raise ValueError("Term must be provided.")
        if title == "" and delivery_method == "" and discipline == "" and course_code == "":
            raise ValueError("At least one parameter other than term must be provided.")
        
        if not self._init:
            self.init_connection()

        data = {
            "_scriptManager_HiddenField": "",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": self._viewstate,
            "__VIEWSTATEGENERATOR": self._viewstate_generator,
            "___BrowserRefresh": self._browser_refresh,
            "userName": "",
            "password": "",
            f"{self.DROPDOWN_PREFIX}TermSearch": term,
            f"{self.DROPDOWN_PREFIX}DeliveryMethod": delivery_method,
            f"{self.DROPDOWN_PREFIX}Dept": "",
            f"{self.DROPDOWN_PREFIX}Discipline": discipline,
            f"{self.TEXT_PREFIX}TitleRestrictor": title,
            f"{self.TEXT_PREFIX}CourseRestrictor": course_code,
            f"{self.CHECKBOX_PREFIX}ExcludeWaitlisted": exclude_waitlisted,
            f"{self.DROPDOWN_PREFIX}DivisionSearch": "",
            f"{self.BUTTON_PREFIX}Search": "Search",
            "q": "site:byui.edu",
        }

        res = self._session.post(self._url, data=data)
        if res.status_code != 200:
            raise ValueError(f"Failed to get page. Status code: {res.status_code}")

        self._update_hidden_data(res.text)

        return res.text

    def get_sections_data(
            self,
            term: str,
            delivery_method: str = "",
            discipline: str = "",
            course_code: str = "",
            title: str = "",
            exclude_waitlisted: str = "on",
    ) -> Section:
        """
        Get the sections data for the given search parameters.
        At least term and one other parameter must be provided.

        :param term: The term to search for.
        :param delivery_method: The delivery method to search for.
        :param discipline: The discipline to search for.
        :param course_code: The course code to search for.
        :param exclude_waitlisted: Whether to exclude waitlisted courses.
        :return: The sections data.
        """

        page = self.get_page(term, delivery_method, discipline, course_code, title, exclude_waitlisted)

        # with open("page.html", "w") as f:
        #     f.write(page)

        # exit()

        return self.parse_sections_data(page)

    def _parse_times(self, td: BeautifulSoup) -> tuple[list[tuple[str, float, float]], Block]:
        """
        Parse the times data from the given td.
        
        :param td: The td to parse.
        :return: The times data.
        """
            
        times = []
        block = None

        # The times are in an unordered list.
        ul = td.find("ul")

        # Each ui has its own time data.
        for li in ul.find_all("li"):
            # The text is in the format "{Days} {Start hh:mm}-{End hh:mm}{AM/PM} <div>...</div><div>...</div> <div>{location}</div>"

            # Get the text before the first div.
            # time_text = li_text.split("<div>")[0].strip()
            # print(time_text)
            # exit()

            time_text = li.contents[0].strip()

            # If no days, then it is an online class so let's skip it.
            if len(time_text.split(" ")) < 2:
                break
            days, time = time_text.split(" ")[:2]
            start, end = time.split("-")
            starts_am = False
            if start[-2:] == "AM":
                starts_am = True
                start = start[:-2]
            is_pm = end[-2:] == "PM"
            end = end[:-2]
            # Convert time to float, and if pm, add 12 hours.
            # Turn minutes into a decimal e.g. 30 minutes = 0.5 hours.
            start = float(start[:2]) + float(start[3:]) / 60
            end = float(end[:2]) + float(end[3:]) / 60
            if is_pm:
                start += 12
                end += 12
            if starts_am:
                start -= 12

            for day in days:
                times.append((day, start, end))

        # After the ul, there could be a div with class "subsess" which determines block. If it does not exist, it is full semester.
        subsess = td.find("div", class_="subsess")
        if subsess is not None:
            if "First" in subsess.text:
                block = Block.First
            elif "Second" in subsess.text:
                block = Block.Second
        else:
            block = Block.Full

        return times, block


    def parse_sections_data(self, page: str) -> Section:
        """
        Parse the sections data from the given page.

        :param page: The page to parse.
        :return: The sections data.
        """

        soup = BeautifulSoup(page, "html.parser")

        # Find the table with id "tableCourses"
        table = soup.find("table", attrs={"id": "tableCourses"})
        table_body = table.find("tbody")

        # Each row is a section with its data.
        # The first td is the add checkbox, which we don't need.
        # The second td is the course and section code inside an a tag.
        # The third td is the title.
        # The fourth td is the number of credits.
        # The fifth td is the class schedule. Its format is weird.
        # Format (What's directly inside the td):
        #  <ul ...><li>{Days} {Start hh:mm}-{End hh:mm}{AM/PM} <div>...</div><div>...</div><div>{location}</div></li></ul>{if is block class, then:}<div>{block}</div>
        # Days are represented by a single letter. M=Monday, T=Tuesday, W=Wednesday, R=Thursday, F=Friday, S=Saturday.
        # The sixth td doesn't matter.
        # The seventh td is the delivery method.

        sections = []
        
        for row in table_body.find_all("tr"):
            tds = row.find_all("td")
            
            code_and_section = tds[1].find("a").text
            course_code, section_number = code_and_section.split("-")
            title = tds[2].text.strip()
            _credits = float(tds[3].text.strip())

            times, block = self._parse_times(tds[4])
            delivery_method = _delivery_conversion[tds[6].text.strip()]

            sections.append(Section(times, course_code, section_number, delivery_method, block, title, _credits))

        return sections


if __name__ == "__main__":
    scraper = ScraperSession()
    # A bunch of tests
    # print(scraper.get_sections_data(term="2024;FA", discipline="CSE"))
    # print(scraper.get_sections_data(term="2024;FA", discipline="CSE", course_code="110"))
    # print(scraper.get_sections_data(term="2024;FA", title="Introduction"))
    print("Finding CSE 210")
    print(scraper.get_sections_data(term="2024;FA", course_code="210"))
    print("Finding CSE 111")
    # print("browser_refresh", scraper._browser_refresh, "\nviewstate", scraper._viewstate, "\nviewstate_generator", scraper._viewstate_generator)
    print(scraper.get_sections_data(term="2024;FA", course_code="111"))
    
