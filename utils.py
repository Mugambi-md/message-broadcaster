from backend import InputReader


class ImportController:
    def __init__(self, db):
        self.db = db

    def import_contacts(self, file_path, name, contact, loc_col=None, manual_loc=None):
        reader = InputReader(file_path)
        data = reader.extract_data(name, contact, loc_col, manual_loc)
        return reader.insert_into_db(self.db, data)