import cx_Oracle

from decouple import config


list_orgaos_query = """
    SELECT
        org.ORLW_ORGI_CDORGAO AS CDORG,
        org.ORLW_REGI_NM_REGIAO AS CRAAI,
        org.ORLW_CMRC_NM_COMARCA AS COMARCA,
        org.ORLW_COFO_NM_FORO AS FORO,
        org.ORLW_ORGI_NM_ORGAO AS ORGAO,
        func.NMFUNCIONARIO AS TITULAR
    FROM
        ORGI_VW_ORGAO_LOCAL_ATUAL org
        LEFT JOIN MPRJ_VW_FUNCIONARIO func ON func.CDORGAO = org.ORLW_DK
    WHERE
        1=1
        AND org.ORLW_TPOR_DK = 1
        AND (org.ORLW_ORGI_DT_FIM IS NULL
            OR org.ORLW_ORGI_DT_FIM > SYSDATE)
        AND func.CDTIPFUNC = 1
        AND func.CDSITUACAOFUNC = 1
        AND func.CDCARGO = 74
"""


def run(query, params):
    connection = cx_Oracle.connect(
            user=config('DS_EXADATA_user'),
            password=config('DS_EXADATA_password'),
            dsn=config('DS_EXADATA_CONN_SID'),
            encoding="UTF-8",
            nencoding="UTF-8"
    )

    cursor = connection.cursor()
    if params is None:
        return cursor.execute(query)
    return cursor.execute(query, params)
