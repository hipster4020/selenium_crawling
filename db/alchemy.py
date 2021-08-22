import pandas as pd
import sqlalchemy
from config import make_data_source


class DataSource:
    def __init__(self, db_type: str, db_name: str):
        """
        database_uri 생성 및 sqlalchemy engine 생성
        Args:
            db_type(str): 사용할 데이터베이스 서버
            db_name(str): 사용할 데이터베이스 이름

        """
        self.table_dict = {}
        self.database_uri = make_data_source(db_type, db_name)
        self.engine = sqlalchemy.create_engine(self.database_uri, pool_pre_ping=True)
        # pool_pre_ping : testing of connections upon checkout is achievable by using the Pool.pre_ping argument

    def __enter__(self):
        return self.engine.begin()

    def __exit__(self):
        if self.engine:
            self.engine.dispose()

    def __del__(self):
        if self.engine:
            self.engine.dispose()

    def df_to_sql(self, df: pd.DataFrame, table_name: str):
        """
        Args:
            df(DataFrame): 데이터베이스에 저장할 데이터프레임 객체
            table_name(str): 테이블 이름
        """

        df.to_sql(table_name, con=self.engine, if_exists="append", index=False)

    def execute_query(self, query: str):
        """
        단순히 query 실행
        Args:
            query(str): 실행할 쿼리
        """

        try:
            with self.engine.begin() as con:
                result = con.execute(query)
                return result
        except Exception as e:
            print(e)

    def execute_query_to_df(self, query: str):
        """
        쿼리 결과를 데이터프레임 형태로 반환
        Args:
            query(str): 실행할 쿼리
        """

        row_list = []
        try:
            with self.engine.begin() as con:
                result = con.execute(query)
                for row in result:
                    row_list.append(dict(row))
        except Exception as e:
            print(e)
        return pd.DataFrame(row_list)
