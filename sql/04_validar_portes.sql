USE SIIAN_PORTES;




-- Contagem das tabelas
SELECT COUNT(*) AS total_portes
FROM dbo.portes_envio;

SELECT COUNT(*) AS total_zonas
FROM dbo.zonas_geograficas;



-- Contagem da view
SELECT COUNT(*) AS total_linhas_view
FROM dbo.vw_zonas_geograficas;



-- Ver amostra da view
SELECT TOP 100
    pais,
    zona,
    criterio_zona,
    codigo,
    localidade,
    escalao_peso,
    tipo_preco,
    preco_sem_iva,
    preco_texto,
    prazo
FROM dbo.vw_zonas_geograficas
ORDER BY
    pais,
    zona,
    localidade,
    escalao_peso;



-- Verificar tarifas sem correspondencia geografica
SELECT
    p.ref_portes,
    p.pais,
    p.zona,
    p.servico
FROM dbo.portes_envio AS p
LEFT JOIN dbo.zonas_geograficas AS z
    ON p.pais = z.pais
    AND p.zona = z.zona
    AND p.servico = z.servico
    AND z.is_active = 1
WHERE
    p.is_active = 1
    AND z.id_zona_geo IS NULL;



-- Verificar duplicacoes inesperadas na view
SELECT
    pais,
    zona,
    criterio_zona,
    codigo,
    localidade,
    escalao_peso,
    tipo_preco,
    preco_sem_iva,
    preco_texto,
    prazo,
    COUNT(*) AS total
FROM dbo.vw_zonas_geograficas
GROUP BY
    pais,
    zona,
    criterio_zona,
    codigo,
    localidade,
    escalao_peso,
    tipo_preco,
    preco_sem_iva,
    preco_texto,
    prazo
HAVING COUNT(*) > 1;
