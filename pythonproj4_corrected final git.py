import csv
import json
import os

FILE = "students.json"
LEGACY_FILE = "students.csv"


def load_students():
    """Load all student records, including marks, attendance, clubs, fees and events."""
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        students = {}

        # Import basic records from the old CSV file once, if one exists.
        if os.path.exists(LEGACY_FILE) and os.path.getsize(LEGACY_FILE) > 0:
            try:
                with open(LEGACY_FILE, "r", newline="", encoding="utf-8") as fh:
                    reader = csv.DictReader(fh)
                    for row in reader:
                        roll = (row.get("roll") or "").strip()
                        if not roll:
                            continue
                        try:
                            year = int(row.get("year", ""))
                        except (TypeError, ValueError):
                            year = 1
                        students[roll] = {
                            "name": row.get("name", ""),
                            "branch": row.get("branch", ""),
                            "year": year
                        }
            except (OSError, csv.Error):
                print("Warning: Could not read the old students.csv file.")

        save_students(students)
        return students

    try:
        with open(FILE, "r", encoding="utf-8") as fh:
            students = json.load(fh)
        if not isinstance(students, dict):
            raise ValueError("Student data must be a dictionary.")
        return students
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Error reading student data: {error}")
        return {}


def save_students(students):
    """Save the complete student records to JSON."""
    with open(FILE, "w", encoding="utf-8") as fh:
        json.dump(students, fh, indent=4)


