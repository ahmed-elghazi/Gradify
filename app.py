from flask import Flask, render_template, request, jsonify, redirect, url_for
from coursebook import getProfessors
from concurrent.futures import ThreadPoolExecutor, as_completed
from DIYRMP import testAPI
from historicalData import hitTheDB
import re

# Problems:
# If the professor does not exist on RMP, he is not shown on any list
# There is no testing for incorrect inputs (CSSSS instead of CS3345)
# Parallel thread execution needs to be implemented for query's & RMP
# APP.PY file is too large and needs to be broken down into smaller files
# No sorting buttons.
# Use coursebook-master-api?

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/results')
def results():
    course_id = request.args.get('courseID')
    professors = getProfessors(course_id)  # Fetch professors based on course ID
    if(professors == "error"):
        Error = "Invalid Course ID"
        return render_template('error.html', error=Error)
    all_professor_info = []
    chart_data = {
        "professors": [],
        "a_percentages": []
    }
    for professor in professors:
        professor_info = testAPI(professor)
        if professor_info:
            first_name = professor_info[0]
            last_name = professor_info[1]
            rating = professor_info[2]
            quality = professor_info[3]
            take_again = professor_info[4]
            a_percentage = hitTheDB(first_name + " " + last_name)

            if take_again != "N/A":
                try:
                    take_again = float(take_again)
                    take_again = f"{take_again:.0f}%"
                except ValueError:
                    take_again = "N/A"
            
            all_professor_info.append({
                "name": f"{first_name} {last_name}",
                "rating": rating,
                "quality": quality,
                "take_again": take_again,
                "a_percentages": a_percentage  # Ensure this is an array
            })
            
            chart_data["professors"].append(f"{first_name} {last_name}")
            chart_data["a_percentages"].append(a_percentage)
    match = re.match(r"([a-zA-Z]+)(\d+)", course_id)
    letters = match.group(1).upper()  # Capitalize the letters
    numbers = match.group(2)  # Get the numbers
    formatted_code = f"{letters} {numbers}"
        
    
    return render_template('results.html', professors=all_professor_info, chartData=chart_data, courseID = formatted_code)


if __name__ == '__main__':
    app.run(debug=True)

# Use ThreadPoolExecutor to run the requests in parallel
#         with ThreadPoolExecutor(max_workers=4) as executor:
#             # Submit all tasks to the executor
#             future_to_professor = {executor.submit(get_professor_info, professor): professor for professor in professors}
            
#             # Collect the results as they complete
#             for future in as_completed(future_to_professor):
#                 try:
#                     professor_info = future.result()
#                     all_professor_info.append(professor_info)
#                 except Exception as e:
#                     print(f"Exception occurred for professor {future_to_professor[future]}: {e}")


#User enters class in to search
#Verify if course is valid and exists in the coursebook
#Retrieve the list of professors from coursebook
#Retrieve RMP ratings for each professor
#Retrieve UTDGrades stats for professor (Average %, %A, %B, %C, %D, %F)
#Sort results (%A first, then the rating from RMP)
#Display the results

#Later versions:
# Keep track of user's classes and exclude classes that overlap with previously entered classes
# Directly enroll the users in the classes
# Filter classes by open / close / waitlist
# Replace time.sleep() with a better coded version

#Efficiency:
# Use a dictionary to store the professors and their ratings
# Update the table directly instead of reading into placeholder that gets returned from function
# Directly seat the coursebok info in a data base (How would you update it regularly?)
# Make the code not use a visual GUI and instead use a headless browser