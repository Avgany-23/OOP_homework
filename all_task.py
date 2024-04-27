from abc import abstractmethod
from random import randint

class Comparisons_eq_lt:  # Класс для операторов наследования (дочерний класс Student and Lecturer)
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.grades = {}


    def __eq__(self, other):  # Для равенства и неравенства
        a1, a2 = self.average_r(self.grades), self.average_r(other.grades)
        return a1 == a2

    def __le__(self, other):
        a1, a2 = self.average_r(self.grades), self.average_r(other.grades)
        return a2 >= a1

    def average_r(self, grade):  # Средняя оценка за ДЗ по всем курсам
        return round(sum(list(map(lambda x: (sum(grade[x]) / len(grade[x])) / len(grade), grade))), 2)


class Student(Comparisons_eq_lt):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname)
        self.gender, self.finished_courses, self.courses_in_progress, self.grades = gender, [], [], {}
        self.grades_courses_lecturer = []  # Чтобы ставили только одну оценку за курс

    def add_courses_progress(self, item):
        self.courses_in_progress.append(item)

    def add_finished_courses(self, item):
        self.finished_courses.append(item)

    def rate_hw(self, lecturer, course, grade):
        self.check_grades_courses(lecturer, course, grade)
        self.grades_courses_lecturer.append(course)

        if lecturer.grades.get(course) is None:
            return lecturer.grades.setdefault(course, [grade])
        lecturer.grades[course].append(grade)

    def check_grades_courses(self, lecturer, course, grade):  # для проверки
        if course not in self.courses_in_progress:  # Студент должны быть на этом курсе
            raise AttributeError(f'Студент {self.name} {self.surname} не за креплен на курсе {course}')

        if course not in lecturer.courses_attached:  # Ментор должны быть на этом курсе
            raise AttributeError(f'Ментор {lecturer.name} {lecturer.surname} не за креплен на курсе {course}')

        if grade not in range(11):  # Оценка в диапазоне [0:10]
            raise AttributeError('Оценка должна быть от 0 до 10 включительно')

        if course in self.grades_courses_lecturer:  # Чтобы не ставили больше одной оценки
            raise AttributeError(f'Студент {self.name} уже поставил оценку за курс {course}')

    def __str__(self):
        return (f'{self.__class__.__name__}\n'
                f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.average_r(self.grades)}\n'
                f'Курсы в процессе изучения: {', '.join(map(str, self.courses_in_progress))}\n'
                f'Завершенные курсы: {', '.join(map(str, self.finished_courses))}')


class Mentor:
    def __init__(self, name, surname):
        self.name, self.surname = name, surname
        self.courses_attached = []

    def add_courses_attached(self, item):
        self.courses_attached.append(item)

    @abstractmethod  # У лектора (класс Lecturer) не будет доступа к выставлению оценок пока не переопределён этот метод
    def rate_hw(self, student, course, grade):
        raise UserWarning(f'{self.__name__} запрещено выставлять оценки')


class Lecturer(Mentor, Comparisons_eq_lt):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        # self.grades_lecture = {} # данный список заменён на список grades для наследования от класса Comparisons
        self.grades = {}

    def __str__(self):
        return (f'{self.__class__.__name__}\n'
                f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.average_r(self.grades)}')


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):  # Данный метод не менял
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f'{self.__class__.__name__}\n'
                f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')


# Добавление трех студентов
student1 = Student('Ruoy', 'Eman', 'M')
student2 = Student('Vlad', 'Even', 'M')
student3 = Student('Maria', 'Ivanova', 'D')

# Добавление курса Python, Java и Django в список проходимых студентами курсов
courses_in_progress = [(i.add_courses_progress('Python'), i.add_courses_progress('Java'), i.add_courses_progress('Django')) for i in (student1, student2, student3)]

# Добавление прошедших курсов студентами
finished_courses = [(i.add_finished_courses('Git'), i.add_finished_courses('Синтаксис ООП')) for i in (student1, student2, student3)]

# Добавление трех менторов (2 лектора и 1 проверяющий)
mentor1 = Lecturer('Some', 'Buddy')
mentor2 = Reviewer('Mark', 'Dunaev')
mentor3 = Lecturer('Job', 'Sunder')

# Добавление лекций, которые ведет ментор 1 и ментор 3
mentor1.add_courses_attached('Python')
mentor1.add_courses_attached('Java')
mentor3.add_courses_attached('Django')

