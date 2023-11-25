# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Sabrina Fechtner, 11/24/2023, Imported A06 and Modified for A07
# ------------------------------------------------------------------------------------------ #
import json
from typing import TextIO, List

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
Select from the following menu:  
1. Register a Student for a Course.
2. Show current data.  
3. Save data to a file.
4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
FILE_NAME: str = "Enrollments.json"


# Define Classes
class Person:
    def __init__(self, first_name: str, last_name: str) -> None:
        self._first_name = first_name
        self._last_name = last_name

    @property
    def first_name(self) -> str:
        return self._first_name.capitalize()

    @first_name.setter
    def first_name(self, value):
        if value.isalpha():
            self._first_name = value
        else:
            raise ValueError("The first name cannot be alphanumeric. Please re-enter the first name.")

    @property
    def last_name(self) -> str:
        return self._last_name.capitalize()

    @last_name.setter
    def last_name(self, value):
        if value.isalpha():
            self._last_name = value
        else:
            raise ValueError("The last name cannot be alphanumeric. Please re-enter the last name.")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Student(Person):
    def __init__(self, student_first_name: str, student_last_name: str, course_name: str) -> None:
        super().__init__(first_name=student_first_name, last_name=student_last_name)
        self.course_name = course_name

    @property
    def student_course_name(self) -> str:
        return self.course_name.capitalize()

    @student_course_name.setter
    def student_course_name(self, value):
        self.course_name = str(value)

    def __str__(self) -> str:
        return f"{super().__str__()} has been registered for {self.student_course_name}"


# Define the Data Variables
students: list[Student] = []
menu_choice: str


# File Processing Functions
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    Sabrina Fechtner 11.24.2023 Incorporated Class into A07
    """

    @staticmethod
    def read_data_from_file(file_name: str) -> list[Student]:
        """ This function reads previous JSON file with student and course data

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function
        Sabrina Fechtner, 11.16.2023, Incorporated Function

        :param: file_name: string data with name of file to read from
        :return: Student Data as list
        """
        file: TextIO = None
        json_data = []
        students: list[Student] = []
        try:
            file = open(file_name, "r")
            json_data = json.load(file)
            print("Data successfully loaded from the file.")
        except FileNotFoundError:
            print("File not found, creating it...")
            with open(file_name, "w") as file:
                json.dump(json_data, file)
                print("File created successfully.")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON file: {e}. Resetting it...")
            with open(file_name, "w") as file:
                json.dump(json_data, file)
                print("File reset successfully.")
        except Exception as e:
            print(f"An unexpected error occurred while loading data: {e}")

        for row in json_data:
            student = Student(row["student_first_name"], row["student_last_name"], row["course_name"])
            students.append(student)

        return students

    @staticmethod
    def write_data_to_file(roster: list[Student], file_name: str) -> list[Student]:
        """ This function writes student and course data to JSON file

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function
        Sabrina Fechtner, 11.16.2023, Incorporated Function
        Sabrina Fechtner, 11.24.2023, Pulled into A07
        :param: file name = JSON file and roster = student data
        :return: None
        """
        file: TextIO = None
        try:
            json_data: list[dict[str, str, str]] = []
            for student in roster:
                json_data.append({
                    "student_first_name": student.first_name,
                    "student_last_name": student.last_name,
                    "course_name": student.student_course_name
                }
                )
            with open(file_name, "w") as file:
                json.dump(json_data, file)
                print("Data successfully written to the file.")
        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid JSON format", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return roster


# Present and Process the data
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.4.2030,Added a function to display custom error messages
    Sabrina Fechtner 11.17.23, Incorporated in A06
    Sabrina Fechtner 11.24.23, Pulled into A07
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays error messages to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function
        Sabrina Fechtner, 11.16.2023, Incorporated into A06
        Sabrina Fechter, 11.24.2023, Pulled into A07
        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print(f"An unexpected error occurred: {error}")

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function
        Sabrina Fechtner, 11.16.2023, Incorporated into A06

        :return: None
        """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """ This function incorporates user choice from menu

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function
        Sabrina Fechtner, 11.16.2023, Incorporated into A06

        :return: User Choice
            """
        choice = "0"
        try:
            choice = input("What would you like to do?: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Only Enter 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice

    @staticmethod
    def output_student_courses(student_data: list[Student]):
        """ This function shows the first name, last name, and course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function
        Sabrina Fechtner, 11.16.2023, Incorporated into A06

        :return: None
        """
        print("\nThe current data is:")
        for student in student_data:
            student_first_name = student.first_name
            student_last_name = student.last_name
            student_course_name = student.course_name
            print(student_first_name, student_last_name, student_course_name)

    @staticmethod
    def input_student_data(student_data: List[Student]) -> List[Student]:
        """
        This function incorporates user choice from the menu

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function
        Sabrina Fechtner, 11.16.2023, Incorporated into A06

        :return: None
        """
        while True:
            # Create an instance of Student with valid initial values
            student = Student("", "", "")

            student_first_name: str = input("Please enter first name: ")
            student_last_name: str = input("Please enter last name: ")
            student_course_name: str = input("Please enter the course name: ")

            try:
                # Set the properties individually
                student.first_name = student_first_name
                student.last_name = student_last_name
                student.student_course_name = student_course_name

                # Create a new instance with validated properties
                student = Student(student.first_name, student.last_name, student.student_course_name)
                student_data.append(student)

                print(
                    f"You have registered {student.first_name} {student.last_name} for {student.student_course_name}.")
                break  # exit the loop if registration is successful
            except ValueError as e:
                IO.output_error_messages(f"Error registering student: {e}")

        return student_data


# Main Program:

students: list[Student] = FileProcessor.read_data_from_file(file_name=FILE_NAME)

while True:
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":  # get student input
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":  # Present data
        IO.output_student_courses(student_data=students)
        continue

    elif menu_choice == "3":  # Save data in a file
        FileProcessor.write_data_to_file(file_name=FILE_NAME, roster=students)
        continue

    elif menu_choice == "4":  # End the program
        break  # out of the while loop
