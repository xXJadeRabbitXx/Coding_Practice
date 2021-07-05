import json

import main

# Test Methodology is a Black-Box interface-type test

# Given the scale of the project and the requirement for Unit Testing I did not resort to more complex test processes
# such as a test framework

# I also avoided white-box testing methodologies such as code coverage for that reason,
# but I understand such processes exist

def test_parse():
    """
        Test 1: Example Case
    """
    expected_output = {'1': {'name': 'A', 'tests': [{('2', 'History', 'Mrs. P'): {'weight': '40', 'mark': '32'}},
                                                    {('2', 'History', 'Mrs. P'): {'weight': '60', 'mark': '65'}},
                                                    {('3', 'Math', 'Mrs. C'): {'weight': '90', 'mark': '78'}},
                                                    {('3', 'Math', 'Mrs. C'): {'weight': '10', 'mark': '40'}}]}}
    actual_output = main.parse_csv("Test Files/courses.csv", "Test Files/students.csv", "Test Files/tests.csv",
                                   "Test Files/marks.csv")

    assert expected_output == actual_output
    print("Parse Test 1 successful")

    """
    Test 2: Malformed CSV
    """
    try:
        main.parse_csv("Test Files/courses.csv", "Test Files/students.csv", "Test Files/tests (modified).csv",
                       "Test Files/marks.csv")
        print("Parse Test 2 failed")
    except KeyError:
        print("Parse Test 2 successful")
    except:
        print("Parse Test 2 failed")


def test_gen():
    """
        Test 1: Example Case
    """
    input = {'1': {'name': 'A', 'courses': {
        '1': {'name': 'Biology', 'teacher': 'Mr. D', 'accumulated_weight': 100, 'accumulated_mark': 90.1},
        '2': {'name': 'History', 'teacher': 'Mrs. P', 'accumulated_weight': 100, 'accumulated_mark': 51.8},
        '3': {'name': 'Math', 'teacher': 'Mrs. C', 'accumulated_weight': 100, 'accumulated_mark': 74.2}}}}

    expected_output = "{\n  \"students\": [\n    {\n      \"courses\": [\n        {\n          \"courseAverage\": " \
                      "90.1,\n          \"id\": 1,\n          \"name\": \"Biology\",\n          \"teacher\": \"Mr. " \
                      "D\"\n        },\n        {\n          \"courseAverage\": 51.8,\n          \"id\": 2," \
                      "\n          \"name\": \"History\",\n          \"teacher\": \"Mrs. P\"\n        },\n        {\n " \
                      "         \"courseAverage\": 74.2,\n          \"id\": 3,\n          \"name\": \"Math\"," \
                      "\n          \"teacher\": \"Mrs. C\"\n        }\n      ],\n      \"id\": 1,\n      \"name\": " \
                      "\"A\",\n      \"totalAverage\": 72.03\n    }\n  ]\n}"

    actual_output = main.generate_output(input)

    assert expected_output == actual_output
    print("Generation Test 1 successful")

    """
           Test 2: Incorrect Weights Case (Too High)
    """
    input = {'1': {'name': 'A', 'courses': {
        '1': {'name': 'Biology', 'teacher': 'Mr. D', 'accumulated_weight': 110, 'accumulated_mark': 90.1},
        '2': {'name': 'History', 'teacher': 'Mrs. P', 'accumulated_weight': 100, 'accumulated_mark': 51.8},
        '3': {'name': 'Math', 'teacher': 'Mrs. C', 'accumulated_weight': 100, 'accumulated_mark': 74.2}}}}

    expected_output = "{\n  \"error\": \"invalid course weights\"\n}"
    actual_output = main.generate_output(input)

    assert expected_output == actual_output
    print("Generation Test 2 successful")

    """
           Test 3: Incorrect Weights Case (Too Low)
    """
    input = {'1': {'name': 'A', 'courses': {
        '1': {'name': 'Biology', 'teacher': 'Mr. D', 'accumulated_weight': 90, 'accumulated_mark': 90.1},
        '2': {'name': 'History', 'teacher': 'Mrs. P', 'accumulated_weight': 100, 'accumulated_mark': 51.8},
        '3': {'name': 'Math', 'teacher': 'Mrs. C', 'accumulated_weight': 100, 'accumulated_mark': 74.2}}}}

    expected_output = "{\n  \"error\": \"invalid course weights\"\n}"
    actual_output = main.generate_output(input)

    assert expected_output == actual_output
    print("Generation Test 3 successful")

    """
           Test 3: Incorrect Weights Case (Negative)
    """
    input = {'1': {'name': 'A', 'courses': {
        '1': {'name': 'Biology', 'teacher': 'Mr. D', 'accumulated_weight': -100, 'accumulated_mark': 90.1},
        '2': {'name': 'History', 'teacher': 'Mrs. P', 'accumulated_weight': 100, 'accumulated_mark': 51.8},
        '3': {'name': 'Math', 'teacher': 'Mrs. C', 'accumulated_weight': 100, 'accumulated_mark': 74.2}}}}

    expected_output = "{\n  \"error\": \"invalid course weights\"\n}"
    actual_output = main.generate_output(input)

    assert expected_output == actual_output
    print("Generation Test 4 successful")


def test_calc():
    """
        Test 1: Example Case
    """
    input = [{('1', 'Biology', 'Mr. D'): {'weight': '10', 'mark': '78'}},
             {('1', 'Biology', 'Mr. D'): {'weight': '40', 'mark': '87'}},
             {('1', 'Biology', 'Mr. D'): {'weight': '50', 'mark': '95'}},
             {('2', 'History', 'Mrs. P'): {'weight': '40', 'mark': '32'}},
             {('2', 'History', 'Mrs. P'): {'weight': '60', 'mark': '65'}},
             {('3', 'Math', 'Mrs. C'): {'weight': '90', 'mark': '78'}},
             {('3', 'Math', 'Mrs. C'): {'weight': '10', 'mark': '40'}}]

    expected_output = {
        '1': {'name': 'Biology', 'teacher': 'Mr. D', 'accumulated_weight': 100, 'accumulated_mark': 90.1},
        '2': {'name': 'History', 'teacher': 'Mrs. P', 'accumulated_weight': 100, 'accumulated_mark': 51.8},
        '3': {'name': 'Math', 'teacher': 'Mrs. C', 'accumulated_weight': 100, 'accumulated_mark': 74.2}}

    actual_output = main.calculate_summary(input)

    assert expected_output == actual_output, "Calculation Test 1 failed"
    print("Calculation Test 1 successful")

    """
        Test 2: Empty Case
    """
    input = []

    expected_output = {}

    actual_output = main.calculate_summary(input)

    assert expected_output == actual_output, "Calculation Test 2 failed"
    print("Calculation Test 2 successful")


def test_function():
    """
        Entire Program Test
    """

    main.main(["Test Files/courses.csv", "Test Files/students.csv", "Test Files/tests.csv", "Test Files/marks.csv",
               "output.csv"])

    with open("output.csv") as actual_output:
        actual_json = json.load(actual_output)
        with open("Test Files/output.json") as expected_output:
            expected_json = json.load(expected_output)

            actual, expected = json.dumps(actual_json, sort_keys=True), json.dumps(expected_json, sort_keys=True)
            assert actual == expected

    print("Function Test passed")


if __name__ == '__main__':
    test_parse()
    test_calc()
    test_gen()
    test_function()
