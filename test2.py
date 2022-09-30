class Student:


    global student_count
    student_count = 0
    
    def __init__(self, studentName):
        global student_count
        student_count += 1
        self.studentName = studentName
        pass
    @classmethod
    def funct1(self):
        print(student_count)


kevin = Student("kevin")
alan = Student("alan")
kevin4324 = Student("kevin")
alan4324 = Student("alan")
kevin5435 = Student("kevin")
alan54764 = Student("alan")

print(kevin.studentName)

print(alan.studentName)
print(kevin.funct1())