from texttable import Texttable
from helpers.decorators import except_handler
from models import Course


class CourseCRUD:

    def __init__(self, is_local=True):
        if is_local:
            self._visual_interface()

    @except_handler('При обработке данных возникла ошибка')
    def _visual_interface(self):
        is_repeat = True
        while is_repeat:
            print('Выберите действие 1-Список курсов 2-Добавить новый 3-Удалить')
            action = int(input('Выберите действие: '))
            if action == 1:
                self._list()
            elif action == 2:
                self._create()
            elif action == 3:
                self._destroy()
            else:
                print('Действие не найдено')

            if input('Назад (Да/Нет): ') == "Да":
                is_repeat = False

    def _create(self):
        name = input('Название: ')
        Course.create(name=name)
        print("Курс успешно добавлен")

    def _get_one(self):
        id = input('Course ID: ')
        return Course.get(Course.id == id)

    def _destroy(self):
        id = input('ID: ')
        q = Course.delete().where(Course.id == id)
        if q.execute() > 0:
            print('Курс успешно удален')
        else:
            print('При уладении курса возникла ошибка')

    def _list(self):
        self.__print_table(Course.select())

    def __print_table(self, elems):
        t = Texttable()
        t.add_row(['ID', 'Name'])
        t.set_cols_width([10, 100])
        for val in elems:
            t.add_row(self.__item_constructor(val))
        print(t.draw())

    def __item_constructor(self, item):
        return item.id, item.name
