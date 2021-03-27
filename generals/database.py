import psycopg2 as pg
from generals.templates import GET_SCHEMA_BY_SESSION


conn = pg.connect(
    user='tatfezxgvgaefs',
    password='05deb9321d5f3b4420fdccdd507e21f29c06baf2b8cd3d080ba39ef42e374d5e',
    host='ec2-54-155-208-5.eu-west-1.compute.amazonaws.com',
    port=5432,
    database='dm6a2f8rs68e1'
)


def SqlQuery(request, *params, my_conn=None):
    """
    Выполняет sql запрос
    :param request: Запрос. Для корректной вставки в запрос параметров нужно в запросе вставлять %s
    Пример: "select * from "table" where "type" = %s"
    :param params: Параметры, которые нужно вставить запрос
    :param my_conn: Потом расскажу
    :return:
    """
    if my_conn is None:
        cur = conn.cursor()
    else:
        cur = my_conn.cursor()
    cur.execute(request, tuple(params))
    if my_conn is None:
        conn.commit()
    return cur.fetchall() if cur else None

class Database:
    def __init__(self, clientid=None):
        self.clientid = clientid
        self.conn = pg.connect(
            user='tatfezxgvgaefs',
            password='05deb9321d5f3b4420fdccdd507e21f29c06baf2b8cd3d080ba39ef42e374d5e',
            host='ec2-54-155-208-5.eu-west-1.compute.amazonaws.com',
            port=5432,
            database='dm6a2f8rs68e1',
            options=f'-c search_path = {self.clientid + "," if self.clientid else ""}public'
        )

    def SqlQuery(self, request, *params, my_conn=None):
        """
        Выполняет sql запрос
        :param request: Запрос. Для корректной вставки в запрос параметров нужно в запросе вставлять %s
        Пример: "select * from "table" where "type" = %s"
        :param params: Параметры, которые нужно вставить запрос
        :param my_conn: Потом расскажу
        :return:
        """
        if my_conn is None:
            cur = self.conn.cursor()
        else:
            cur = my_conn.cursor()
        cur.execute(request, tuple(params))
        if my_conn is None:
            self.conn.commit()
        return cur.fetchall() if cur else None


def get_schema_by_session(session):
    return Database().SqlQuery(GET_SCHEMA_BY_SESSION, session)
