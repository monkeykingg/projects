import json
import urllib.request
import itertools

API_TEMPLATE = 'https://cobalt.qas.im/api/1.0/courses/{}?key={}'
API_KEY = 'zX4y3ZSBFqDTGfc75q7YAB5ul3InWMCN'
WEEKDAY = {'MONDAY': 0, 'TUESDAY': 1, 'WEDNESDAY': 2, 'THURSDAY': 3, 'FRIDAY': 4}


class Section:
    def __init__(self, course_code, section_code, section_time):
        self.course_code = course_code
        self.section_code = section_code
        self.section_time = section_time

    def is_overlap(self, other):
        if self.course_code + self.section_code[0] == other.course_code + other.section_code[0]:
            return True
        for time1, time2 in list(itertools.product(self.section_time, other.section_time)):
            # Same day
            if time1[0] == time2[0]:
                if len(list(set(range(time1[1], time1[2])) & set(range(time2[1], time2[2])))) > 0:
                    return True

        return False

    def is_overlap_in_range(self, day, start, end):
        for time in self.section_time:
            if time[0] == day:
                if len(list(set(range(time[1], time[2])) & set(range(start, end)))) > 0:
                    return True

        return False

    def __str__(self):
        return "{} - {} : {}".format(self.course_code, self.section_code, self.section_time)


    def get_cells(self):
        result = []
        for time in self.section_time:
            for i in range(time[1], time[2]):
                result.append((time[0], i))
        return result

    def __hash__(self):
        return hash(self.course_code + self.section_code)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def get_length_on_day(self, day):
        for time in self.section_time:
            if time[0] == day:
                return time[2] - time[1]
        return 0


class Course:
    def __init__(self, course_code):
        self.course_code = course_code
        self.course_type = course_code[8]
        self.sections = {}
        self.load_section_info(course_code)

    def load_section_info(self, course_code):
        # Load json data from api.
        a = API_TEMPLATE.format(course_code, API_KEY)
        url = urllib.request.urlopen(a)
        result = json.loads(url.read().decode())

        # TODO: 404 FAILURE DETECTION

        # Convert into section_list
        for section in result['meeting_sections']:
            times = [(WEEKDAY[time['day']], get_time(time['start']), get_time(time['end'])) for time in
                     section['times']]
            section_initial = section['code'][0]
            self.sections[section_initial] = self.sections.get(section_initial, []) + [Section(course_code, section['code'], times)]

    def __hash__(self):
        return hash(self.course_code)

    def __eq__(self, other):
        return hash(self) == hash(other)

# Helper
def get_time(second):
    return int(second / 3600) - 9




if __name__ == '__main__':

    """ Course Object """
    c = Course('CSC108H1F20179')
    print('Course Code is', c.course_code)
    print('Course Type is', c.course_type)
    for section_type, sections in c.sections.items():
        print('---------------------------')
        print('Course section type', section_type)
        for s in sections:
            print(s.section_code)
            for time in s.section_time:
                print(' ' * 4, time)


    """Testing Overlap"""
    s1 = Section('Code1', 'L0101', [(0,1,2)])
    s2 = Section('Code2', 'L0103', [(0,1,2)])
    s3 = Section('Code1', 'L0103', [(0,5,8)])
    print('s1 & s3', s1.is_overlap(s3))
    print('s1 & s2', s1.is_overlap(s2))
    print('s2 & s3', s2.is_overlap(s3))


