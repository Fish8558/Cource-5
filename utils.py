import psycopg2
import requests


def get_vacancies(employer_id: str) -> list:
    """Получение данных вакансий по API"""

    params = {
        'employer_id': employer_id,
        'page': 0,
        'per_page': 100
    }
    url = "https://api.hh.ru/vacancies/"
    data_vacancies = requests.get(url, params=params).json()

    vacancies_data = []
    for item in data_vacancies["items"]:
        salary = item["salary"]
        if salary:
            salary_from = salary['from']
            salary_to = salary['to']
            if salary_from and not salary_to:
                salary = salary_from
            elif not salary_from and salary_to:
                salary = salary_to
            elif salary_from and salary_to:
                salary = (salary_from + salary_to) / 2
        else:
            salary = None
        hh_vacancies = {
            'vacancy_id': int(item['id']),
            'vacancies_name': item['name'],
            'payment': salary,
            'requirement': item['snippet']['requirement'],
            'vacancies_url': item['alternate_url'],
            'employer_id': employer_id
        }
        if hh_vacancies['payment'] is not None:
            vacancies_data.append(hh_vacancies)

    return vacancies_data


def get_employer(employer_id: str) -> dict:
    """Получение данных о работодателе по API"""

    url = f"https://api.hh.ru/employers/{employer_id}"
    data_vacancies = requests.get(url).json()
    hh_company = {
        "employer_id": int(employer_id),
        "company_name": data_vacancies['name'],
        "open_vacancies": data_vacancies['open_vacancies']
    }

    return hh_company


def create_table(db_name: str, params: dict) -> None:
    """Создание БД, создание таблиц"""

    conn = psycopg2.connect(database="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()

    conn = psycopg2.connect(database=db_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE employers (
                    employer_id INTEGER PRIMARY KEY,
                    company_name varchar(255),
                    open_vacancies INTEGER
                    )""")

        cur.execute("""
                    CREATE TABLE vacancies (
                    vacancy_id INTEGER PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    vacancies_name varchar(255),
                    payment INTEGER,
                    vacancies_url TEXT,
                    requirement TEXT
                    )""")
    conn.commit()
    conn.close()


def add_to_table(employers_list: list, db_name: str, params: dict) -> None:
    """Заполнение базы данных компании и вакансии"""

    conn = psycopg2.connect(database=db_name, **params)
    with conn.cursor() as cur:
        cur.execute('TRUNCATE TABLE employers, vacancies RESTART IDENTITY;')

        for employer in employers_list:
            employer_info = get_employer(employer)
            cur.execute('INSERT INTO employers (employer_id, company_name, open_vacancies) '
                        'VALUES (%s, %s, %s)',
                        (employer_info['employer_id'], employer_info['company_name'],
                         employer_info['open_vacancies']))

            vacancy_list = get_vacancies(employer)
            print(f"Добавляем в БД вакансии работодателя {employer_info['company_name']}")
            for v in vacancy_list:
                cur.execute('INSERT INTO vacancies (vacancy_id, employer_id, vacancies_name, '
                            'payment, vacancies_url, requirement) '
                            'VALUES (%s, %s, %s, %s, %s, %s)',
                            (v['vacancy_id'], v['employer_id'], v['vacancies_name'], v['payment'],
                             v['vacancies_url'], v['requirement']))

    conn.commit()
    conn.close()
