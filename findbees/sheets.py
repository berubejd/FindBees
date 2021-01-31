from datetime import date, timedelta
from typing import Optional, Tuple
import gspread
import random


class Worksheet:
    def __init__(
        self, sheet_name: str, secrets_file: str = "service_account.json"
    ) -> None:
        # Setup auth for Sheets
        self.gc = gspread.service_account(secrets_file)

        # Open a sheet and read in records
        self.sheet = self.gc.open(sheet_name).sheet1

        self.refresh()
        # self.cells: list[dict] = self.sheet.get_all_records()

    def refresh(self) -> bool:
        try:
            # Pull contents of sheet
            self.cells = self.sheet.get_all_records()

            # Pull out useful fields
            self.headers: list = self.sheet.row_values(1)
            self.names: list[str] = [cell["Name"] for cell in self.cells]

            return True
        except:
            return False

    def find_row_by_name(self, name: str) -> Optional[dict]:
        for cell in self.cells:
            if cell["Name"] == name:
                return cell

        return None

    def find_name(self, name: str) -> Optional[int]:
        try:
            return self.names.index(name) + 2
        except:
            return None

    def find_column(self, value: str) -> Optional[int]:
        try:
            return self.headers.index(value) + 1
        except:
            return None

    def update_cell(self, name: str, column: str, value: str) -> bool:
        row_index = self.find_name(name)
        column_index = self.find_column(column)

        if row_index == None or column_index == None:
            return False

        self.sheet.update_cell(row_index, column_index, value)
        self.refresh()

        return True

    def add_header(self, value: str) -> bool:
        if not self.find_column(value):
            self.sheet.add_cols(1)
            self.sheet.update_cell(1, len(self.headers) + 1, value)
            self.refresh()

        return True


def calculate_dates() -> Tuple[str, str]:
    # Setup required dates
    today: date = date.today()
    monday_current: date = today - timedelta(days=today.weekday())
    monday_last: date = monday_current - timedelta(weeks=1)

    return str(monday_current), str(monday_last)


def get_or_assign_pick(worksheet: Worksheet, name: str) -> Optional[str]:
    # Ensure the worksheet is in sync with the Google Sheet
    worksheet.refresh()
    
    # Request dates
    monday_current, monday_last = calculate_dates()

    # Ensure current week is in headers
    if not monday_current in worksheet.headers:
        worksheet.add_header(monday_current)

    # Get user information
    user_row = worksheet.find_row_by_name(name)
    if not user_row:
        return None

    # If assigned already exists then return it directly
    if not user_row.get(monday_current) == "":
        return user_row[monday_current]

    saved_assignments: list[str] = [cell[monday_current] for cell in worksheet.cells]
    retry_count: int = 0

    while True:
        if retry_count > 3:
            print("Exceeded allowable failure count.")
            return None

        new_assignments = []

        try:
            for index, cell in enumerate(worksheet.cells):
                if saved_assignments[index] == "":
                    # Choose new name to assign
                    excludes: list[str] = [cell["Name"]]

                    if not cell.get(monday_last) == "":
                        excludes.append(cell[monday_last])

                    all_assigned = saved_assignments + new_assignments
                    assigned = {entry for entry in all_assigned if not entry == ""}
                    assigned.update(excludes)

                    new_name: str = random.choice(
                        [name for name in worksheet.names if name not in assigned]
                    )
                else:
                    new_name: str = saved_assignments[index]

                new_assignments.append(new_name)

            break
        except:
            print("Failed... Retrying.")
            retry_count += 1

    # Find target cell and update worksheet
    for index, name_t in enumerate(worksheet.names):
        if saved_assignments[index] == "":
            worksheet.update_cell(name_t, monday_current, new_assignments[index])

    # return new name
    return new_assignments[worksheet.names.index(name)]


# def get_or_assign_pick(worksheet: Worksheet, name: str) -> Optional[str]:
#     # Request dates
#     monday_current, monday_last = calculate_dates()

#     # Ensure current week is in headers
#     if not monday_current in worksheet.headers:
#         worksheet.add_header(monday_current)

#     # Get user information
#     user_row = worksheet.find_row_by_name(name)
#     if not user_row:
#         return None

#     # If assigned already exists then return it directly
#     if not user_row.get(monday_current) == "":
#         return user_row[monday_current]

#     # Choose new name to assign
#     excludes = [name]

#     if not user_row.get(monday_last) == "":
#         excludes.append(user_row[monday_last])

#     assigned = {
#         cell[monday_current]
#         for cell in worksheet.cells
#         if not cell[monday_current] == ""
#     }
#     assigned.update(excludes)

#     new_name: str = random.choice(
#         [name for name in worksheet.names if name not in assigned]
#     )

#     # Find target cell and update worksheet
#     worksheet.update_cell(name, monday_current, new_name)

#     return new_name


def main() -> None:
    worksheet = Worksheet("The Hat")

    print(get_or_assign_pick(worksheet, "Todd"))

    for cell in worksheet.cells:
        name = cell["Name"]

        print(f"{name}: {get_or_assign_pick(worksheet, name)}")


if __name__ == "__main__":
    main()