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
                                    # Add constraints based on block type
                                    if block_type_a == 'full' and block_type_b == 'full':
                                        model.Add(schedule_vars[f"{course_a}_{section_a}"] + schedule_vars[f"{course_b}_{section_b}"] <= 1)
                                    elif block_type_a == 'first' and block_type_b == 'first':
                                        model.Add(schedule_vars[f"{course_a}_{section_a}"] + schedule_vars[f"{course_b}_{section_b}"] <= 1)
                                    elif block_type_a == 'second' and block_type_b == 'second':
                                        model.Add(schedule_vars[f"{course_a}_{section_a}"] + schedule_vars[f"{course_b}_{section_b}"] <= 1)

    # At least one section of each course should be taken
    for course, sections in classes.items():
        model.Add(sum(schedule_vars[f"{course}_{section_name}"] for section_name in sections) >= 1)

    # Objective: Maximize in-person classes, minimize online classes
    objective_terms = []
    for var in schedule_vars:
        if 'Any' in var:  # This means it's an online class
            objective_terms.append(-1 * schedule_vars[var])  # Penalize online classes

    model.Maximize(sum(objective_terms))

    # Solve the model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0  # Increase solver time limit to 60 seconds
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = [(var.split('_')[0], var.split('_')[1]) for var in schedule_vars if solver.Value(schedule_vars[var]) == 1]
        return result
    else:
        return []