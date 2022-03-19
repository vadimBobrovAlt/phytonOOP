from texttable import Texttable
from helpers.decorators import except_handler
from models import Course, Academic_Performance, Student
from studentCrud import StudentCRUD


class Report:

    def __init__(self):
        self._visual_interface()

    @except_handler('При обработке данных возникла ошибка')
    def _visual_interface(self):
        is_repeat = True
        while is_repeat:
            print('Выберите действие 1-Получить справку 2-Получить ведомость')
            action = int(input('Выберите действие: '))
            if action == 1:
                self._get_certificate()
            elif action == 2:
                self._get_statement()
            else:
                print('Действие не найдено')

            if input('Назад (Да/Нет): ') == "Да":
                is_repeat = False

    def _get_certificate(self):
        studentCRUD = StudentCRUD(False)
        student = studentCRUD._get_one()

        print("Справка")
        print(f"Выдана студенту {student.surname} {student.name} {student.patronymic} обучающимуся на {student.course} курсе,"
              f"год начала обучения {student.start_year} год окончания обучения {student.end_year} статус студента {student.status}")

    def _get_statement(self):
        id = int(input('Student ID: '))
        grades = Academic_Performance.select().where(Academic_Performance.student_id == id)
        print("Ведомость")
        print(f"Успеваемость студента { grades[0].student.surname } { grades[0].student.name } { grades[0].student.patronymic }")
        self.__print_table(grades)

    def __print_table(self, elems):
        t = Texttable()
        t.add_row(['ID', 'Course', 'Student', 'Grades'])
        t.set_cols_width([10, 20, 20, 10])
        for val in elems:
            t.add_row(self.__item_constructor(val))
        print(t.draw())

    def __item_constructor(self, item):
            return item.id, item.student.name, item.course.name, item.grade
