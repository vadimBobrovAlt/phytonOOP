from texttable import Texttable
from courseCrud import CourseCRUD
from helpers.decorators import except_handler
from models import Student, Academic_Performance, User, Course


class StudentCRUD:

    def __init__(self, is_local=True):
        if is_local:
            self._visual_interface()

    @except_handler('При обработке данных возникла ошибка')
    def _visual_interface(self):
        is_repeat = True
        while is_repeat:
            print(
                'Выберите действие 1-Список студентов 2-Информация по студенту 3-Добавить нового 4-Изменить статус 5-Выставить оценку 6-Посмотреть оценки')
            action = int(input('Выберите действие: '))
            if action == 1:
                self._list()
            elif action == 2:
                self._one_print()
            elif action == 3:
                self._create()
            elif action == 4:
                self._update_status()
            elif action == 5:
                self._set_grade()
            elif action == 6:
                self._get_grades()
            else:
                print('Действие не найдено')

            if input('Назад (Да/Нет): ') == "Да":
                is_repeat = False

    def _create(self):
        name = input('Имя: ')
        surname = input('Фамилия: ')
        patronymic = input('Отчество: ')
        phone = input('Телефон: ')
        course = input('Курс: ')
        start_year = input('Дата начала обучения: ')
        end_year = input('Дата окончания обучения: ')
        status = 'Обучается'
        Student.create(
            name=name,
            surname=surname,
            patronymic=patronymic,
            phone=phone,
            course=course,
            start_year=start_year,
            end_year=end_year,
            status=status)
        print("Студент успешно добавлен")

    def _update_status(self):
        id = input('ID: ')
        status = input('Статус: ')
        q = Student.update(status=status).where(Student.id == id)
        if q.execute() > 0:
            print('Статус студента успешно обновлен')
        else:
            print('При обновление статуса возникла ошибка')

    def _list(self):
        self.__print_table(Student.select())

    def _get_one(self):
        id = input('Student ID: ')
        return Student.get(Student.id == id)

    def _set_grade(self):
        student = self._get_one()
        if student.get().status != 'Обучается':
            print(f'Студент в данный момент имеет статус: {student.status}.Выставление оценки невозможно')
            return
        courseCRUD = CourseCRUD(False)
        course = courseCRUD._get_one()
        result = Academic_Performance.get_or_none(student=student, course=course)
        if result is not None:
            print('Оценка уже выставлена')
            return

        grade = float(input('Оценка: '))
        Academic_Performance.create(student=student, course=course, grade=grade)
        print("Оценка успешно выставлена")

    def _get_grades(self):
        id = int(input('Student ID: '))
        grades = Academic_Performance.select().where(Academic_Performance.student_id == id)
        self.__print_table(grades, type='grade')

    def _one_print(self):
        self.__print_table([self._get_one()])

    def __print_table(self, elems, type='student'):
        title = ['ID', 'Name', 'Surname', 'Patronymic', 'Phone', 'Course', 'Start year', 'End year', 'Status']
        column_width = [10, 10, 10, 10, 20, 10, 10, 10, 30]
        if type == 'grade':
            title = ['ID', 'Course', 'Student', 'Grades']
            column_width = [10, 20, 20, 10]

        t = Texttable()
        t.add_row(title)
        t.set_cols_width(column_width)
        for val in elems:
            t.add_row(self.__item_constructor(val, type))
        print(t.draw())

    def __item_constructor(self, item, type):
        if type == 'student':
            return item.id, item.name, item.surname, item.patronymic, item.phone, item.course, item.start_year, item.end_year, item.status
        elif type == 'grade':
            return item.id, item.student.name, item.course.name, item.grade
