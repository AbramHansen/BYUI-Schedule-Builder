from ortools.sat.python import cp_model

def schedule(classes):
    model = cp_model.CpModel()
    
    # Create decision variables
    schedule_vars = {}
    for course, sections in classes.items():
        for section_name, time_slots in sections.items():
            var_name = f"{course}_{section_name}"
            schedule_vars[var_name] = model.NewBoolVar(var_name)

    # Add constraints to ensure classes don't overlap based on block types
    for course_a, sections_a in classes.items():
        for section_a, time_slots_a in sections_a.items():
            for (day_a, start_a, end_a, block_type_a) in time_slots_a:
                if day_a == 'Any':
                    continue  # Skip online classes
                for course_b, sections_b in classes.items():
                    if course_a == course_b:
                        continue  # Skip the same course
                    for section_b, time_slots_b in sections_b.items():
                        for (day_b, start_b, end_b, block_type_b) in time_slots_b:
                            if day_b == 'Any':
                                continue  # Skip online classes
                            if day_a == day_b:
                                # Check for overlap
                                if start_a < end_b and start_b < end_a:  # Overlap condition
                                    # Debug information
                                    print(f"Conflict between {course_a} {section_a} and {course_b} {section_b} on {day_a} from {start_a} to {end_a} and {start_b} to {end_b}")

                                    # Add constraints based on block type
                                    if block_type_a == 'full' and block_type_b == 'full':
                                        model.Add(schedule_vars[f"{course_a}_{section_a}"] + schedule_vars[f"{course_b}_{section_b}"] <= 1)
                                    elif block_type_a == 'first' and block_type_b == 'first':
                                        model.Add(schedule_vars[f"{course_a}_{section_a}"] + schedule_vars[f"{course_b}_{section_b}"] <= 1)
                                    elif block_type_a == 'second' and block_type_b == 'second':
                                        model.Add(schedule_vars[f"{course_a}_{section_a}"] + schedule_vars[f"{course_b}_{section_b}"] <= 1)
                                    # Allow first and second blocks to overlap
                                    # No additional constraints needed here

    # At least one section of each course should be taken
    for course, sections in classes.items():
        model.Add(sum(schedule_vars[f"{course}_{section_name}"] for section_name in sections) >= 1)

    # Solve the model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0  # Increase solver time limit to 60 seconds
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Schedule:")
        for var in schedule_vars:
            if solver.Value(schedule_vars[var]) == 1:
                print(var)
    else:
        print('No solution found.')

# New class data
classes = {
    'CSE 220C': {
        'A1': [('Any', 0, 24, 'full')], 
        'A2': [('W', 13.25, 14.25, 'first')], 
        'A3': [('W', 13.25, 14.25, 'second')], 
        'A4': [('Any', 0, 24, 'full')]
    },
    'CSE 336': {
        'B3': [('M', 14.5, 16, 'first'), ('W', 14.5, 16, 'first')], 
        'B5': [('T', 14.5, 16, 'second'), ('R', 14.5, 16, 'second')], 
        'B7': [('T', 9, 10, 'first'), ('R', 9, 10, 'first')], 
        'B9': [('T', 10.25, 11.25, 'second'), ('R', 10.25, 11.25, 'second')]
    },
    'PSY 101': {
        'A17': [('M', 14.5, 16, 'full'), ('W', 14.5, 15, 'full'), ('F', 14.5, 16, 'full')]
    },
    'CSE 210': {
        'C4': [('M', 10.25, 11.25, 'full'), ('W', 15, 18, 'full'), ('F', 10.25, 11.25, 'full')]
    }
}

schedule(classes)
