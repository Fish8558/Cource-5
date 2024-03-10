from DB_manager import DBManager
from config import config
from utils import create_table, add_to_table


def main():
    employers_list = [2071925, 88787, 1918903, 1204987, 5569859, 2223982, 238354, 9473594, 1008541, 40912]
    db_name = 'course_work_5'
    params = config()
    create_table(db_name, params)
    add_to_table(employers_list, db_name, params)
    dbmanager = DBManager(db_name, params)

    while True:
        task = input("\nВведите 1, чтобы получить список всех компаний и количество вакансий у каждой компании\n"
                     "Введите 2, чтобы получить список всех вакансий с указанием названия компании, "
                     "названия вакансии и зарплаты и ссылки на вакансию\n"
                     "Введите 3, чтобы получить среднюю зарплату по вакансиям\n"
                     "Введите 4, чтобы получить список всех вакансий, у которых зарплата выше средней по всем "
                     "вакансиям\n"
                     "Введите 5, чтобы получить список всех вакансий, в названии которых содержатся переданные в "
                     "метод слова\n"
                     "Введите Стоп, чтобы завершить работу\n"
                     )

        if task.lower() in ["стоп", "stop"]:
            break
        elif task == '1':
            dbmanager.get_companies_and_vacancies_count()
        elif task == '2':
            dbmanager.get_all_vacancies()
        elif task == '3':
            dbmanager.get_avg_salary()
        elif task == '4':
            dbmanager.get_vacancies_with_higher_salary()
        elif task == '5':
            keyword = input('Введите ключевое слово: ')
            dbmanager.get_vacancies_with_keyword(keyword)
        else:
            print('Неправильный запрос')


if __name__ == '__main__':
    main()
