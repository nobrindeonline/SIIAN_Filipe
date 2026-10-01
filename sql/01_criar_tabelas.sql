USE SIIAN_PORTES;


CREATE TABLE dbo.portes_envio (
    id_portes INT IDENTITY(1,1) NOT NULL PRIMARY KEY,

    ref_portes NVARCHAR(100) NOT NULL UNIQUE,

    pais NVARCHAR(50) NULL,
    servico NVARCHAR(150) NULL,
    zona NVARCHAR(150) NULL,
    produto NVARCHAR(150) NULL,
    valor_pedido NVARCHAR(150) NULL,

    peso_min_kg DECIMAL(10,3) NULL,
    peso_max_kg DECIMAL(10,3) NULL,

    escalao_peso NVARCHAR(150) NULL,
    tipo_preco NVARCHAR(100) NULL,

    preco_sem_iva DECIMAL(12,3) NULL,
    preco_texto NVARCHAR(150) NULL,

    prazo_min_dias INT NULL,
    prazo_max_dias INT NULL,

    data_update DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    is_active BIT NOT NULL DEFAULT 1
);



CREATE TABLE dbo.zonas_geograficas (
    id_zona_geo INT IDENTITY(1,1) NOT NULL PRIMARY KEY,

    ref_zona_geo NVARCHAR(100) NOT NULL UNIQUE,

    pais NVARCHAR(50) NULL,
    zona NVARCHAR(150) NULL,
    criterio_zona NVARCHAR(100) NULL,
    codigo NVARCHAR(100) NULL,
    localidade NVARCHAR(200) NULL,
    servico NVARCHAR(150) NULL,

    data_update DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    is_active BIT NOT NULL DEFAULT 1
);
