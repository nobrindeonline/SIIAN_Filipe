import os
import sys
from decimal import Decimal, InvalidOperation
from datetime import date


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


from config.env_settings import get_paths
from config.db_config import load_db_config
from config.db_connection import conectar_banco
from modules.portes_excel_processor import processar_excel_portes


def normalizar_comparacao(valor):
    if valor is None:
        return None

    if isinstance(valor, str):
        return valor.strip()

    if isinstance(valor, bool):
        return int(valor)

    if hasattr(valor, "item"):
        try:
            valor = valor.item()
        except Exception:
            pass

    if isinstance(valor, (int, float, Decimal)):
        try:
            return Decimal(
                str(valor)
            ).normalize()
        except (InvalidOperation, ValueError):
            return valor

    return valor


def valores_diferentes(
    valor_sql,
    valor_excel
):
    return (
        normalizar_comparacao(valor_sql)
        !=
        normalizar_comparacao(valor_excel)
    )


def importar_portes(
    cursor,
    registos
):
    total_inserts = 0
    total_updates = 0
    total_sem_alteracao = 0

    for registo in registos:
        ref_portes = registo["ref_portes"]

        if ref_portes is None:
            continue

        ref_portes = str(
            ref_portes
        ).strip()

        if not ref_portes:
            continue

        cursor.execute(
            """
            SELECT
                pais,
                servico,
                zona,
                produto,
                valor_pedido,
                peso_min_kg,
                peso_max_kg,
                escalao_peso,
                tipo_preco,
                preco_sem_iva,
                preco_texto,
                prazo_min_dias,
                prazo_max_dias,
                is_active
            FROM dbo.portes_envio
            WHERE ref_portes = ?
            """,
            ref_portes
        )

        row = cursor.fetchone()

        valores_excel = (
            registo["pais"],
            registo["servico"],
            registo["zona"],
            registo["produto"],
            registo["valor_pedido"],
            registo["peso_min_kg"],
            registo["peso_max_kg"],
            registo["escalao_peso"],
            registo["tipo_preco"],
            registo["preco_sem_iva"],
            registo["preco_texto"],
            registo["prazo_min_dias"],
            registo["prazo_max_dias"],
            registo["is_active"],
        )

        if row:
            valores_sql = tuple(row)

            houve_alteracao = any(
                valores_diferentes(
                    valor_sql,
                    valor_excel
                )
                for valor_sql, valor_excel
                in zip(
                    valores_sql,
                    valores_excel
                )
            )

            if houve_alteracao:
                cursor.execute(
                    """
                    UPDATE dbo.portes_envio
                    SET
                        pais = ?,
                        servico = ?,
                        zona = ?,
                        produto = ?,
                        valor_pedido = ?,
                        peso_min_kg = ?,
                        peso_max_kg = ?,
                        escalao_peso = ?,
                        tipo_preco = ?,
                        preco_sem_iva = ?,
                        preco_texto = ?,
                        prazo_min_dias = ?,
                        prazo_max_dias = ?,
                        data_update = ?,
                        is_active = ?
                    WHERE ref_portes = ?
                    """,
                    registo["pais"],
                    registo["servico"],
                    registo["zona"],
                    registo["produto"],
                    registo["valor_pedido"],
                    registo["peso_min_kg"],
                    registo["peso_max_kg"],
                    registo["escalao_peso"],
                    registo["tipo_preco"],
                    registo["preco_sem_iva"],
                    registo["preco_texto"],
                    registo["prazo_min_dias"],
                    registo["prazo_max_dias"],
                    date.today(),
                    registo["is_active"],
                    ref_portes
                )

                total_updates += 1

                print(
                    f"UPDATE portes -> "
                    f"{ref_portes}"
                )

            else:
                total_sem_alteracao += 1

        else:
            cursor.execute(
                """
                INSERT INTO dbo.portes_envio (
                    ref_portes,
                    pais,
                    servico,
                    zona,
                    produto,
                    valor_pedido,
                    peso_min_kg,
                    peso_max_kg,
                    escalao_peso,
                    tipo_preco,
                    preco_sem_iva,
                    preco_texto,
                    prazo_min_dias,
                    prazo_max_dias,
                    data_update,
                    is_active
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                ref_portes,
                registo["pais"],
                registo["servico"],
                registo["zona"],
                registo["produto"],
                registo["valor_pedido"],
                registo["peso_min_kg"],
                registo["peso_max_kg"],
                registo["escalao_peso"],
                registo["tipo_preco"],
                registo["preco_sem_iva"],
                registo["preco_texto"],
                registo["prazo_min_dias"],
                registo["prazo_max_dias"],
                date.today(),
                registo["is_active"]
            )

            total_inserts += 1

            print(
                f"INSERT portes -> "
                f"{ref_portes}"
            )

    return (
        total_inserts,
        total_updates,
        total_sem_alteracao
    )


def importar_zonas(
    cursor,
    registos
):
    total_inserts = 0
    total_updates = 0
    total_sem_alteracao = 0

    for registo in registos:
        ref_zona_geo = (
            registo["ref_zona_geo"]
        )

        if ref_zona_geo is None:
            continue

        ref_zona_geo = str(
            ref_zona_geo
        ).strip()

        if not ref_zona_geo:
            continue

        cursor.execute(
            """
            SELECT
                pais,
                zona,
                criterio_zona,
                codigo,
                localidade,
                servico,
                is_active
            FROM dbo.zonas_geograficas
            WHERE ref_zona_geo = ?
            """,
            ref_zona_geo
        )

        row = cursor.fetchone()

        valores_excel = (
            registo["pais"],
            registo["zona"],
            registo["criterio_zona"],
            registo["codigo"],
            registo["localidade"],
            registo["servico"],
            registo["is_active"],
        )

        if row:
            valores_sql = tuple(row)

            houve_alteracao = any(
                valores_diferentes(
                    valor_sql,
                    valor_excel
                )
                for valor_sql, valor_excel
                in zip(
                    valores_sql,
                    valores_excel
                )
            )

            if houve_alteracao:
                cursor.execute(
                    """
                    UPDATE dbo.zonas_geograficas
                    SET
                        pais = ?,
                        zona = ?,
                        criterio_zona = ?,
                        codigo = ?,
                        localidade = ?,
                        servico = ?,
                        data_update = ?,
                        is_active = ?
                    WHERE ref_zona_geo = ?
                    """,
                    registo["pais"],
                    registo["zona"],
                    registo["criterio_zona"],
                    registo["codigo"],
                    registo["localidade"],
                    registo["servico"],
                    date.today(),
                    registo["is_active"],
                    ref_zona_geo
                )

                total_updates += 1

                print(
                    f"UPDATE zona -> "
                    f"{ref_zona_geo}"
                )

            else:
                total_sem_alteracao += 1

        else:
            cursor.execute(
                """
                INSERT INTO dbo.zonas_geograficas (
                    ref_zona_geo,
                    pais,
                    zona,
                    criterio_zona,
                    codigo,
                    localidade,
                    servico,
                    data_update,
                    is_active
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                ref_zona_geo,
                registo["pais"],
                registo["zona"],
                registo["criterio_zona"],
                registo["codigo"],
                registo["localidade"],
                registo["servico"],
                date.today(),
                registo["is_active"]
            )

            total_inserts += 1

            print(
                f"INSERT zona -> "
                f"{ref_zona_geo}"
            )

    return (
        total_inserts,
        total_updates,
        total_sem_alteracao
    )


def run():
    print("")
    print(
        "========================================"
    )
    print(" IMPORT PORTES INICIADO")
    print(
        "========================================"
    )
    print("")

    # ============================================
    # 0. CAMINHOS
    # ============================================

    paths = get_paths()

    env_path = paths["ENV_PATH"]

    excel_file = (
        paths["EXCEL_PORTES_ENVIO"]
    )

    print(
        f"Ficheiro .env: "
        f"{env_path}"
    )

    print(
        f"Ficheiro Excel: "
        f"{excel_file}"
    )

    # ============================================
    # 1. CONFIGURACAO SQL
    # ============================================

    db_config = load_db_config(
        env_path
    )

    # ============================================
    # 2. PROCESSAR EXCEL
    # ============================================

    (
        registos_portes,
        registos_zonas
    ) = processar_excel_portes(
        excel_file
    )

    print(
        f"Registos portes: "
        f"{len(registos_portes)}"
    )

    print(
        f"Registos zonas: "
        f"{len(registos_zonas)}"
    )

    # ============================================
    # 3. LIGACAO SQL
    # ============================================

    conn = conectar_banco(
        db_config
    )

    if conn is None:
        raise SystemExit(
            "Nao foi possivel "
            "conectar ao SQL."
        )

    cursor = conn.cursor()

    try:
        # ========================================
        # 4. IMPORTAR PORTES
        # ========================================

        (
            portes_inserts,
            portes_updates,
            portes_sem_alteracao
        ) = importar_portes(
            cursor,
            registos_portes
        )

        # ========================================
        # 5. IMPORTAR ZONAS
        # ========================================

        (
            zonas_inserts,
            zonas_updates,
            zonas_sem_alteracao
        ) = importar_zonas(
            cursor,
            registos_zonas
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

    print("")
    print(
        "========================================"
    )
    print(" IMPORTACAO CONCLUIDA")
    print(
        "========================================"
    )

    print("")
    print("PORTES")

    print(
        f"Total INSERTS: "
        f"{portes_inserts}"
    )

    print(
        f"Total UPDATES: "
        f"{portes_updates}"
    )

    print(
        f"Sem alteracao: "
        f"{portes_sem_alteracao}"
    )

    print("")
    print("ZONAS")

    print(
        f"Total INSERTS: "
        f"{zonas_inserts}"
    )

    print(
        f"Total UPDATES: "
        f"{zonas_updates}"
    )

    print(
        f"Sem alteracao: "
        f"{zonas_sem_alteracao}"
    )

    print("")
    print(
        "========================================"
    )


if __name__ == "__main__":
    run()