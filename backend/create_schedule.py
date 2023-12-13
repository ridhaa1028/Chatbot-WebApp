from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify, make_response
from sqlalchemy import and_, or_
from .models import SectionTally

from .SchedulerCode import time_formatting
from .SchedulerCode.solve_basic import do_solve as do_solve0
from .SchedulerCode.solve_minimizeDays import do_solve as do_solve1 
from .SchedulerCode.solve_minimizeGap import do_solve as do_solve2
from .SchedulerCode.solve_minimizeGapAndDays import do_solve as do_solve3 


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('course_list', type=list, location='json', required=True)
parser.add_argument('limit', type=int, location='json', required=True)
parser.add_argument('constraint', type=int, location='json', required=True)

class ScheduleCreationResource(Resource):
    def __init__(self, Session):
        self.Session = Session
    
    
    # Get
    def fetch_course(self, course_list):
        # Query based on the list of tuples
        with self.Session() as session:
            results = session.query(SectionTally).filter(or_(*(and_(SectionTally.subj == subj, SectionTally.crse == crse) for subj, crse in course_list))).all()
            return results

    def post(self):
        args = parser.parse_args()
        course_list = args['course_list']
        limit = args.get('limit') 
        constraint = args.get('constraint')  

        if limit == -1: 
            limit = float('inf')

        # Create a new session for this request
        session = self.Session()

        try:
            results = self.fetch_course(course_list) 

            # Check to see if each course in the query is even a course or being offered currently Spring 2024
            unique_combo = {course.subj + " " + course.crse for course in results}
            all_combo = {p[0] + " " + p[1] for p in course_list}

            not_found = all_combo - unique_combo  # Set difference to find courses not found

            if not_found:
                return make_response(jsonify({"error": "One or more courses not found", "not_found": list(not_found)}), 400)


            # CSP Solver will take in a list of lists representing each possible section
            # Eg: [crn, subj+crse, list of Day Start End Time block Strings]
            # Example list: a list of many sections like [22143, 'ARAB12102', ['M 1100 1215', 'W 1100 1215']]
            input_to_algo = []
            for c in results:
                input_to_algo.append([c.crn, c.subj + c.crse, time_formatting.extract_times(c.day_beg_end_bldgroom_type)])


            if constraint == 0:
                schedules = do_solve0(input_to_algo)  # Solve the CSP
            elif constraint == 1:
                schedules = do_solve1(input_to_algo)  
            elif constraint == 2:
                schedules = do_solve2(input_to_algo) 
            else:
                schedules = do_solve3(input_to_algo)  

            # Was a weird bug with limits in CSP Solver. Doing Manually now. Efficiency should be same.
            print("len before", len(schedules))
            if limit and len(schedules) > limit:
                print(limit)
                schedules = schedules[:limit]

            # Fetch course details and serialize
            detailed_schedules = []
            for sched in schedules:
                detailed_schedule = []
                for crn in sched:
                    course = session.query(SectionTally).filter_by(crn=crn).first()
                    detailed_schedule.append(course.serialize())
                detailed_schedules.append(detailed_schedule)

            return jsonify({'schedules': detailed_schedules})

        finally:
            session.close() 