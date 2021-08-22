from urllib.parse import quote

data_source_dict = {
    "mysql": {
        "db_id": "id",
        "password": "password",
        "host": "localhost",
        "port": "3306",
    },
}


def make_data_source(db_type, db_name):
    """
    Args:
        db_type(str): 사용할 db서버
                        ex)
                        CPU : cpu server mariadb
                        AWS_TEST : aws test mariadb
                        AWS_PROD : aws production mariadb
        db_name(str): 사용할 db이름
    Returns:
        str: data_source
    """

    db_id = data_source_dict[db_type]["db_id"]
    password = data_source_dict[db_type]["password"]
    host = data_source_dict[db_type]["host"]
    port = data_source_dict[db_type]["port"]
    data_source = "mysql+pymysql://" + db_id + ":" + quote(password) + "@" + host + ":" + port + "/" + db_name
    return data_source
