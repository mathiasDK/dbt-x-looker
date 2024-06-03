
class dbtLookerExposure:
    def __init__(self, looker_path:str):
        self.looker_path = looker_path

    @property
    def update_looker_path(self, looker_path)->None:
        self.looker_path = looker_path

    def _get_exposure_files(self)->list:
        pass

    def _get_view_files(self)->list:
        pass

    def get_exposure_tables(self, exposure_name:str)->list:
        pass

    def get_table_columns(self, table_name:str)->list:
        pass

    def create_exposure_doc(self, exposure_name:str)->str:
        pass

    def create_all_exposures_docs(self)->str:
        pass

    def update_exposure_doc(self, yml_content)->str:
        pass
