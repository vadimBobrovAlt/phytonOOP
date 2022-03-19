from auth import Auth
from courseCrud import CourseCRUD
from helpers.decorators import except_handler
from report import Report
from studentCrud import StudentCRUD


@except_handler('При обработке данных возникла ошибка')
def visual_interface():
    print('программный модуль «Личные дела студентов»')
    auth = Auth()
    auth.login()
    print('Добро пожаловать в личный кабинет')
    is_repeat = True
    while is_repeat:
        print('Выберите действие 1-Управление студентами 2-Управление курсами 3-Формирование отчетов 4-Выйти')
        action = int(input('Выберите действие: '))
        if action == 1:
            StudentCRUD()
        elif action == 2:
            CourseCRUD()
        elif action == 3:
            Report()
        elif action == 4:
            break
        else:
            print('Действие не найдено')


if __name__ == '__main__':
    visual_interface()
