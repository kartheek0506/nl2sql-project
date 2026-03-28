def validate_sql(sql: str):
    if not sql:
        return False, "Empty SQL"

    sql = sql.lower()

    banned = ["insert", "update", "delete", "drop", "alter", "exec"]

    for word in banned:
        if word in sql:
            return False, "Only SELECT queries allowed"

    if "sqlite_master" in sql:
        return False, "System tables access not allowed"

    return True, "Valid"