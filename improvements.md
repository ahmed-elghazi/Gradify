# Problems

- **Professor Availability**: If the professor does not exist on Rate My Professors (RMP), they are not shown in any list.
- **Input Validation**: There is no testing for incorrect inputs (e.g., "CSSSS" instead of "CS3345").
- **Thread Execution**: Parallel thread execution needs to be implemented for queries & RMP data retrieval.
- **File Size and Organization**: The `app.py` file is too large and needs to be broken down into smaller, more manageable files.
- **Sorting Functionality**: The application currently lacks sorting buttons for sorting results based on different criteria.
- **API Consideration**: Consider using `coursebook-master-api` for more robust data handling.

# Parallel Execution

- **ThreadPoolExecutor**: Use `ThreadPoolExecutor` to run the requests in parallel.
  
  Example:
  ```python
  with ThreadPoolExecutor(max_workers=4) as executor:
      # Submit all tasks to the executor
      future_to_professor = {executor.submit(get_professor_info, professor): professor for professor in professors}
      
      # Collect the results as they complete
      for future in as_completed(future_to_professor):
          try:
              professor_info = future.result()
              all_professor_info.append(professor_info)
          except Exception as e:
              print(f"Exception occurred for professor {future_to_professor[future]}: {e}")
  ```

# Current Functionality

- **User Input**: Users enter a class ID to search for courses.
- **Course Validation**: Verify if the course ID is valid and exists in the coursebook.
- **Professor Retrieval**: Retrieve the list of professors associated with the course from the coursebook.
- **RMP Data Retrieval**: Retrieve RMP ratings for each professor.
- **Grade Stats**: Retrieve UTDGrades stats for each professor (e.g., Average %, %A, %B, %C, %D, %F).
- **Sorting and Display**: Sort results by %A first, then by the RMP rating, and display the results.

# Future Improvements

- **Class Tracking**: Keep track of users' classes and exclude classes that overlap with previously entered classes.
- **Automated Enrollment**: Add functionality to directly enroll users in selected classes.
- **Class Status Filtering**: Filter classes by open, closed, or waitlist status.
- **Improved Sleep Management**: Replace `time.sleep()` with a more efficient method for handling delays.

# Efficiency Enhancements

- **Data Structure**: Use a dictionary to store professors and their ratings for better performance.
- **Direct Table Updates**: Update the table directly instead of reading into a placeholder that gets returned from a function.
- **Database Integration**: Directly seed coursebook information into a database. Consider how to regularly update the database.
- **Headless Browser**: Modify the code to avoid using a visual GUI and instead use a headless browser for web scraping.
