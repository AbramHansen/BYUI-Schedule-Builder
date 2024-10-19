from ortools.sat.python import cp_model

def main():
    # Define classes with block types
    classes = {
        'Math 101': {
            'Section A': [('Monday', 9.0, 10.0, 'first'), ('Wednesday', 9.0, 10.0, 'first')],
            'Section B': [('Tuesday', 10.5, 11.5, 'second'), ('Thursday', 10.5, 11.5, 'second')]
        },
        'Math 102': {
            'Section A': [('Monday', 11.0, 12.0, 'first'), ('Wednesday', 11.0, 12.0, 'first')],
            'Section B': [('Any', 0, 24, 'full')]  # Generic online class time
        },
        'Math 201': {
            'Section A': [('Tuesday', 13.0, 14.0, 'second'), ('Thursday', 13.0, 14.0, 'second')]
        },
        'Math 401': {
            'Section A': [('Monday', 14.0, 16.0, 'full'), ('Thursday', 15.0, 16.0, 'full')]
        },
        'CSE 101': {
            'Section A': [('Thursday', 11.0, 12.0, 'first'), ('Friday', 9.0, 10.0, 'first')],
            'Section B': [('Tuesday', 10.5, 11.5, 'second'), ('Thursday', 10.5, 11.5, 'second')],
            'Section C': [('Any', 0, 24, 'full')]  # Generic online class time
        },
        'CSE 110': {
            'Section A': [('Monday', 9.0, 12.0, 'full'), ('Wednesday', 9.0, 10.0, 'full')],
        }
    }
    schedule(classes)

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
            for course_b, sections_b in classes.items():
                if course_a == course_b:
                    continue  # Skip the same course
                for section_b, time_slots_b in sections_b.items():
                    for (day_a, start_a, end_a, block_type_a) in time_slots_a:
                        for (day_b, start_b, end_b, block_type_b) in time_slots_b:
                            if day_a == day_b and day_a != 'Any':
                                # Check for overlap
                                if start_a < end_b and start_b < end_a:  # Overlap condition
                                    if block_type_a == 'full' or block_type_b == 'full':
                                        # Full block classes cannot overlap with any block type
                                        model.Add(schedule_vars[f"{course_a}_{section_a}"] + schedule_vars[f"{course_b}_{section_b}"] <= 1)
                                    elif block_type_a != block_type_b:
                                        # Different block types (first and second) can overlap
                                        continue
                                    else:
                                        # Same block types (first or second) cannot overlap
                                        model.Add(schedule_vars[f"{course_a}_{section_a}"] + schedule_vars[f"{course_b}_{section_b}"] <= 1)

    # At least one section of each course should be taken
    for course, sections in classes.items():
        model.Add(sum(schedule_vars[f"{course}_{section_name}"] for section_name in sections) >= 1)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Schedule:")
        for var in schedule_vars:
            if solver.Value(schedule_vars[var]) == 1:
                print(var)
    else:
        print('No solution found.')

if __name__ == '__main__':
    main()
