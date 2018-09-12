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

list_vistas_query = """
    SELECT
        NVL(COUNT(TOTAL), 0) TOTAL,
        NVL(COUNT(HOJE), 0) HOJE,
        NVL(COUNT(ATE_30), 0) ATE_30,
        NVL(COUNT(DE_30_A_40), 0) DE_30_A_40,
        NVL(COUNT(MAIS_40), 0) MAIS_40
    FROM(
        SELECT
            1 TOTAL,
            CASE
                WHEN FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) < 1
                    AND FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) >= 0
                THEN 1
            END AS HOJE,
            CASE
                WHEN FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) <= 30
                    AND FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) >= 0
                THEN 1
            END AS ATE_30,
            CASE
                WHEN FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) <= 40
                    AND FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) > 30
                THEN 1
            END AS DE_30_A_40,
            CASE
                WHEN FLOOR(SYSDATE - VIST_DT_ABERTURA_VISTA) > 40
                THEN 1
            END AS MAIS_40
        FROM
            MCPR_VISTA
            JOIN MCPR_DOCUMENTO ON DOCU_DK = VIST_DOCU_DK
        WHERE
            (DOCU_ORGI_ORGA_DK_RESPONSAVEL = :org
                OR DOCU_ORGI_ORGA_DK_CARGA = :org)
            AND VIST_DT_FECHAMENTO_VISTA IS NULL
            AND DOCU_TPST_DK != 11
        ORDER BY 1 DESC
    )
"""

list_acervo_query = """
    WITH ENTRADAS AS(
        SELECT
            TO_CHAR(HRDC_DT_INI_RESPONSABILIDADE, 'YYYY-MM') AS MES_ANO,
            COUNT(HRDC_DOCU_DK) AS entradas
        FROM MCPR.MCPR_HISTORICO_RESP_DOCUMENTO
        WHERE HRDC_ORGI_DK_RESP_DOC = :org
        GROUP BY TO_CHAR(HRDC_DT_INI_RESPONSABILIDADE, 'YYYY-MM')
    ), SAIDAS AS (
        SELECT
            TO_CHAR(HRDC_DT_FIM_RESPONSABILIDADE, 'YYYY-MM') AS MES_ANO,
            COUNT(HRDC_DOCU_DK) AS SAIDAS
        FROM MCPR.MCPR_HISTORICO_RESP_DOCUMENTO
        WHERE
            HRDC_DT_FIM_RESPONSABILIDADE IS NOT NULL
            AND HRDC_ORGI_DK_RESP_DOC = :org
        GROUP BY TO_CHAR(HRDC_DT_FIM_RESPONSABILIDADE, 'YYYY-MM')
        UNION ALL
        SELECT
            TO_CHAR(HCFS_DT_INICIO, 'YYYY-MM') AS MES_ANO,
            COUNT(DOCU_DK) AS SAIDAS
        FROM
            MCPR_DOCUMENTO doc
            JOIN MCPR.MCPR_HISTORICO_FASE_DOC fdc
                ON doc.DOCU_DK = fdc.HCFS_DOCU_DK
        WHERE
            doc.DOCU_ORGI_ORGA_DK_RESPONSAVEL = :org
            AND HCFS_FSDC_DK = 2
        GROUP BY TO_CHAR(HCFS_DT_INICIO, 'YYYY-MM')
    )
    SELECT ENTRADAS.MES_ANO, MAX(ENTRADAS), SUM(SAIDAS)
    FROM ENTRADAS JOIN SAIDAS ON ENTRADAS.MES_ANO = SAIDAS.MES_ANO
    GROUP BY ENTRADAS.MES_ANO
    ORDER BY MES_ANO DESC
"""


acervo_qtd_query = """
    select count(DOCU_DK) as acervo_atual
    from MCPR_DOCUMENTO
    where
        DOCU_FSDC_DK = 1
        and DOCU_ORGI_ORGA_DK_RESPONSAVEL = :org
    group by DOCU_ORGI_ORGA_DK_RESPONSAVEL
"""

foto_mat_query = """
    SELECT foto, nome_arq FROM RH.RH_FUNC_IMG WHERE cdmatricula = :mat
"""

acervo_classe_pai_query = """
    WITH docs AS (
        SELECT
            (
                SELECT cls.cldc_dk cldc_dk_pai
                FROM mcpr_classe_docto_mp cls
                WHERE connect_by_isleaf = 1
                    CONNECT BY PRIOR cls.cldc_cldc_dk_superior = cls.cldc_dk
                    START WITH  d.docu_cldc_dk = cls.cldc_dk
            ) AS cldc_dk_pai,
            d.docu_dk
        FROM mcpr_documento d
        WHERE
            d.docu_fsdc_dk = 1
            AND DOCU_ORGI_ORGA_DK_RESPONSAVEL = :org
    )
    SELECT
        cldc_dk_pai CLASSE_ID_PAI,
        nvl(cldc_ds_classe, '* SEM CLASSE CADASTRADA *') CLASSE_PAI,
        count(docu_dk) QTD
    FROM docs
    LEFT JOIN mcpr_classe_docto_mp ON cldc_dk = cldc_dk_pai
    GROUP BY cldc_dk_pai, cldc_ds_classe
    ORDER BY 3 DESC
"""

list_detalhes_query = """
    select
    MMPM_ORDEM,
    MMPM_MAPA_CRAAI,
    MMPM_MAPA_FORUM,
    MMPM_MAPA_BAIRRO,
    MMPM_MAPA_MUNICIPIO,
    MMPM_CRAAI,
    MMPM_COMARCA,
    MMPM_FORO,
    MMPM_GRUPO,
    MMPM_ORGAO,
    MMPM_TELEFONESORGAO,
    MMPM_EXIBEGRUPO,
    MMPM_EXIBEFORO,
    MMPM_ORDEMGRUPO,
    MMPM_ORDEMQUADRO,
    MMPM_MATRICULA,
    MMPM_NOME,
    MMPM_CELULAR,
    MMPM_CARGO,
    MMPM_CONCURSO,
    MMPM_ANOCONCURSO,
    MMPM_ROMANO,
    MMPM_FUNCAO,
    MMPM_ORDEMSUBSTITUCAO,
    MMPM_FLAG_PGJ,
    MMPM_FLAG_ELEITORAL,
    MMPM_FLAG_CRAAI,
    MMPM_DIAS,
    nvl(MMPM_AFASTAMENTO,'') as MMPM_AFASTAMENTO,
    MMPM_PGJ_FUNCAO,
    MMPM_DTNASC,
    MMPM_DTINICIOSUBS,
    MMPM_DTFIMSUBS,
    MMPM_FLAG_ASSESSOR,
    MMPM_CDORGAO
    from MMPS.MMPS_ADM_RH_MOV_PROM
    where mmpm_cdorgao = :org
    order by MMPM_ORDEM, MMPM_ORDEMSUBSTITUCAO
"""


def run(query, params=None):
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
