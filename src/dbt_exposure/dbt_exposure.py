import os
import re
from sql_metadata import Parser

class LookerContentExtractor:
    def __init__(self, looker_path:str):
        self._looker_path = looker_path
        self.exposure_to_tables = None
        self.table_name_mapping = None
        self.table_sql_lookup = None
        self.view_to_sql_columns = None
        self.view_to_sql_tables = None

    @property
    def looker_path(self)->None:
        return self._looker_path

    @looker_path.setter
    def looker_path(self, looker_path:str)->None:
        self._looker_path = looker_path

    @staticmethod
    def __find_files(directory, extension):
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
    
    @staticmethod
    def __read_and_split_file(file_path:str, keyword:str)->str:
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
    
    @staticmethod
    def _get_all_matches(s:str, pattern:str):
        matches = re.findall(pattern, s)

        if matches:
            return matches
        
    def get_all_exposure_tables(self)->dict:
        exposure_files = self._get_exposure_files()
        exposure_to_tables = {}
        for file in exposure_files:
            segments = self.__read_and_split_file(file, "explore:")
            for segment in segments:
                tables = []
                s = segment.strip()
                explore_name = re.search(r'\b\w+\b', s).group(0)
                
                # Main view
                pattern = r'\bfrom:\s*(\w+)'
                # Use a regular expression to find the first match
                match = self._get_all_matches(s, pattern)
                if match:
                    tables.append(match[0])

                # additional views
                pattern = r'\bjoin:\s*(\w+)'
                # Use a regular expression to find the first match
                match = self._get_all_matches(s, pattern)
                if match:
                    for m in match:
                        tables.append(m)
                if tables != []:
                    exposure_to_tables[explore_name] = tables
        self.exposure_to_tables = exposure_to_tables
        return exposure_to_tables

    def get_exposure_tables(self, exposure_name:str)->list:
        if self.exposure_to_tables is None:
            self.get_all_exposure_tables()
        
        return self.exposure_to_tables.get(exposure_name)

    def _extract_table_sql_columns(self, table_content:str)->list:
        columns = []
        pattern = r'\$\{TABLE\}.(\w+)'
        # Use a regular expression to find the first match
        match = self._get_all_matches(table_content, pattern)
        if match:
            for m in match:
                columns.append(m)
        columns = list(sorted(set(columns))) # making it unique
        return columns

    def _extract_sql_tables(self, content:str)->list:
        if "derived_table" in content:
            pattern = re.compile(f'{re.escape(r"sql:")}(.*?){re.escape(r";;")}', re.DOTALL)
            query = pattern.search(content).group(1)
            sql_table_names = Parser(query).tables
        else:
            pattern = r"sql_table_name:\s*(\S+)"
            match = self._get_all_matches(content, pattern)
            if match:
                sql_table_names = [match[0]]
        return sql_table_names

    def create_table_sql_lookup(self)->dict:
        view_to_sql_columns = {}
        view_to_sql_tables = {}
        for file_path in self._get_view_files():
            with open(file_path, 'r') as file:
                content = file.read()
                view_name = self._get_all_matches(content, r'\bview:\s*(\w+)')
                sql_tables = self._extract_sql_tables(content=content)
                sql_columns = self._extract_table_sql_columns(content)
                view_to_sql_columns[view_name] = sql_columns
                view_to_sql_tables[view_name] = sql_tables
        self.view_to_sql_columns = view_to_sql_columns
        self.view_to_sql_tables = view_to_sql_tables

    def get_view_sql_columns(self, view_name:str)->list:
        if self.table_sql_lookup is None:
            self.create_table_sql_lookup()
        
        return self.view_to_sql_columns.get(view_name)
