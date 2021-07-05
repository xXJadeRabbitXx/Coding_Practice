import argparse
import csv
import json


def parse_csv(COURSES_FILE, STUDENTS_FILE, TESTS_FILE, MARKS_FILE):
    """
    Opens, reads, and organizes csv file data

    :param COURSES_FILE: filepath to courses csv file
    :param STUDENTS_FILE: filepath to students csv file:
    :param TESTS_FILE: filepath to tests csv file:
    :param MARKS_FILE: filepath to marks csv file:
    :return datastructure of organized student data:
    """

    students = {}
    with open(STUDENTS_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for student in csv_reader:
            temp_student = {student["id"]: {"name": student["name"], "tests": []}}
            students.update(temp_student)

    courses = {}
    with open(COURSES_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for course in csv_reader:
            temp_course = {course["id"]: {"name": course["name"], "teacher": course["teacher"]}}
            courses.update(temp_course)

    tests = {}
    with open(TESTS_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for test in csv_reader:
            temp_test = {test["id"]: {"course_id": test["course_id"], "weight": test["weight"]}}
            tests.update(temp_test)

    marks = []
    with open(MARKS_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        marks = list(csv_reader)

    # Combining data from all CSV Files
    for entry in marks:
        test = tests[entry["test_id"]]

        temp_result = {(test["course_id"], courses[test["course_id"]]["name"], courses[test["course_id"]]["teacher"]): {
            "weight": test["weight"], "mark": entry["mark"]}}

        students[entry["student_id"]]["tests"] += [temp_result]

    return students


def calculate_summary(data):
    """
    calculates the students' course data based on given input test data

    :param data: student test data
    :return: student course data
    """

    temp_results = {}
    for entry in data:
        key = list(entry.items())[0][0]
        value = list(entry.items())[0][1]

        weight = int(value["weight"])
        mark = int(value["mark"])

        if key in temp_results:
            temp_results[key]["accumulated_weight"] += weight
            temp_results[key]["accumulated_mark"] += weight * mark / 100
        else:
            temp_results.update({key: {"accumulated_weight": weight, "accumulated_mark": weight * mark / 100}})

    # formatting output
    results = {}
    for key in temp_results:
        value = temp_results[key]
        results.update({key[0]: {"name": key[1], "teacher": key[2], "accumulated_weight": value["accumulated_weight"],
                                 "accumulated_mark": value["accumulated_mark"]}})

    return results


def generate_output(data):
    """
    formats datastructure of student data into the appropriate JSON string

    :param data: student data
    :return: JSON string
    """

    # formatting output
    formatted_student_data = []
    for student_id in data:
        student_data = data[student_id]
        student_courses = student_data["courses"]

        formatted_course_data = []
        total_average = 0
        for course_id in student_courses:
            course_data = student_courses[course_id]

            # Course exams MUST have a weight of 100% (customer requirement)
            if course_data["accumulated_weight"] != 100:
                return json.dumps({"error": "invalid course weights"}, indent=2, sort_keys=True)
            else:
                total_average += course_data["accumulated_mark"] / len(student_courses)

            formatted_course_data.append(
                {"id": int(course_id), "name": course_data["name"], "teacher": course_data["teacher"],
                 "courseAverage": round(course_data["accumulated_mark"], 2)})

        formatted_student_data.append(
            {"id": int(student_id), "name": student_data["name"], "totalAverage": round(total_average, 2),
             "courses": formatted_course_data})

    return json.dumps({"students": formatted_student_data}, indent=2, sort_keys=True)


def main(args=None):
    # Retrieving arguments from command
    parser = argparse.ArgumentParser(description="Process student csv files.")

    parser.add_argument("courses_file", type=str, help="path to courses file")
    parser.add_argument("students_file", type=str, help="path to students file")
    parser.add_argument("tests_file", type=str, help="path to tests file")
    parser.add_argument("marks_file", type=str, help="path to marks file")
    parser.add_argument("output_file", type=str, help="path to output file")

    args = parser.parse_args(args)

    # Processing Data
    student_data = parse_csv(args.courses_file, args.students_file, args.tests_file, args.marks_file)

    for _, data in student_data.items():
        data["courses"] = calculate_summary(data["tests"])

    json_result = generate_output(student_data)

    # Output Data
    with open(args.output_file, mode="w") as output_file:
        output_file.write(json_result)


if __name__ == '__main__':
    main()
