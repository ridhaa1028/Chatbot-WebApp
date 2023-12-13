# Scheduler
# Schedule with minimum gap between classes (least wait time between class) //Excluding 15 min between classes
from ortools.sat.python import cp_model
class CoursesSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, selection, all_courses, all_crns):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._selection = selection
        self._all_courses = all_courses
        self._all_crns = all_crns
        self._solution_count = 0
        self._solutions = []

    def on_solution_callback(self):
        self._solution_count += 1
        current_solution = []
        
        for course in self._all_courses:
            for crn in self._all_crns:
                if (crn, course) in self._selection and self.Value(self._selection[(crn, course)]) == 1:
                    current_solution.append(crn)
        
        self._solutions.append(current_solution)

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
def do_solve(input_to_algo):
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

    model = cp_model.CpModel()

    selection = {} 
    for crn in all_crns:
        for course in all_courses:
            if crn in course_to_crns[course]:
                selection[(crn, course)] = model.NewBoolVar(f"crn={crn} -> class={course} \n")
                

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

    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True


    solution_printer = CoursesSolutionPrinter(selection, all_courses, all_crns)
    
    # Solve the CSP
    solver.SearchForAllSolutions(model, solution_printer)
    #print(f"Total number of solutions found: {solution_printer.solution_count()}")

    solutions = solution_printer.get_solutions()
    
        ######################################################################################################################
    # Now to manually get the time breaks and minimize

    # Given two times in military time: return time gap in minutes
    def time_gap(start, end):
        # Split the military time into hours and minutes
        start_hours, start_minutes = divmod(start, 100)
        end_hours, end_minutes = divmod(end, 100)

        # Convert times to minutes
        start_total_minutes = start_hours * 60 + start_minutes
        end_total_minutes = end_hours * 60 + end_minutes

        # Calculate the difference
        return end_total_minutes - start_total_minutes

    # Function given a schedule returns time breaks in between classes
    # Obviously there may be 15 minutes in between classes (don't count those)
    def get_total_gaptimes(schedule):
        total_gaps = 0

        # schedule is a list of crns (a valid schedules)
        timings = {crn: crn_to_times[crn] for crn in schedule}
        # classes with double periods are already combined!
        # times is a list of (start, end) time encodings
        times = []
        for k in timings:
            for pairs in timings[k]:
                times.append(pairs)
        times = [t for t in times if t != (-1, -1)]
        times.sort()
        # 8520 -> 8520 mod 2400 returns time (1320 = 1:20pm)
                  # 8520 // 2400 returns 3 -> Thursday  
        for i in range(len(times)-1):
            end_current = times[i][1]
            start_next = times[i+1][0]

            # if same day and more than 20 min. gap
            if (end_current // 2400) == (start_next // 2400):
                gap = time_gap(end_current, start_next)
                if gap >= 20:
                    total_gaps += gap
        
        return total_gaps
    
    min_gap_time = float('inf')
    for schedule in solutions:
        total_gaps = get_total_gaptimes(schedule)
        if total_gaps < min_gap_time:
            min_gap_time = total_gaps
    
    return [s for s in solutions if get_total_gaptimes(s) == min_gap_time]