# Выставление (случайных) оценок ментору 1 студентам по курсам Python, Java
grade_mentor1_Python = [i.rate_hw(mentor1, 'Python', randint(0, 10)) for i in (student1, student2, student3)]
grade_mentor1_Java = [i.rate_hw(mentor1, 'Java', randint(0, 10)) for i in (student1, student2, student3)]

# Выставление (случайных) оценок ментору 1 и ментору 3 студентами по курсу Django
grade_mentor3 = [i.rate_hw(mentor3, 'Django', randint(0, 10)) for i in (student1, student2, student3)]

# Добавление предметов, по которым ментор 2 (Reviewer) может ставить оценки
add_grades_mentor2 = [mentor2.add_courses_attached(course) for course in ('Python', 'Java', 'Django')]

# Выставление двух (случайных) оценок ментором 2 Студентам по курсам Python, Java и Django
for student in (student1, student2, student3):
    for courses in ('Python', 'Java', 'Django'):
        for _ in range(2):
            mentor2.rate_hw(student, courses, randint(0, 10))


x1 = mentor1.average_r(mentor1.grades)  # Средняя за все лекции оценка лектора ментора 1
x2 = mentor3.average_r(mentor3.grades)  # Средняя за все лекции оценка лектора ментора 3
y1 = student2.average_r(student2.grades)  # Средняя за все курсы оценка студента 2
y2 = student3.average_r(student3.grades)  # Средняя за все курсы оценка студента 3

# Вывод всех условий
print(f"{student1}\n{'-'*20}\n"
      f"{student2}\n{'-'*20}\n"
      f"{student3}\n{'-'*20}\n"
      f"{mentor1}\n{'-'*20}\n"
      f"{mentor2}\n{'-'*20}\n"
      f"{mentor3}\n{'-'*90}\n"
      f"Средняя за все лекции оценка лектора {mentor1.name} {mentor1.surname}: {x1}\n"
      f"Средняя за все лекции оценка лектора {mentor3.name} {mentor3.surname}: {x2}\n"
      f"Истинность равенства данных оценок: {x1} = {x2} --> {mentor1 == mentor3}\n"
      f"Истинность оператора сравнения данных оценок: {x1} ≥ {x2} --> {mentor1 >= mentor3}\n{'-'*20}\n"
      f"Средняя за все курсы оценка студента {student2.name} {student2.surname}: {y1}\n"
      f"Средняя за все курсы оценка студента {student3.name} {student3.surname}: {y2}\n"
      f"Истинность равенства данных оценок: {y1} = {y2} --> {student2 == student3}\n"
      f"Истинность оператора сравнения данных оценок: {y1} ≥ {y2} --> {student2 >= student3}\n{'-'*20}")


# Дз 4 (сказано функция, а не метод):
def avegare_grade_course_student(courses, *student):
    middle_grade_courses = 0
    middle_grade_courses += sum(map(lambda x: sum(x.grades[courses])/len(x.grades[courses]), student))
    return (f'Средняя оценка всех студентов за ДЗ по курсу {courses}: '
            f'{round(middle_grade_courses/len(student), 2)}')

print('\n'.join(list(map(lambda x: avegare_grade_course_student(x, student1, student2, student3),
                         ('Python', 'Java', 'Django')))), '\n')



'''
Небольшой комментарий: я сделал так, что определенный курс ведет только один ментор, следовательно студент может
выставлять только одну итоговую оценку за курс определенному ментору.
поэтому создал функцию по средней оценке лектора за проведенные им курсы
'''
def avegare_grade_courses_mentor(mentor, *courses):

    if not all(True if course in mentor.courses_attached else False for course in courses):  # Проверка на наличие
        not_course = list(filter(lambda x: x not in mentor.courses_attached, courses))
        return f'У {mentor.name} {mentor.surname} нет ведёт курсы {', '.join(map(str, not_course))}'

    middle_grade_course = []
    for course in courses:
        middle_grade_course.append(round(sum(mentor.grades[course])/len(mentor.grades[course]), 2))

    return (f'Средняя оценка {mentor.name} {mentor.surname} за лекции: '
            f'{', '.join(list(map(lambda x: f'{courses[x]}: {middle_grade_course[x]}', range(len(courses)))))}')

# Ментор 1 ведёт лекции только на курсах Python и Java
print(avegare_grade_courses_mentor(mentor1, 'Python', 'Java'))

# Ментор 3 ведёт лекции только на курсе Django
print(avegare_grade_courses_mentor(mentor3, 'Django'))

# Вылезет другое сообщение, так как ментор 3 не ведёт курс Python и Java. В ошибке появятся курсы, которых нет
print(avegare_grade_courses_mentor(mentor3, 'Django', 'Python', 'Java'))