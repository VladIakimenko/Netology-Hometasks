from random import choice, randrange


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.average_grade()}\n'
                f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}')

    def __lt__(self, other):
        if isinstance(other, Student):
            if isinstance(self.average_grade(), float) \
                    and isinstance(other.average_grade(), float):
                return self.average_grade() < other.average_grade()
            else:
                print('Ошибка. Вы не можете сравнить студента, если у него нет оценок')
                return
        else:
            print('Ошибка. Вы можете сравнивать между собой только двух студентов')
            return

    def add_courses(self, course_name):
        if course_name not in self.finished_courses:
            self.finished_courses.append(course_name)

    def add_to_course(self, course_name):
        if course_name not in self.courses_in_progress \
                and course_name not in self.finished_courses:
            self.courses_in_progress.append(course_name)

    def average_grade(self, course=None):
        if self.grades:
            if course:
                return round(sum(self.grades[course]) / len(self.grades[course]), 2)
            else:
                return round(sum(sum(self.grades[key]) / len(self.grades[key])
                                 for key in self.grades) / len(self.grades), 2)
        else:
            return 'оценок нет'

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) \
                and course in self.courses_in_progress \
                and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')

    def add_courses(self, course_name):
        if course_name not in self.courses_attached:
            self.courses_attached.append(course_name)


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) \
                and course in self.courses_attached \
                and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return (super().__str__() +
                f'\nСредняя оценка за лекции: {self.average_grade()}')

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            if isinstance(self.average_grade(), float) \
                    and isinstance(other.average_grade(), float):
                return self.average_grade() < other.average_grade()
            else:
                print('Ошибка. Вы не можете сравнить лектора, если у него нет оценок')
                return
        else:
            print('Ошибка. Вы можете сравнивать лектора только с другим лектором.')
            return

    def average_grade(self, course=None):
        if self.grades:
            if course:
                return round(sum(self.grades[course]) / len(self.grades[course]), 2)
            else:
                return round(sum(sum(self.grades[key]) / len(self.grades[key])
                                 for key in self.grades) / len(self.grades), 2)
        else:
            return 'оценок нет'


def average_rate_by_course(netology, targets, course):
    avg_grade = []
    for target in netology[targets]:
        avg_grade.append(sum([grade for grade in target.grades[course]]) /
                         len(target.grades[course])) if course in target.grades \
                                                     else None
    return round(sum(avg_grade) / len(avg_grade), 2) if len(avg_grade) != 0 else 'Оценок нет'


def test_as_per_hometask():
    """Создаёт по 5 экземпляров каждого класса, вызывает все созданные методы"""

    netology = {
        'students': [],
        'reviewers': [],
        'lecturers': []
               }
    for _ in range(5):
        name, surname, gender = randomize('names')
        netology['students'].append(Student(name, surname, gender))

        name, surname, gender = randomize('names')
        netology['lecturers'].append(Lecturer(name, surname))

        name, surname, gender = randomize('names')
        netology['reviewers'].append(Reviewer(name, surname))

    for targets in netology:
        for target in netology[targets]:
            for _ in range(randrange(2, 5)):
                target.add_courses(randomize('course'))
            if targets == 'students':
                for _ in range(randrange(2, 5)):
                    target.add_to_course(randomize('course'))

    for _ in range(5):
        for student in netology['students']:
            for lecturer in netology['lecturers']:
                for course in student.courses_in_progress:
                    if course in lecturer.courses_attached:
                        student.rate_lecture(lecturer, course, randomize('grade'))

        for reviewer in netology['reviewers']:
            for student in netology['students']:
                for course in reviewer.courses_attached:
                    if course in student.courses_in_progress:
                        reviewer.rate_hw(student, course, randomize('grade'))
    print()
    print('\t\tСтуденты:')
    for student in netology['students']:
        print(student)
        print()
    print('Тестируем ">" и "<":')
    print(f"{netology['students'][0].name} {netology['students'][0].surname} > "
          f"{netology['students'][1].name} {netology['students'][1].surname}")
    print(netology['students'][0] > netology['students'][1])
    print(f"{netology['students'][2].name} {netology['students'][2].surname} < "
          f"{netology['students'][3].name} {netology['students'][3].surname}")
    print(netology['students'][2] < netology['students'][3])
    print()

    print('\t\tРевьюеры:')
    for reviewer in netology['reviewers']:
        print(reviewer)
        print()

    print('\t\tЛекторы:')
    for lecturer in netology['lecturers']:
        print(lecturer)
        print()
    print('Тестируем ">" и "<":')
    print(f"{netology['lecturers'][0].name} {netology['lecturers'][0].surname} > "
          f"{netology['lecturers'][1].name} {netology['lecturers'][1].surname}")
    print(netology['lecturers'][0] > netology['lecturers'][1])
    print(f"{netology['lecturers'][2].name} {netology['lecturers'][2].surname} < "
          f"{netology['lecturers'][3].name} {netology['lecturers'][3].surname}")
    print(netology['lecturers'][2] < netology['lecturers'][3])

    return netology


