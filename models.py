from hashlib import md5
from peewee import SqliteDatabase, Model
from peewee import TextField, DateTimeField, ForeignKeyField, IntegerField, FloatField, PrimaryKeyField
from peewee import InternalError
import datetime

db = SqliteDatabase('app.db')


class BaseModel(Model):
    id = PrimaryKeyField(null=False)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


class User(BaseModel):
    login = TextField()
    password = TextField()

    class Meta:
        db_table = 'users'


class Student(BaseModel):
    name = TextField()
    surname = TextField()
    patronymic = TextField()
    phone = TextField()
    course = IntegerField()
    status = TextField()
    start_year = IntegerField()
    end_year = IntegerField()

    class Meta:
        db_table = 'students'


class Course(BaseModel):
    name = TextField()

    class Meta:
        db_table = 'courses'


class Academic_Performance(BaseModel):
    student = ForeignKeyField(Student, backref='academic_performances')
    course = ForeignKeyField(Course, backref='academic_performances')
    grade = FloatField()

    class Meta:
        db_table = 'academic_performances'


def user_seed():
    if User.select().count() == 0:
        User.create(login="Test", password=md5("Test".encode('utf-8')).hexdigest())


def student_seed():
    if Student.select().count() == 0:
        Student.insert_many([
            {'name': 'Иван', 'surname': 'Фролов', 'patronymic': 'Алексеевич', 'phone': '+913 999-99-99', 'course': 1, 'status': 'Обучается', 'start_year': 2022, 'end_year': 2025},
            {'name': 'Лидия', 'surname': 'Алексеевна', 'patronymic': 'Семенова', 'phone': '+913 999-99-98', 'course': 3, 'status': 'Отчислен', 'start_year': 2018, 'end_year': 2021},
            {'name': 'Ильар', 'surname': 'Петрович', 'patronymic': 'Семенова', 'phone': '+913 999-99-965', 'course': 2, 'status': 'В академическом отпуске', 'start_year': 2021, 'end_year': 2022},
        ]).execute()


def course_seed():
    if Course.select().count() == 0:
        Course.insert_many([
            {'name': 'Математика'},
            {'name': 'Физика'},
            {'name': 'Экономика'},
            {'name': 'Теория вероятности'},
            {'name': 'Программирование'},
        ]).execute()


def academic_performance_seed():
    if Academic_Performance.select().count() == 0:
        Academic_Performance.insert_many([
            {'student': 1, 'course': 2, 'grade': 3},
            {'student': 1, 'course': 4, 'grade': 5},
            {'student': 1, 'course': 3, 'grade': 4},
        ]).execute()


# Создаем таблицу если не существует.
try:
    db.connect()
    User.create_table()
    Student.create_table()
    Course.create_table()
    Academic_Performance.create_table()
    user_seed()
    course_seed()
    student_seed()
    academic_performance_seed()
except InternalError as px:
    print(str(px))
