from pathlib import Path
import pandas as pd
import re


class InputReader:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self._df = None

    def read_file(self):
        """Read file once and cache it."""
        if self._df is not None:
            return self._df

        if self.file_path.suffix == ".csv":
            self._df = pd.read_csv(self.file_path)
        elif self.file_path.suffix in [".xlsx", ".xls"]:
            self._df = pd.read_excel(self.file_path)
        else:
            raise ValueError("Unsupported file format")
        # Normalize column names (important)
        self._df.columns = [col.strip().lower() for col in self._df.columns]

        return self._df

    def get_columns(self):
        """Return available column name."""
        df = self.read_file()
        return list(df.columns)

    def extract_data(self, name_col, contact_col, location_col=None, manual_loc=None):
        """
        Extract Selected columns and return clean list of dictionaries.
        :param manual_loc: Location that is not in sheet columns
        :param name_col: contact name
        :param contact_col: phone number
        :param location_col: location of the contact
        :return: list
        """
        df = self.read_file()

        # validate columns
        required = [name_col, contact_col]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not Found")

        columns = [name_col, contact_col]
        if location_col and location_col in df.columns:
            columns.append(location_col)

        df = df[columns].copy()

        # Rename columns to match DB
        rename_map = {
            name_col: "name",
            contact_col: "contact"
        }
        if location_col and location_col in df.columns:
            rename_map[location_col] = "location"

        df.rename(columns=rename_map, inplace=True)

        # Clean data
        df["name"] = df["name"].astype(str).str.strip()
        df["contact"] = df["contact"].apply(self.normalize_phone)

        if "location" in df.columns:
            df["location"] = df["location"].astype(str).str.strip()
        elif manual_loc:
            df["location"] = [str(manual_loc).strip()] * len(df)
        else:
            df["location"] = None

        df = df.dropna(subset=["contact"])

        # Remove duplicates (important before DB)
        df = df.drop_duplicates(subset=["contact"])

        # Convert to list of dictionaries
        return df.to_dict(orient="records")

    @staticmethod
    def insert_into_db(db, data):
        """
        Insert extracted data into database.
        :param db: Database instance
        :param data: list of dictionaries
        :return:
        """
        if not data:
            return 0
        query = """
            INSERT OR IGNORE INTO contacts (name, contact, location)
            VALUES (?, ?, ?)
        """
        values = [
            (
                item.get("name"),
                item.get("contact"),
                item.get("location")
            )
            for item in data
        ]
        before = db.execute(
            "SELECT COUNT(*) FROM contacts", commit=False
        ).fetchone()[0]

        db.executemany(query, values)

        after = db.execute(
            "SELECT COUNT(*) FROM contacts", commit=False
        ).fetchone()[0]
        return after - before

    @staticmethod
    def normalize_phone(phone):
        """Normalize Kenyan phone numbers ro 254xxxxxxxxx format."""
        if not phone:
            return None
        phone = str(phone).strip()

        # Remove spaces and common symbols
        phone = re.sub(r"\D", "", phone)

        # Remove leading +
        if phone.startswith("+"):
            phone = phone[1:]
        # Case 1: starts with 0 replace with 254
        if phone.startswith("0") and len(phone) == 10:
            phone = "254" + phone[1:]
        # Case 2: starts with 7 or 1, add 254
        elif (phone.startswith("7") or phone.startswith("1")) and len(phone) == 9:
            phone = "254" + phone
        # Case 3: already correct
        elif phone.startswith("254") and len(phone) == 12:
            pass
        else:
            return None # Invalid number
        return phone