def randomize(item):
    men = [
        'Гришин Максим', 'Петров Тимофей', 'Иванов Иван', 'Харитонов Тимур', 'Поляков Иван',
        'Савельев Герман', 'Румянцев Анатолий', 'Парфенов Михаил', 'Мартынов Михаил',
        'Большаков Алексей', 'Шубин Глеб', 'Никифоров Альберт', 'Родионов Александр',
        'Кудрявцев Семён', 'Соловьев Михаил', 'Белоусов Кирилл', 'Бочаров Александр'
          ]
    women = [
        'Денисова Карина', 'Яковлева Анастасия', 'Денисова Алиса', 'Рогова Елена', 'Андреева Софья',
        'Андреева Валерия', 'Козлова София', 'Иванова Виктория', 'Волкова Ангелина', 'Михеева Арина',
        'Савина Виктория', 'Иванова Мария', 'Захарова София', 'Головина Диана', 'Терентьева Василиса'
            ]
    sex = ['муж.', 'жен.']
    courses = [
        'Система контроля версий Git', 'Fullstack-разработчик на Python', 'Английский для разработчиков',
        'Тестировщик ПО', 'Data Scientist с нуля до middle', 'Java-разработчик с нуля'
              ]

    if item == 'names':
        gender = choice(sex)
        if gender == 'муж.':
            name = choice(men).split()[1]
            surname = choice(men).split()[0]
        else:
            name = choice(women).split()[1]
            surname = choice(women).split()[0]
        return name, surname, gender

    elif item == 'course':
        course = choice(courses)
        return course

    elif item == 'grade':
        grade = randrange(1, 11)
        return grade


def dialogue_for_avg_rate_by_course(netology, targets, attribute):
    course = possible_courses_display(netology, targets, attribute)
    print(average_rate_by_course(netology, targets, course))


def possible_courses_display(netology, targets, attribute):
    print('Возможные курсы:')
    all_courses = set()
    for target in netology[targets]:
        for course in getattr(target, attribute):
            all_courses.add(course)
    print(*all_courses, sep=', ')
    course = input('Введите название курса:\n').strip()
    return course


def print_targets(netology, targets, attribute=None):
    if not attribute:
        print()
        for target in netology[targets]:
            print(target)
            print()
    else:
        course = possible_courses_display(netology, targets, attribute)

        targets_on_course = []
        for target in netology[targets]:
            if course in getattr(target, attribute):
                targets_on_course.append(target)
        print()
        print(*targets_on_course, sep='\n\n')


def char_details(netology):
    print('Введите имя и фамилию:\n'
          'Фамилию - обязательно, имя при необходимости:')
    names = input().strip().title().split()
    flag = False
    for key in netology:
        for character in netology[key]:
            if character.surname in names \
                    and (character.name in names or len(names) == 1):
                print()
                print('Студент') if isinstance(character, Student) \
                                 else print('Преподаватель')
                print(character)
                if isinstance(character, Mentor):
                    print('Закреплённые курсы:')
                    print(*character.courses_attached, sep=', ')
                if isinstance(character, Student) or \
                        isinstance(character, Lecturer):
                    print('Оценки по отдельным курсам:')
                    for course in character.grades:
                        if character.grades[course]:
                            print(course + ':', end='\t')
                            print(*character.grades[course])
                flag = True
    if not flag:
        print('Такой человек не найден!')


def print_help():
    return """
        help - список доступных команд
        
        char_details - вывести полную информацию о студенте или менторе
        
        avg_rate_s_by_course - вывести среднию оценку студентов по курсу
        avg_rate_l_by_course - вывести среднию оценку лекторов по курсу
        
        list_students - вывести список всех студентов
        list_s_by_course - вывести студентов на конкретном курсе
        list_s_fin_course - вывести студентов, завершивших кокретный курс
        
        list_lecturers - вывести список всех лекторов
        list_l_by_course - вывести список лекторов по конкретному курсу
        
        list_reviewers - вывести список всех ревьюеров
        list_r_by_course - вывести список ревьюеров по конкретному курсу
           """


def init_cmd(netology):
    commands = {
'help': (print_help, []),
'char_details': (char_details, [netology]),
'list_students': (print_targets, [netology, 'students']),
'list_s_by_course': (print_targets, [netology, 'students', 'courses_in_progress']),
'list_s_fin_course': (print_targets, [netology, 'students', 'finished_courses']),
'list_lecturers': (print_targets, [netology, 'lecturers']),
'list_l_by_course': (print_targets, [netology, 'lecturers', 'courses_attached']),
'list_reviewers': (print_targets, [netology, 'reviewers']),
'list_r_by_course': (print_targets, [netology, 'reviewers', 'courses_attached']),
'avg_rate_s_by_course': (dialogue_for_avg_rate_by_course, [netology, 'students', 'courses_in_progress']),
'avg_rate_l_by_course': (dialogue_for_avg_rate_by_course, [netology, 'lecturers', 'courses_attached']),
              }
    return commands


def main():
    input('Нажмите "enter", чтобы провести полевые испытания созданных классов')
    netology = test_as_per_hometask()
    commands = init_cmd(netology)

    while True:
        cmd = ''
        print()
        print('Введите "help", чтобы посмотреть список команд')
        while cmd not in commands:
            cmd = input().lower().strip()
        if cmd == 'help':
            print(print_help())
        else:
            commands[cmd][0](*commands[cmd][1])


main()
