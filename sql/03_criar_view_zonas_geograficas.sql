USE SIIAN_PORTES;


CREATE OR ALTER VIEW dbo.vw_zonas_geograficas
AS

SELECT
    p.pais,
    p.zona,
    z.criterio_zona,
    z.codigo,
    z.localidade,

    p.escalao_peso,
    p.tipo_preco,

    p.preco_sem_iva,
    p.preco_texto,

    CASE
        WHEN p.prazo_min_dias IS NULL
             AND p.prazo_max_dias IS NULL
            THEN N'Nao fornecido'

        WHEN p.prazo_min_dias = p.prazo_max_dias
            THEN CONCAT(
                p.prazo_min_dias,
                N' dias'
            )

        WHEN p.prazo_min_dias IS NOT NULL
             AND p.prazo_max_dias IS NOT NULL
            THEN CONCAT(
                p.prazo_min_dias,
                N' a ',
                p.prazo_max_dias,
                N' dias'
            )

        WHEN p.prazo_min_dias IS NOT NULL
            THEN CONCAT(
                N'A partir de ',
                p.prazo_min_dias,
                N' dias'
            )

        ELSE CONCAT(
            N'Ate ',
            p.prazo_max_dias,
            N' dias'
        )
    END AS prazo

FROM dbo.portes_envio AS p

LEFT JOIN dbo.zonas_geograficas AS z
    ON p.pais = z.pais
    AND p.zona = z.zona
    AND p.servico = z.servico
    AND z.is_active = 1

WHERE p.is_active = 1;
