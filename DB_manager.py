import psycopg2


class DBManager:
    """Класс для подсключения к БД"""

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех компаний и
        количество вакансий у каждой компани"""

        with psycopg2.connect(host="localhost", database="course_work_5",
                              user="postgres", password="12345") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT company_name, COUNT(vacancies_name) AS count_vacancies  "
                            f"FROM employers "
                            f"JOIN vacancies USING (employer_id) "
                            f"GROUP BY employers.company_name")
                result = cur.fetchall()
            conn.commit()
        return result

    @property
    def get_all_vacancies(self, keyword=None):
        """Метод получает среднюю по ЗП вакансию
        у которыз ЗП выше средней по всемвакансия"""
        with psycopg2.connect(host="localhost", database="course_work_5",
                              user="postgres", password="12345") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies "
                            f"WHERE lower(vacancies_name) LIKE '%{keyword}%' "
                            f"OR lower(vacancies_name) LIKE '%{keyword}'"
                            f"OR lower(vacancies_name) LIKE '{keyword}%';")
                result = cur.fetchall()
            conn.commit()
        return result
