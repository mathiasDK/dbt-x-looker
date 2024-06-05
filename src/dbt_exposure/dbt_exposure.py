
class dbtLookerExposure:
    def __init__(self, looker_path:str, dbt_path:str):
        self._looker_path = looker_path
        self._dbt_path = dbt_path

    @property
    def looker_path(self)->None:
        return self._looker_path

    @looker_path.setter
    def looker_path(self, looker_path:str)->None:
        self._looker_path = looker_path

    @property
    def dbt_path(self)->None:
        return self._dbt_path

    @dbt_path.setter
    def update_dbt_path(self, dbt_path:str)->None:
        self._dbt_path = dbt_path

    def _get_exposure_files(self)->list:
        pass

    def _get_view_files(self)->list:
        pass

    def get_exposure_tables(self, exposure_name:str)->list:
        pass

    def get_table_columns(self, table_name:str)->list:
        pass

    def get_table_sql_columns(self, table_name:str)->list:
        pass

    def create_exposure_doc(self, exposure_name:str)->str:
        pass

    def create_all_exposures_docs(self)->str:
        pass

    def update_exposure_doc(self, yml_content)->str:
        pass
