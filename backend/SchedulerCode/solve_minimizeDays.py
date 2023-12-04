# Scheduler
# Returns Schedule with minimum number of days (Least amount of days to come to school)
from ortools.sat.python import cp_model
class CoursesSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, selection, all_courses, all_crns, limit=0):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._selection = selection
        self._all_courses = all_courses
        self._all_crns = all_crns
        self._solution_count = 0
        self._solution_limit = limit
        self._solutions = []

    def on_solution_callback(self):
        self._solution_count += 1
        current_solution = []
        
        for course in self._all_courses:
            for crn in self._all_crns:
                if (crn, course) in self._selection and self.Value(self._selection[(crn, course)]) == 1:
                    current_solution.append(crn)
        
        self._solutions.append(current_solution)

        if self._solution_limit and self._solution_count >= self._solution_limit:
            # print(f"Stop search after {self._solution_limit} solutions")
            self.StopSearch()

    def solution_count(self):
        return self._solution_count
    
    def get_solutions(self):
        return self._solutions
######################################################################################################################################################   
def to_continuous_minutes(entry):
    day_map = {
        'M': 0,      # Monday
        'T': 2400,   # Tuesday
        'W': 2400*2,   # Wednesday
        'R': 2400*3,   # Thursday
        'F': 2400*4,   # Friday
        'S' :2400*5, # Saturday
        'U' :2400*6  # Sunday
    }
    if entry == 'None':
        return -1, -1
    day, start, end = entry.split()
    return day_map[day] + int(start), day_map[day] + int(end)

# given 2 times slots return True if no conflict
def conflict_between_slots(time1, time2):
    # One of the slots is a class with no timing
    if time1 == (-1. -1) or time2 == (-1. -1):
        return False
    s1, e1 = time1
    s2, e2 = time2    
    return not (s1 > e2 or s2 > e1)
######################################################################################################################################################
def do_solve(input_to_algo, limit):
    for i in range(len(input_to_algo)):
        all = []
        for string in input_to_algo[i][2]:
            all.append(to_continuous_minutes(string))
        input_to_algo[i].append(all)
    
    # for both crn, none of there times slots are in conflict
    def conflict_between_sections(crn1, crn2):
        for time1 in crn_to_times[crn1]:
            for time2 in crn_to_times[crn2]:
                if conflict_between_slots(time1, time2): # If any slot conflicts
                    return True
        return False # No conflicts found!
        # course with set of all crns/sections
    
    course_to_crns = {
        d[1] : set()
        for d in input_to_algo         
    }
    
    for d in input_to_algo:
        course_to_crns[d[1]].add(d[0])
    
    all_crns = {d[0] for d in input_to_algo}
    all_courses = {d[1] for d in input_to_algo}

    # crn with list of time slots
    crn_to_times = {
        d[0] : d[3]
        for d in input_to_algo
    }

    # crn mapped to course
    crn_to_course = {
        d[0] : d[1]
        for d in input_to_algo
    }
    ######################################################################################################################
    model = cp_model.CpModel()

    # Create Boolean variable for each day of the week
    day_vars = {day: model.NewBoolVar(f"day_{day}") for day in range(7)}  # 0: Monday ... 6: Sunday
    # {0: day_0(0..1), 1: day_1(0..1), 2: day_2(0..1), 3: day_3(0..1), 4: day_4(0..1), 5: day_5(0..1), 6: day_6(0..1)}

    selection = {} 
    for crn in all_crns:
        for course in all_courses:
            if crn in course_to_crns[course]:
                selection[(crn, course)] = model.NewBoolVar(f"crn={crn} -> class={course} \n")   
                # eg crn=24735 -> class=CS04400 

    # exactly 1 crn per course
    for course in all_courses:
        model.AddExactlyOne(selection[(crn, course)] for crn in all_crns if crn in course_to_crns[course])

    # no conflicts
    for crn1 in all_crns:
        for crn2 in all_crns:
            if crn1 != crn2 and conflict_between_sections(crn1, crn2):
                for course in all_courses:
                    if ((crn1 in course_to_crns[course] and crn2 not in course_to_crns[course]) 
                        or (crn1 not in course_to_crns[course] and crn2 in course_to_crns[course])):
                        model.Add(selection[(crn1, crn_to_course[crn1])] + selection[(crn2, crn_to_course[crn2])] <= 1)

    
    # Link day variables to CRN selection
    for crn in all_crns:
        for day in range(7):
            # Check if the CRN has a class on this day
            if any(start // 2400 == day for start, _ in crn_to_times[crn]):
                # If CRN is selected and it has a class on 'day', set day_vars[day] to true
                model.AddBoolOr([selection[(crn, crn_to_course[crn])].Not(), day_vars[day]])

    # Minimize the sum of day variables
    model.Minimize(sum(day_vars.values()))

    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    # Time limit
    solver.parameters.max_time_in_seconds = 120  # 120 sec

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Get Smallest number of days possible
    optimal_value = int(solver.ObjectiveValue())
    ######################################################################################################################
    # Now use the optimal value and find all schedules that satisfy it
    
    # Create a new model
    enum_model = cp_model.CpModel()

    # Add all like original model (excluding Minimize constraint)
    # Create Boolean variable for each day of the week
    day_vars = {day: enum_model.NewBoolVar(f"day_{day}") for day in range(7)}  # 0: Monday ... 6: Sunday
    # {0: day_0(0..1), 1: day_1(0..1), 2: day_2(0..1), 3: day_3(0..1), 4: day_4(0..1), 5: day_5(0..1), 6: day_6(0..1)}

    selection = {} 
    for crn in all_crns:
        for course in all_courses:
            if crn in course_to_crns[course]:
                selection[(crn, course)] = enum_model.NewBoolVar(f"crn={crn} -> class={course} \n")   
                # eg crn=24735 -> class=CS04400 

    # exactly 1 crn per course
    for course in all_courses:
        enum_model.AddExactlyOne(selection[(crn, course)] for crn in all_crns if crn in course_to_crns[course])

    # no conflicts
    for crn1 in all_crns:
        for crn2 in all_crns:
            if crn1 != crn2 and conflict_between_sections(crn1, crn2):
                for course in all_courses:
                    if ((crn1 in course_to_crns[course] and crn2 not in course_to_crns[course]) 
                        or (crn1 not in course_to_crns[course] and crn2 in course_to_crns[course])):
                        enum_model.Add(selection[(crn1, crn_to_course[crn1])] + selection[(crn2, crn_to_course[crn2])] <= 1)

    # Link day variables to CRN selection
    for crn in all_crns:
        for day in range(7):
            # Check if the CRN has a class on this day
            if any(start // 2400 == day for start, _ in crn_to_times[crn]):
                # If CRN is selected and it has a class on 'day', set day_vars[day] to true
                enum_model.AddBoolOr([selection[(crn, crn_to_course[crn])].Not(), day_vars[day]])

    # Now optimal value is a constraint 
    enum_model.Add(sum(day_vars.values()) == optimal_value)

    # Create a new solver instance for enumeration
    enum_solver = cp_model.CpSolver()
    enum_solver.parameters.enumerate_all_solutions = True

    total_possibles = 1
    for course in course_to_crns:
        total_possibles *= len(course_to_crns[course]) 

    if total_possibles > limit:
        total_possibles = limit

    # Attach the solution printer to the new solver
    enum_solution_printer = CoursesSolutionPrinter(selection, all_courses, all_crns, limit=total_possibles)

    # Solve the new model
    enum_solver.SearchForAllSolutions(enum_model, enum_solution_printer)

    solutions = enum_solution_printer.get_solutions()
    return solutions
    
