USE SIIAN_PORTES;

CREATE INDEX ix_portes_envio_pais_zona
ON dbo.portes_envio (pais, zona);

CREATE INDEX ix_portes_envio_servico
ON dbo.portes_envio (servico);

CREATE INDEX ix_zonas_geograficas_pais_zona
ON dbo.zonas_geograficas (pais, zona);

CREATE INDEX ix_zonas_geograficas_codigo
ON dbo.zonas_geograficas (codigo);

CREATE INDEX ix_zonas_geograficas_localidade
ON dbo.zonas_geograficas (localidade);
