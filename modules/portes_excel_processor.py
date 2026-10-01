import pandas as pd


COLUNAS_PORTES = [
    "ref_portes",
    "pais",
    "servico",
    "zona",
    "produto",
    "valor_pedido",
    "peso_min_kg",
    "peso_max_kg",
    "escalao_peso",
    "tipo_preco",
    "preco_sem_iva",
    "preco_texto",
    "prazo_min_dias",
    "prazo_max_dias",
    "is_active",
]


COLUNAS_ZONAS = [
    "ref_zona_geo",
    "pais",
    "zona",
    "criterio_zona",
    "codigo",
    "localidade",
    "servico",
    "is_active",
]


def limpar_valor(valor):
    if pd.isna(valor):
        return None

    if hasattr(valor, "item"):
        try:
            valor = valor.item()
        except Exception:
            pass

    if isinstance(valor, pd.Timestamp):
        return valor.date()

    return valor


def validar_colunas(
    df,
    colunas_obrigatorias,
    nome_folha
):
    faltam = [
        coluna
        for coluna in colunas_obrigatorias
        if coluna not in df.columns
    ]

    if faltam:
        raise ValueError(
            f"Faltam colunas na folha "
            f"'{nome_folha}': {faltam}"
        )


def validar_referencias(
    df,
    coluna_ref,
    nome_folha
):
    refs = (
        df[coluna_ref]
        .dropna()
        .astype(str)
        .str.strip()
    )

    duplicados = refs[
        refs.duplicated(keep=False)
    ].unique()

    if len(duplicados) > 0:
        raise ValueError(
            f"Referencias duplicadas na folha "
            f"'{nome_folha}': "
            f"{list(duplicados)}"
        )


def processar_excel_portes(excel_file):
    df_portes = pd.read_excel(
        excel_file,
        sheet_name="portes_envio"
    )

    df_zonas = pd.read_excel(
        excel_file,
        sheet_name="zonas_geograficas"
    )

    validar_colunas(
        df_portes,
        COLUNAS_PORTES,
        "portes_envio"
    )

    validar_colunas(
        df_zonas,
        COLUNAS_ZONAS,
        "zonas_geograficas"
    )

    validar_referencias(
        df_portes,
        "ref_portes",
        "portes_envio"
    )

    validar_referencias(
        df_zonas,
        "ref_zona_geo",
        "zonas_geograficas"
    )

    registos_portes = []

    for _, row in df_portes.iterrows():
        registos_portes.append(
            {
                coluna: limpar_valor(
                    row[coluna]
                )
                for coluna in COLUNAS_PORTES
            }
        )

    registos_zonas = []

    for _, row in df_zonas.iterrows():
        registos_zonas.append(
            {
                coluna: limpar_valor(
                    row[coluna]
                )
                for coluna in COLUNAS_ZONAS
            }
        )

    return (
        registos_portes,
        registos_zonas
    )