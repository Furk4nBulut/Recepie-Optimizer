import pytest
import json

def calculate_time(steps):
    results = []
    step_times = {}
    chef_busy_until = 0

    while steps:
        current_batch = []
        for step in steps:
            if step.prerequisites:
                if not all(prerequisite in step_times for prerequisite in step.prerequisites):
                    continue

            if step.occupies_chef:
                start_time = chef_busy_until
            else:
                start_time = 0

            if step.prerequisites:
                prerequisite_end_times = [
                    step_times[prerequisite]['end_time']
                    for prerequisite in step.prerequisites
                    if prerequisite in step_times
                ]
                if prerequisite_end_times:
                    start_time = max(start_time, max(prerequisite_end_times))

            end_time = start_time + step.duration

            current_batch.append((step, start_time, end_time))

            if step.occupies_chef:
                chef_busy_until = end_time

        for step, start, end in current_batch:
            step_times[step] = {'start_time': start, 'end_time': end}
            results.append(f"'{step.name}' starts at minute {start} and ends at minute {end}.")

        steps = [step for step in steps if step not in [s for s, _, _ in current_batch]]

    return results
class Step:
    def __init__(self, name, duration, occupies_chef=True, prerequisites=None):
        self.name = name
        self.duration = duration
        self.occupies_chef = occupies_chef
        self.prerequisites = prerequisites if prerequisites else []


def load_test_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def steps_from_json(step_data):
    step_dict = {}
    for step_info in step_data:
        step = Step(
            name=step_info["name"],
            duration=step_info["duration"],
            occupies_chef=step_info["occupies_chef"],
            prerequisites=[step_dict[prereq] for prereq in step_info["prerequisites"]]
        )
        step_dict[step.name] = step
    return list(step_dict.values())


@pytest.mark.parametrize("test_case", load_test_data("test_data_no_prerequisites_chef_not_busy.json").items())
def test_no_prerequisites_chef_not_busy(test_case):
    test_name, test_data = test_case
    steps = steps_from_json(test_data["steps"])

    results = calculate_time(steps)

    expected = test_data["expected"]
    assert results == expected

@pytest.mark.parametrize("test_case", load_test_data("test_data_with_prerequisites_chef_not_busy.json").items())
def test_with_prerequisites_chef_not_busy(test_case):
    test_name, test_data = test_case
    steps = steps_from_json(test_data["steps"])

    results = calculate_time(steps)

    expected = test_data["expected"]
    assert results == expected

@pytest.mark.parametrize("test_case", load_test_data("test_data_no_prerequisites_chef_busy.json").items())
def test_no_prerequisites_chef_busy(test_case):
    test_name, test_data = test_case
    steps = steps_from_json(test_data["steps"])

    results = calculate_time(steps)

    expected = test_data["expected"]
    assert results == expected

@pytest.mark.parametrize("test_case", load_test_data("test_data_with_prerequisites_chef_busy.json").items())
def test_with_prerequisites_chef_busy(test_case):
    test_name, test_data = test_case
    steps = steps_from_json(test_data["steps"])

    results = calculate_time(steps)

    expected = test_data["expected"]
    assert results == expected
