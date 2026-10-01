def load_db_config(env_path):
    db_config = {}

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                db_config[key.strip()] = value.strip()

    return {
        "driver": db_config.get(
            "DB_DRIVER",
            "{ODBC Driver 18 for SQL Server}"
        ),
        "server": db_config.get("DB_SERVER", ""),
        "database": db_config.get("DB_DATABASE", ""),
        "username": db_config.get("DB_USERNAME", ""),
        "password": db_config.get("DB_PASSWORD", ""),
    }