while True:
    print("\nCOLLEGE STUDENT MANAGEMENT")
    print("1. Student Management")
    print("2. Academic Management")
    print("3. Attendance Management")
    print("4. Club Management")
    print("5. Fees and Events")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        while True:
            print("\nSTUDENT MANAGEMENT")
            print("1. Add Student")
            print("2. Search Student")
            print("3. Display All Students")
            print("4. Delete Student")
            print("5. Update Student")
            print("6. Search by Branch")
            print("7. Back to Main Menu")

            student_choice = input("Enter choice: ")
            students = load_students()

            if student_choice == "1":
                roll = input("Enter roll number: ")

                if roll in students:
                    print("Student already exists.")
                else:
                    name = input("Enter student name: ")
                    branch = input("Enter branch: ")
                    try:
                        year = int(input("Enter year: "))
                        if year < 1:
                            print("Year must be a positive whole number.")
                            continue
                    except ValueError:
                        print("Please enter a valid whole number for the year.")
                        continue

                    students[roll] = {
                        "name": name,
                        "branch": branch,
                        "year": year
                    }

                    save_students(students)
                    print("Student added successfully.")

            elif student_choice == "2":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                else:
                    print("Roll Number:", roll)
                    print("Name:", students[roll]["name"])
                    print("Branch:", students[roll]["branch"])
                    print("Year:", students[roll]["year"])

            elif student_choice == "3":
                if not students:
                    print("No students registered.")
                else:
                    for roll, data in students.items():
                        print("\nRoll Number:", roll)
                        print("Name:", data["name"])
                        print("Branch:", data["branch"])
                        print("Year:", data["year"])

            elif student_choice == "4":
                roll = input("Enter roll number: ")

                if roll in students:
                    del students[roll]
                    save_students(students)
                    print("Student deleted successfully.")
                else:
                    print("Student not found.")

            elif student_choice == "5":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                else:
                    print("1. Change Name")
                    print("2. Change Branch")
                    print("3. Change Year")

                    update_choice = input("Enter choice: ")

                    if update_choice == "1":
                        students[roll]["name"] = input("Enter new name: ")
                        print("Name updated successfully.")

                    elif update_choice == "2":
                        students[roll]["branch"] = input(
                            "Enter new branch: "
                        )
                        print("Branch updated successfully.")

                    elif update_choice == "3":
                        try:
                            students[roll]["year"] = int(
                                input("Enter new year: ")
                            )
                            print("Year updated successfully.")
                        except ValueError:
                            print("Enter a valid year.")
                            continue

                    else:
                        print("Invalid choice.")
                        continue

                    save_students(students)

            elif student_choice == "6":
                branch = input("Enter branch: ")
                found = False

                for roll, data in students.items():
                    if data["branch"].lower() == branch.lower():
                        print(roll, "-", data["name"])
                        found = True

                if not found:
                    print("No students found in this branch.")

            elif student_choice == "7":
                print("Returning to Main Menu.")
                break

            else:
                print("Invalid choice.")

    elif choice == "2":
        while True:
            print("\nACADEMIC MANAGEMENT")
            print("1. Enter Marks")
            print("2. Display Marks")
            print("3. Calculate Percentage")
            print("4. Grade")
            print("5. Failed Subjects")
            print("6. Find Topper")
            print("7. Back to Main Menu")

            academic_choice = input("Enter choice: ")
            students = load_students()

            if academic_choice == "1":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                    continue

                subjects = [
                    "Python",
                    "Mathematics",
                    "Physics",
                    "English"
                ]
                marks = {}
                valid_marks = True

                for subject in subjects:
                    try:
                        score = float(
                            input(f"Enter {subject} marks (0-100): ")
                        )

                        if not 0 <= score <= 100:
                            print("Marks must be between 0 and 100.")
                            valid_marks = False
                            break

                        marks[subject] = score

                    except ValueError:
                        print("Please enter valid numeric marks.")
                        valid_marks = False
                        break

                if valid_marks:
                    students[roll]["marks"] = marks
                    save_students(students)
                    print("Marks entered successfully.")

            elif academic_choice in ("2", "3", "4", "5"):
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                    continue

                marks = students[roll].get("marks", {})

                if not marks:
                    print("Marks have not been entered.")
                    continue

                if academic_choice == "2":
                    print("\n===== MARKS =====")
                    for subject, score in marks.items():
                        print(f"{subject}: {score}")

                elif academic_choice == "3":
                    total = sum(marks.values())
                    percentage = total / len(marks)
                    print(f"Percentage: {percentage:.2f}%")

                elif academic_choice == "4":
                    total = sum(marks.values())
                    percentage = total / len(marks)

                    if percentage >= 90:
                        grade = "A+"
                    elif percentage >= 80:
                        grade = "A"
                    elif percentage >= 70:
                        grade = "B"
                    elif percentage >= 60:
                        grade = "C"
                    elif percentage >= 50:
                        grade = "D"
                    else:
                        grade = "F"

                    print(f"Percentage: {percentage:.2f}%")
                    print(f"Grade: {grade}")

                elif academic_choice == "5":
                    failed = [
                        subject
                        for subject, score in marks.items()
                        if score < 40
                    ]

                    if failed:
                        for subject in failed:
                            print(f"{subject} - FAILED")
                    else:
                        print("No failed subjects.")

            elif academic_choice == "6":
                highest = -1
                topper = None

                for roll, data in students.items():
                    marks = data.get("marks", {})

                    if marks:
                        percentage = sum(marks.values()) / len(marks)

                        if percentage > highest:
                            highest = percentage
                            topper = roll

                if topper is not None:
                    print("Topper:", students[topper]["name"])
                    print("Roll Number:", topper)
                    print(f"Percentage: {highest:.2f}%")
                else:
                    print("No marks available.")

            elif academic_choice == "7":
                print("Returning to Main Menu.")
                break

            else:
                print("Invalid choice.")

    elif choice == "3":
        while True:
            print("\n===== ATTENDANCE MANAGEMENT =====")
            print("1. Enter Attendance")
            print("2. View Attendance")
            print("3. Check Exam Eligibility")
            print("4. Find Low-Attendance Students")
            print("5. Back to Main Menu")

            attendance_choice = input("Enter choice: ")
            students = load_students()

            if attendance_choice == "1":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                    continue

                subjects = [
                    "Python",
                    "Mathematics",
                    "Physics",
                    "English"
                ]

                attendance = {}
                valid = True

                for subject in subjects:
                    try:
                        attended = int(
                            input(f"Classes attended in {subject}: ")
                        )
                        total = int(
                            input(f"Total classes in {subject}: ")
                        )

                        if (
                            total < 0
                            or attended < 0
                            or attended > total
                        ):
                            print("Invalid attendance details.")
                            valid = False
                            break

                        attendance[subject] = [attended, total]

                    except ValueError:
                        print("Please enter valid whole numbers.")
                        valid = False
                        break

                if valid:
                    students[roll]["attendance"] = attendance
                    save_students(students)
                    print("Attendance recorded successfully.")

            elif attendance_choice == "2":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                    continue

                attendance = students[roll].get("attendance", {})

                if not attendance:
                    print("Attendance has not been entered.")
                    continue

                print("\n===== ATTENDANCE =====")
                print("Student:", students[roll]["name"])
                print("Roll Number:", roll)

                for subject, values in attendance.items():
                    attended, total = values
                    percentage = (
                        attended / total * 100 if total > 0 else 0
                    )

                    print(
                        f"{subject}: {attended}/{total} classes "
                        f"- {percentage:.2f}%"
                    )

            elif attendance_choice == "3":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                    continue

                attendance = students[roll].get("attendance", {})

                if not attendance:
                    print("Attendance has not been entered.")
                    continue

                eligible = True

                for subject, values in attendance.items():
                    attended, total = values
                    percentage = (
                        attended / total * 100 if total > 0 else 0
                    )

                    if percentage < 75:
                        print(
                            f"{subject}: Below 75% "
                            f"({percentage:.2f}%)"
                        )
                        eligible = False

                if eligible:
                    print("Student is eligible for examination.")
                else:
                    print("Student is NOT eligible for examination.")

            elif attendance_choice == "4":
                found = False

                for roll, data in students.items():
                    attendance = data.get("attendance", {})

                    for subject, values in attendance.items():
                        attended, total = values

                        if total > 0:
                            percentage = attended / total * 100

                            if percentage < 75:
                                print(
                                    f"{data['name']} - {roll} - "
                                    f"{subject} - {percentage:.2f}%"
                                )
                                found = True

                if not found:
                    print("No low-attendance students found.")

            elif attendance_choice == "5":
                print("Returning to Main Menu.")
                break

            else:
                print("Invalid choice. Please try again.")

    elif choice == "4":
        while True:
            print("\n===== CLUB MANAGEMENT =====")
            print("1. Join Club")
            print("2. Display Clubs")
            print("3. Back to Main Menu")

            club_choice = input("Enter choice: ")
            students = load_students()

            if club_choice == "1":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                else:
                    clubs = {
                        "1": "Coding Club",
                        "2": "Robotics Club",
                        "3": "Music Club",
                        "4": "Sports Club",
                        "5": "Literary Club"
                    }

                    print("\n===== AVAILABLE CLUBS =====")
                    for number, club in clubs.items():
                        print(number, "-", club)

                    selected_club = input("Enter club choice: ")

                    if selected_club in clubs:
                        if "clubs" not in students[roll]:
                            students[roll]["clubs"] = []

                        club_name = clubs[selected_club]

                        if club_name in students[roll]["clubs"]:
                            print(
                                "Student has already joined this club."
                            )
                        else:
                            students[roll]["clubs"].append(club_name)
                            save_students(students)
                            print("Club added successfully.")
                    else:
                        print("Invalid club choice.")

            elif club_choice == "2":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                else:
                    joined_clubs = students[roll].get("clubs", [])

                    if not joined_clubs:
                        print("No clubs joined.")
                    else:
                        print("\n===== JOINED CLUBS =====")
                        print("Student:", students[roll]["name"])

                        for club in joined_clubs:
                            print("-", club)

            elif club_choice == "3":
                print("Returning to Main Menu.")
                break

            else:
                print("Invalid choice. Please try again.")

    
    elif choice == "5":
        while True:
            print("\n===== FEES AND EVENTS =====")
            print("1. Pay Fees")
            print("2. Display Fees")
            print("3. Register for Event")
            print("4. Back to Main Menu")

            fees_event_choice = input("Enter choice: ")
            students = load_students()

            if fees_event_choice == "1":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                else:
                    try:
                        amount = float(input("Enter amount to pay: "))

                        if amount > 0:
                            fees_paid = students[roll].get(
                                "fees_paid", 0.0
                            )
                            students[roll]["fees_paid"] = (
                                fees_paid + amount
                            )

                            save_students(students)
                            print("Payment successful.")
                            print(
                                "Total fees paid:",
                                students[roll]["fees_paid"]
                            )
                        else:
                            print("Invalid amount.")

                    except ValueError:
                        print("Please enter a valid amount.")

            elif fees_event_choice == "2":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                else:
                    fees_paid = students[roll].get("fees_paid", 0.0)
                    print("Student:", students[roll]["name"])
                    print("Roll Number:", roll)
                    print("Total fees paid:", fees_paid)

            elif fees_event_choice == "3":
                roll = input("Enter roll number: ")

                if roll not in students:
                    print("Student not found.")
                else:
                    events = {
                        "1": "Hackathon",
                        "2": "Sports Day",
                        "3": "Cultural Fest",
                        "4": "Tech Exhibition"
                    }

                    print("\n===== AVAILABLE EVENTS =====")
                    for number, event in events.items():
                        print(number, "-", event)

                    event_choice = input("Choose event: ")

                    if event_choice in events:
                        event_name = events[event_choice]

                        if "events" not in students[roll]:
                            students[roll]["events"] = []

                        if event_name in students[roll]["events"]:
                            print("Already registered for this event.")
                        else:
                            students[roll]["events"].append(event_name)
                            save_students(students)

                            print(
                                students[roll]["name"],
                                "registered for",
                                event_name
                            )
                    else:
                        print("Invalid event choice.")

            elif fees_event_choice == "4":
                print("Returning to Main Menu.")
                break

            else:
                print("Invalid choice. Please try again.")

    elif choice == "6":
        print("Exiting College Student Management.")
        break

    else:
        print("Invalid choice. Please try again.")
