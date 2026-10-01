import os


AMBIENTE = "dev"


def get_paths():
    base_path = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    if AMBIENTE == "dev":
        return {
            "ENV_PATH": os.path.join(
                base_path,
                "secrets",
                "sql_data_dev.env"
            ),

            "EXCEL_PORTES_ENVIO": os.path.join(
                base_path,
                "data",
                "portes_envio.xlsx"
            ),

            "EXCEL_PORTES_IMPORTACAO": os.path.join(
                base_path,
                "import",
                "portes_envio_importacao.xlsx"
            ),
        }

    raise SystemExit(
        f"Ambiente inválido: {AMBIENTE}"
    )