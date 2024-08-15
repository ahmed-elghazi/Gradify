Thank you for the correction. Here's the updated README with the correct structure:

---

# Dynamic Coursebook and Professor Rating System

## Overview

This project is a Flask-based web application designed to help students at the University of Texas at Dallas search for courses and view comprehensive professor ratings and grade distributions. The application integrates data from multiple sources, including the university coursebook and Rate My Professors, to provide users with up-to-date information on courses and instructors.

## Features

- **Search Courses**: Allows users to search for courses by their course ID.
- **View Professor Ratings**: Displays professor ratings, including average ratings, difficulty, and percentage of students who would take the professor again.
- **Grade Distribution**: Provides grade distribution data for professors, 4.0 (A+ or A), Pass (A-, B+, B, B-, C+ C), Fail (C-, D+, D, D-, F) and Withdraw.
- **Interactive Frontend**: Users can select professor and respective data results dynamically using a responsive and interactive interface built with HTML, CSS, and JavaScript.
- **Real-time Data Retrieval**: Utilizes web scraping and asynchronous processing to fetch the latest data from the university coursebook and Rate My Professors.
- **Secure Database Access**: Connects to MongoDB for historical data retrieval while ensuring secure access through environment variables.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+**
- **MongoDB**: Ensure you have a MongoDB instance running, either locally or via a cloud service like MongoDB Atlas.
- **Web Browser**: Chrome or a Chromium-based browser (for Selenium).

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/coursebook-rating-system.git
cd coursebook-rating-system
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Required Libraries

Install the necessary Python libraries using pip:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of your project directory and add your MongoDB URI and other sensitive information:

```plaintext
MONGO_URI=mongodb+srv://username:password@cluster-url/dbname?retryWrites=true&w=majority
```

### 5. WebDriver Setup for Selenium

Selenium requires a web driver to interact with the browser. The application uses `webdriver-manager` to handle the installation:

```bash
python -m webdriver_manager.chrome
```

### 6. Run the Application

Start the Flask application by running:

```bash
python app.py
```

The application should now be running on `http://127.0.0.1:5000/`. Open this URL in your web browser to use the application.

## Usage

- **Home Page**: Start by entering a course ID (e.g., CS3345) to search for relevant courses and professors.
- **Results Page**: View a list of professors teaching the course along with their ratings, grade distribution, and other relevant information.
- **Error Handling**: If the course ID is invalid or no data is found, the application will redirect you to an error page.

## Project Structure

```
coursebook-rating-system/
│
├── app.py                      # Main Flask application
├── coursebook.py               # Handles web scraping from the coursebook
├── DIYRMP.py                   # Integrates with Rate My Professors
├── historicalData.py           # Retrieves historical data from MongoDB
├── templates/
│   ├── index.html              # Home page template
│   ├── results.html            # Results page template
│   └── error.html              # Error page template for invalid or missing data
├── static/
│   ├── style.css               # Custom CSS for general styling
│   ├── results.css             # CSS specific to the results page
│   └── error.css               # CSS specific to the error page
├── .env                        # Environment variables (not to be committed)
├── requirements.txt            # Python dependencies
└── README.md                   # This README file
```

## Contributing

If you want to contribute to this project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or questions, feel free to reach out:

- **Email**: aelghazi6@gmail.com
- **GitHub**: [Ahmed Elghazi](https://github.com/ahmed-elghazi)
- **LinkedIn**: [Ahmed Elghazi](https://www.linkedin.com/in/ahmed-elghazi)

---
