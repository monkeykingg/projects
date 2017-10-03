from grade import GradeEntry
from grade import NumericGradeEntry
from grade import LetterGradeEntry

if __name__ == '__main__':
    grades = [NumericGradeEntry('csc148', 87, 1.0),
              NumericGradeEntry('bio150', 76, 2.0),
              LetterGradeEntry('his450', 'B+', 1.0)]
    for g in grades:
        print("Weight: {}, grade: {}, points: {}".format(g.course_weight,
                                                         g.course_grade,
                                                         g.get_points()))
        total = sum([g.course_weight * g.get_points() for g in grades])
        total_weight = sum([g.course_weight for g in grades])
    print("GPA = {}".format(total / total_weight))           