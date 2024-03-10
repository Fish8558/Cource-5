import psycopg2


class DBManager:
    """Класс для подключения к БД"""

    def __init__(self, bd_name: str, params: dict) -> None:
        self.bd_name = bd_name
        self.params = params

    def bd_connect(self, query: str = None):
        """Метод подключения к БД"""
        try:
            conn = psycopg2.connect(dbname=self.bd_name, **self.params)
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                for num, data in enumerate(result, 1):
                    print(f"{num}: {data}")
            conn.close()
        except Exception:
            print(f"Ошибка подключения к базе данных. Проверьте корректность данных.")

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех компаний и
        количество вакансий у каждой компании"""
        sql_query = ("""SELECT employers.company_name, COUNT(*) AS count_vacancies
                        FROM vacancies
                        JOIN employers USING (employer_id)
                        GROUP BY employers.company_name
                        ORDER BY count_vacancies DESC""")
        self.bd_connect(sql_query)

    def get_all_vacancies(self, keyword=None):
        """Метод получает список всех вакансий: название компании,
        название вакансии, зарплата и ссылка на вакансию.
        """
        sql_query = ("""SELECT employers.company_name, vacancies_name, payment, vacancies_url 
                        FROM vacancies
                        JOIN employers USING(employer_id)""")
        self.bd_connect(sql_query)

    def get_avg_salary(self):
        """Метод получает среднюю зарплату по вакансиям."""
        sql_query = ("""SELECT AVG(payment) AS avg_salary 
                        FROM vacancies""")
        self.bd_connect(sql_query)

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        sql_query = ("""SELECT * FROM vacancies
                        WHERE payment > (SELECT AVG(payment) FROM vacancies)
                        ORDER BY payment DESC""")
        self.bd_connect(sql_query)

    def get_vacancies_with_keyword(self, keyword: str) -> None:
        """Метод получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python."""
        sql_query = (f"""SELECT * FROM vacancies
                         WHERE lower(vacancies_name) LIKE '%{keyword}%'
                         OR lower(vacancies_name) LIKE '%{keyword}'
                         OR lower(vacancies_name) LIKE '{keyword}%'""")
        self.bd_connect(sql_query)
