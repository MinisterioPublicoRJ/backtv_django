import cx_Oracle

from decouple import config

DS_EXADATA_HOST = config('DB_HOST')
DS_EXADATA_PORT = config('DB_PORT')
DS_EXADATA_SN = config('DB_SN')
DS_EXADATA_user = config('DB_USER')
DS_EXADATA_password = config('DB_PASSWORD')

DS_EXADATA_CONN_SID = cx_Oracle.makedsn(
    DS_EXADATA_HOST,
    DS_EXADATA_PORT,
    service_name=DS_EXADATA_SN)


def run(query, params=None):
    connection = cx_Oracle.connect(
            user=DS_EXADATA_user,
            password=DS_EXADATA_password,
            dsn=DS_EXADATA_CONN_SID,
            encoding="UTF-8",
            nencoding="UTF-8"
    )

    cursor = connection.cursor()
    if params is None:
        return cursor.execute(query)
    return cursor.execute(query, params)
