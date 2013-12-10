__author__ = 'tomek'


import os


class CompetitionReader(object):
    """Read data from file"""

    def __init__(self):
        self.data = Data()
        self.buffer = []

    def read(self, fileName):
        """Return data object with data from fileName"""

        self.buffer = self.readF2(fileName)

        self.getHeader()
        self.getCourses()
        self.getRooms()
        self.getCurricula()
        self.getConstraints()

        return self.data

    def readF(self, fileName):
        """Return content of file"""

        path = u"input/" + fileName
        f = open(path, "r")
        content = map(lambda x: x.rstrip('\n'), f.readlines())

        return content

    def readF2(self, fileName):
        """Return content of file"""
        path = u"timetable_scheduler/input/" + fileName
        f = open(path, "r")
        content = map(lambda x: x.rstrip('\n'), f.readlines())

        return content

    def readInstance(self, instanceNr):
        """Return data object with data from instance file"""

        self.buffer = self.readFile(instanceNr)

        self.getHeader()
        self.getCourses()
        self.getRooms()
        self.getCurricula()
        self.getConstraints()

        return self.data

    def readFile(self, instanceNr):
        """Return content of file"""

        path = u"data/Curriculum_based_Course_timetabling/datasets/comp" + str(instanceNr) + ".ctt"
        f = open(path, "r")
        content = map(lambda x: x.rstrip('\n'), f.readlines())

        return content

    def getHeader(self):
        """Get header from buffer"""

        self.data.instanceName = self.buffer[0].strip('Name: ')
        self.data.daysNum = int(self.buffer[3].strip('Days: '))
        self.data.periodsPerDay = int(self.buffer[4].strip('Periods_per_day: '))

    def getCourses(self):
        """Get courses from buffer"""

        index = self.buffer.index('COURSES:') + 1

        while self.buffer[index] != '':
            s = self.buffer[index].split()
            if len(s) > 5:
                course = Course(s[0], s[1], int(s[2]), int(s[3]), int(s[4]), s[5])
                self.data.courses.append(course)
            else:
                course = Course(s[0], s[1], int(s[2]), int(s[3]), int(s[4]))
                self.data.courses.append(course)
            index += 1

    def getRooms(self):
        """Get rooms from buffer"""

        index = self.buffer.index('ROOMS:') + 1

        while self.buffer[index] != '':
            s = self.buffer[index].split()
            if len(s)==3:
                room = Room(s[0], int(s[1]), s[2])
            else:
                room = Room(s[0], int(s[1]))
            self.data.rooms.append(room)

            index += 1

    def getCurricula(self):
        """Get curricula from buffer"""

        index = self.buffer.index('CURRICULA:') + 1

        while self.buffer[index] != '':
            s = self.buffer[index].split()
            curriculum = Curriculum(s[0], int(s[1]), s[2:])
            self.data.curricula.append(curriculum)

            index += 1

    def getConstraints(self):
        """Get constraints from buffer"""

        index = self.buffer.index('UNAVAILABILITY_CONSTRAINTS:') + 1

        while self.buffer[index] != '':
            s = self.buffer[index].split()
            constraint = Constraint(s[0], int(s[1]), int(s[2]))
            self.data.constraints.append(constraint)

            index += 1




class CompetitionDictReader(object):
    def readInstance(self, id):
        c = CompetitionReader()
        data = c.readInstance(id)
        return DictData(data)

    def read(self, path):
        c = CompetitionReader()
        data = c.read(path)
        return DictData(data)



class IData(object):
    instanceName = ""
    daysNum = 0
    periodsPerDay = 0

    def __str__(self):
        return " ".join([self.instanceName, (self.daysNum), str(self.periodsPerDay)])

class Data(IData):
    """Old data structure, linear search time for objects by ids"""
    def __init__(self):
        self.courses = []
        self.rooms = []
        self.curricula = []
        self.constraints = []
        self.instanceName = ""
        self.daysNum = 0
        self.periodsPerDay = 0

    def __str__(self):
        return " ".join([str(self.daysNum), str(self.periodsPerDay)])



    def getAllCourses(self):
        return self.courses

    def getAllRooms(self):
        return self.rooms

    def getAllCurricula(self):
        return self.curricula

    def getAllConstraints(self):
        return self.constraints



class DictData(IData):
    courses = {}
    rooms = {}
    curricula = {}
    constraints = {}

    curriculumLookup = {}

    """ convert old data object """
    def __init__(self, data):
        self.periodsPerDay, self.instanceName, self.daysNum = data.periodsPerDay, data.instanceName, data.daysNum
        for c in data.courses:
            self.courses[c.id] = c
        for r in data.rooms:
            self.rooms[r.id] = r

        self.curriculumLookup = {c.id: set() for c in data.getAllCourses()}

        for c in data.curricula:
            self.curricula[c.id] = c
            for m in c.members:
                self.curriculumLookup[m].add(c)

        self.constraints = { c.id: [] for c in data.constraints}
        for c in data.constraints:
            self.constraints[c.id].append(c)





    def getAllCourses(self):
        return self.courses.values()
    def getAllRooms(self):
        return self.rooms.values()
    def getAllCurricula(self):
        return self.curricula.values()
    def getAllConstraints(self):
        return sum(self.constraints.values(),[])



    def getCourse(self, id):
        return self.courses[id]
    def getRoom(self, id):
        return self.rooms[id]
    def getCurriculum(self, id):
        return self.curricula[id]
    def getConstraintsForCourse(self, id):
        return self.constraints[id]

    def getCurriculumForCourseId(self, courseId):
        return self.curriculumLookup[courseId] if courseId in self.curriculumLookup else set()


    def popCourse(self, id):
        self.courses[id].assignedLectureNum+=1


    def getUnfinishedCourses(self):
        return filter(lambda x: x.lectureNum>x.assignedLectureNum, self.getAllCourses())

class Model(object):
    def getId(self):
        return self.meta["id"]

class Course(Model):
    def __init__(self, id, teacher, lectureNum, minWorkingDays, studentsNum, typeOfRoom = None):
        self.id = id
        self.teacher = teacher
        self.lectureNum = lectureNum
        self.minWorkingDays = minWorkingDays
        self.studentsNum = studentsNum
        self.typeOfRoom = typeOfRoom
        self.assignedLectureNum = 0
class Room(Model):
    def __init__(self, id, capacity, type=None):
        self.id = id
        self.capacity = capacity
        self.type = type
    def __str__(self):
        return str(self.id)+" "+str(self.capacity)

class Curriculum(Model):
    def __init__(self, id, courseNum, members):
        self.id = id
        self.courseNum = courseNum
        self.members = members

class Constraint(Model):
    def __init__(self, id, day, dayPeriod):
        self.id = id
        self.day = day
        self.dayPeriod = dayPeriod
