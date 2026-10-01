import pyodbc


def conectar_banco(db_config):
    try:
        conn_str = (
            f"DRIVER={db_config['driver']};"
            f"SERVER={db_config['server']};"
            f"DATABASE={db_config['database']};"
            f"UID={db_config['username']};"
            f"PWD={db_config['password']};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )

        conn = pyodbc.connect(
            conn_str,
            autocommit=False
        )

        print("✔ Conexão estabelecida.")
        return conn

    except Exception as e:
        print(
            f"❌ Erro ao conectar à base de dados: {e}"
        )
        return None