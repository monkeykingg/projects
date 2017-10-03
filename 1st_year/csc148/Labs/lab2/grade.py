class GradeEntry:
    """A student record system at U of T
    
    A grade entry must keep track of three things:
  -- a course identifier, such as "CSC148".  This is the course
     in which the grade was earned.
  -- a course weight: 1.0 credits for a half-course, 2.0 credits
     for a full course
  -- a course grade, which has no meaningful value unless we know
     whether letter grades or numeric grades are used
A grade entry must also be able to generate how many points it is worth, based
on its grade.  The details of how points are generated are left
out unless we know whether letter or numeric grades are used.
       
    Attributes:
    ===========
    @type course_id: str
    @type course_weight: float
    @type course_grade: str/int
    """    
    def __init__(self, course_id, course_grade, course_weight):
        """init attributes
        
        @type self: GradeEntry
        @type course_id: str
        @type course_weight: float
        @type course_grade: str/int
        @rtype: none
        
        >>>system = GradeEntry("CSC148", 99, 0.5)
        >>>system.course_id
        "CSC148"
        >>>system.course_weight
        0.5
        """
        self.course_id = course_id
        self.course_weight = course_weight
        self.course_grade = course_grade
        self.points = 0
        
    def __eq__(self, other):
        """check if system is the same
        
        @type self: GradeEntry
        @type other: GradeEntry
        @rtype: bool
        
        >>>system1 = GradeEntry("CSC148", 0.5)
        >>>system2 = GradeEntry("CSC108", 1.0)
        >>>return(system1 == system2)
        False
        """
        if (self.course_id == other.course_id) and \
           (self.course_weight == other.course_weight):
            return True        
        
    def __str__(self):
        """return string of GradeEntry
        
        @type self: GradeEntry
        @rtype: str
        
        >>>system = GradeEntry("CSC148", 0.5)
        >>>print(system)
        Course: CSC148, Weight: 0.5, Grade: 
        """
        return "Course: {}, Weight: {}, Grade: {}".format(self.self.course_id, 
                                                          self.course_weight, 
                                                          self.course_grade)
    
    def get_points(self):
        """
        """
        if self.course_grade is int:
            self.points = self.num_to_points()
        elif self.course_grade is str:
            self.points = self.letter_to_points()
        return self.points
            
    
class NumericGradeEntry(GradeEntry):
    """A course grade with an integer value
    
    A numeric grade entry is a grade entry for which the grade is an integer 
    between 0 and 100 (inclusive).  A numeric grade entry generates grade points
    based on its grade, according to the following table:

    value   points
    --------------------
    90-100  4.0 	
    85-89	4.0
    80-84 	3.7
    77-79 	3.3
    73-76	3.0
    70-72 	2.7
    67-69 	2.3
    63-66	2.0
    60-62 	1.7
    57-59 	1.3
    53-56	1.0
    50-52 	0.7
    0-49 	0.0

    Attributes:
    ===========
    @type 
    """
    def __init__(self, course_id, course_grade, course_weight):
        """init attributes
            
        @type self: NumericGradeEntry
        @type numeric_grade: int
        @rtype: none
            
        >>>system = NumericGradeEntry("CSC148", 99, 0.5)
        >>>system.numeric_grade
        99
        """   
        self.course_id = course_id
        self.course_weight = course_weight        
        self.course_grade = course_grade
        self.points = 0
        
    def num_to_points(self):
        """
        """
        if 85 <= self.course_grade:
            self.points = 4.0
            return self.points
        elif 80 <= self.course_grade:
            self.points = 3.7
            return self.points
        elif 77 <= self.course_grade:
            self.points = 3.3  
            return self.points
        elif 73 <= self.course_grade:
            self.points = 3.0
            return self.points
        elif 70 <= self.course_grade:
            self.points = 2.7
            return self.points
        elif 67 <= self.course_grade:
            self.points = 2.3
            return self.points
        elif 63 <= self.course_grade:
            self.points = 2.0
            return self.points
        elif 60 <= self.coursec_grade:
            self.points = 1.7
            return self.points
        elif 57 <= self.course_grade:
            self.points = 1.3
            return self.points
        elif 53 <= self.course_grade:
            self.points = 1.0
            return self.points
        elif 50 <= self.course_grade:
            self.points = 0.7
            return self.points
        elif 0 <= self.course_grade:
            self.points = 0.0
            return self.points
            
    def get_points(self):
        """
        """
        self.points = self.num_to_points()
        return self.points
    
    
    
class LetterGradeEntry(GradeEntry):
    """A course grade entry with letter grades
    A letter grade entry is a grade entry for which the grade is a character.
    The value of the grade is one of {A, B, C, D, F}, with a possible suffix 
    from {+, -}. ALetterGradeEntry generates points, based on its grade, 
    according to the following table:
    
    value   grade-point
    -------------------
    A+ 	    4.0 	
    A 	    4.0
    A- 	    3.7
    B+ 	    3.3
    B 	    3.0
    B- 	    2.7
    C+ 	    2.3
    C 	    2.0
    C- 	    1.7
    D+ 	    1.3
    D 	    1.0
    D- 	    0.7
    F 	    0.0
   
    Attributes:
    ===========
    @type 
    """    
    def __init__(self, course_id, course_grade, course_weight):
        """init attributes
                
        @type self: LetterGradeEntry
        @type letter_grade: str
        @rtype: none
                
        >>>system = LetterGradeEntry("CSC148", "A", 0.5)
        >>>system.letter_grade
        "A"
        """   
        self.course_id = course_id
        self.course_weight = course_weight         
        self.course_grade = course_grade 
        self.points = 0
        
        
    def letter_to_points(self):
        """
        """
        if (self.course_grade == "A") or (self.course_grade == "A+"):
            self.points = 4.0
            return self.points
        elif self.course_grade == "A-":
            self.points = 3.7
            return self.points
        elif self.course_grade == "B+":
            self.points = 3.3  
            return self.points
        elif self.course_grade == "B":
            self.points = 3.0
            return self.points
        elif self.course_grade == "B-":
            self.points = 2.7
            return self.points
        elif self.course_grade == "C+":
            self.points = 2.3
            return self.points
        elif self.course_grade == "C":
            self.points = 2.0
            return self.points
        elif self.course_grade == "C-":
            self.points = 1.7
            return self.points
        elif self.course_grade == "D+":
            self.points = 1.3
            return self.points
        elif self.course_grade == "D":
            self.points = 1.0
            return self.points
        elif self.course_grade == "D-":
            self.points = 0.7 
            return self.points
        elif self.course_grade == "F":
            self.points = 0.0 
            return self.points
            
    def get_points(self):
        """
        """
        self.points = self.letter_to_points()    
        return self.points