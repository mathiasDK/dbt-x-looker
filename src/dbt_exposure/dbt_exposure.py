import os
import re

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

    def __find_files(self, directory, extension):
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(extension):
                    matches.append(os.path.join(root, filename))
        return matches

    def _get_exposure_files(self)->list:
        extension = "model.lkml"
        files = self.__find_files(directory=self.looker_path, extension=extension)
        return files

    def _get_view_files(self)->list:
        extension = "view.lkml"
        files = self.__find_files(directory=self.looker_path, extension=extension)
        return files
    
    def __read_and_split_file(self, file_path:str, keyword:str)->str:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                segments = content.split(keyword)
                return segments
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_all_exposure_tables(self)->dict:
        exposure_files = self._get_exposure_files()
        exposure_dict = {}
        for file in exposure_files:
            segments = self.__read_and_split_file(file, "explore:")
            for segment in segments:
                tables = []
                s = segment.strip()
                explore_name = re.search(r'\b\w+\b', s).group(0)
                
                # Main view
                pattern = r'\bfrom:\s*(\w+)'
                # Use a regular expression to find the first match
                match = re.search(pattern, s)
                if match:
                    tables.append(match.group(1))

                # # additional views
                # pattern = r'\bjoin:\s*(\w+)'
                # # Use a regular expression to find the first match
                # match = re.search(pattern, s)
                # if match:
                #     print(match)
                exposure_dict[explore_name] = tables
        return exposure_dict       

    def get_exposure_tables(self, exposure_name:str)->list:
        exposure_files = self._get_exposure_files()
        for file in exposure_files:
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
