def calculate_time(steps):
    """
    Calculate the start and end times of steps in a sequence, considering prerequisites and chef availability.

    :param steps: A list of step objects, each with attributes:
                  - prerequisites: A list of prerequisite steps.
                  - occupies_chef (bool): Whether the step requires the chef.
                  - duration (int): Duration of the step in minutes.
                  - name (str): Name of the step.
    :type steps: list
    :returns: A tuple containing:
              - A list of strings describing when each step starts and ends.
              - The time when the last step finishes.
    :rtype: tuple
    :raises KeyError: If a prerequisite step is missing from the step_times dictionary.
    """
    results = []
    step_times = {}
    chef_busy_until = 0
    last_end_time = 0

    while steps:
        current_batch = []

        for step in steps:
            if step.prerequisites.exists():
                if not all(prerequisite in step_times for prerequisite in step.prerequisites.all()):
                    continue

            if step.occupies_chef:
                start_time = chef_busy_until
            else:
                start_time = 0

            if step.prerequisites.exists():
                prerequisite_end_times = [
                    step_times[prerequisite]['end_time']
                    for prerequisite in step.prerequisites.all()
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
            last_end_time = max(last_end_time, end)

        steps = [step for step in steps if step not in [s for s, _, _ in current_batch]]

    return results, last_end_time
