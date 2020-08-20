from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import calendar

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# new_row = Table(task=task_string, deadline=datetime.strptime('01-24-2020', '%m-%d-%Y').date()
def add_todo(task_string, task_deadline=datetime.today()):
    if len(task_deadline) == 0:
        new_row = Table(task=task_string)
    else:
        new_row = Table(task=task_string, deadline=datetime.strptime(task_deadline, '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()
    pass


# add_todo('next thing to do')
def print_todo_list():
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print('Nothing to do!')
        pass
    else:
        print('All tasks:')
        for i, item in enumerate(rows, 1):
            print(f'{i}) {item}. {item.deadline.day} {item.deadline.strftime("%b")}')
        pass


# print_todo_list()

# print(first_row.task)
# print(first_row.id)
# print(first_row)
menu_items = {1: "Today's tasks",
              2: "Week's tasks",
              3: "All tasks",
              4: "Missed tasks",
              5: "Add task",
              6: "Delete task",
              0: "Exit"}


# def print_menu(items):
#     for i, item in enumerate(items, 1):
#         print(f'{i}) {item}')
#     pass

def print_dict(my_dict):
    print('')
    for key, value in my_dict.items():
        print(f'{key}) {value}')


def print_todays_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if len(rows) == 0:
        print(f"Today {today.day} {today.strftime('%b')}:")
        print('Nothing to do!')
        pass
    else:
        print(f"Today {today.day} {today.strftime('%b')}:")
        for i, item in enumerate(rows, 1):
            print(f'{i}) {item}')
        print('')
        pass


def print_weeks_tasks():
    today = datetime.today()
    week = [0, 1, 2, 3, 4, 5, 6]
    for day in week:
        weekday = today + timedelta(days=day)
        rows = session.query(Table).filter(Table.deadline == weekday.date()).all()
        if len(rows) == 0:
            print(f"{weekday.strftime('%A')} {weekday.day} {weekday.strftime('%b')}:")
            print('Nothing to do!')
            print('')
            pass
        else:
            print(f"{weekday.strftime('%A')} {weekday.day} {weekday.strftime('%b')}:")
            for i, item in enumerate(rows, 1):
                print(f'{i}) {item}')
            print('')
            pass


def print_missed_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline < today.date()).all()
    if len(rows) == 0:
        print(f"Today {today.day} {today.strftime('%b')}:")
        print('Nothing to do!')
        pass
    else:
        print(f"Today {today.day} {today.strftime('%b')}:")
        for i, item in enumerate(rows, 1):
            print(f'{i}) {item}')
        print('')
        pass


def delete_task(task_id):
    session.query(Table).filter(Table.id == task_id).delete()
    # don't forget to commit changes
    session.commit()
    pass


while True:
    print_dict(menu_items)
    user_input = input()
    if user_input == '1':
        print_todays_tasks()
    elif user_input == '2':
        print_weeks_tasks()
    elif user_input == '3':
        print_todo_list()
    elif user_input == '4':
        print_missed_tasks()
    elif user_input == '5':
        print('Enter task')
        some_task = input()
        print('Enter deadline')
        some_deadline = input()
        add_todo(some_task,some_deadline)
        print('The task has been added!')
    elif user_input == '6':
        print_todo_list()
        print('Choose the number of the task you want to delete:')
        user_input = input()
        delete_task(user_input)
        print('The task has been deleted!')
    elif user_input == '0':
        print('Bye!')
        exit()
