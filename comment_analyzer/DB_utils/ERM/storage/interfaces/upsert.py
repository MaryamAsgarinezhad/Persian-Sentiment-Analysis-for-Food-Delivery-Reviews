from sqlalchemy.orm import Session
from ....ERM.config.db import engine



class UpsertInterface:
    """Docstring for UpsertInterface."""

    def __init__(self):
        self.session = self.__get_session()

    def __get_session(self):
        with Session(engine) as session:
            return session

    def clos(self):
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def write(self, items):
        """
        Insert item into corresponding db table if not exist. Update item if id is provided and found in table.
        :items: List of valid db models objects.
        """
        try:
            for el in items:
                self.session.merge(el)
            self.session.commit()
            return {'status': True}
        except Exception as error:
            print(f"[X] Postgres Error: {error}")
            self.rollback()
            self.clos()
            return {'status': False, 'message': error}

    def delete(self, table, key, id_):
        pass
