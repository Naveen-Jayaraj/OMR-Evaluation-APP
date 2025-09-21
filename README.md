# Automated OMR Sheet Grading System

A web-based application designed to automate the process of grading Optical Mark Recognition (OMR) answer sheets. This system leverages a custom-trained YOLOv8 model for accurate bubble detection and provides a clean, user-friendly interface for uploading sheets, comparing them against an answer key, and receiving an instant, detailed analysis of the results.

---

## Table of Contents

1.  [Key Features](#key-features)
2.  [Application Architecture](#application-architecture)
3.  [Technology Stack](#technology-stack)
4.  [Project Structure](#project-structure)
5.  [Setup and Installation](#setup-and-installation)
6.  [Running the Application](#running-the-application)
7.  [About the Developers](#about-the-developers)
8.  [License](#license)

---

## Key Features

* **Automated Bubble Detection:** Utilizes a YOLOv8 object detection model to accurately identify marked answers on an OMR sheet image.
* **Web-Based Interface:** A user-friendly front end built with Streamlit allows for easy uploading of OMR sheets and answer keys.
* **Automatic Grading and Scoring:** Instantly compares detected answers against the provided answer key, calculates the total score, and provides a percentage.
* **Section-wise Performance Analysis:** Parses the answer key headers to provide a subject-wise breakdown of the score, offering deeper insight into performance.
* **Decoupled Client-Server Architecture:** The backend processing and frontend interface are separated, ensuring a scalable and maintainable application structure.

---

## Application Architecture

This project is built on a client-server model to separate the intensive machine learning inference from the user interface.

* **Backend (Flask API)**
    * A lightweight web server built using Flask.
    * Its sole responsibility is to expose a single API endpoint (`/predict`).
    * This endpoint accepts an image file, processes it using the YOLOv8 model and OpenCV, performs detection sorting logic, and returns a structured JSON object containing the detected question numbers and answers.
    * It is a stateless service focused purely on model inference.

* **Frontend (Streamlit Application)**
    * A multipage web application that serves as the user interface.
    * It handles all user interactions, including file uploads for both the OMR sheet and the answer key.
    * Upon user request, it sends the OMR image to the Flask backend API.
    * After receiving the JSON response from the backend, the frontend performs all the grading logic: parsing the answer key, comparing detected answers, calculating total and section-wise scores, and displaying the final results in a structured and professional format.

This separation ensures that the machine learning model can be updated or scaled independently of the user interface.

---

## Technology Stack

* **Backend:**
    * **Framework:** Flask
    * **ML Model:** Ultralytics YOLOv8
    * **Computer Vision:** OpenCV
    * **WSGI Server:** Gunicorn
* **Frontend:**
    * **Framework:** Streamlit
    * **Data Handling:** Pandas
    * **API Communication:** Requests
* **Core Language:** Python 3

---

## Project Structure

The project is organized into the following file structure:

```
omr-grading-app/
│
├── backend.py          # Flask application for the backend API and model inference.
├── frontend.py         # Streamlit application for the user interface and grading logic.
├── requirements.txt    # A list of all Python dependencies for the project.
├── best.pt             # The trained YOLOv8 model weights file.
└── README.md           # This documentation file.
````

---

## Setup and Installation

To run this project locally, follow these steps.

**1. Clone the Repository**
```bash
git clone https://github.com/YourUsername/omr-grading-app.git
cd omr-grading-app
````

**2. Create a Virtual Environment**
It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
Install all the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**4. Place the Model File**
Ensure that your trained YOLOv8 model file, `best.pt`, is located in the root directory of the project.

-----

## Running the Application

The application requires two separate terminal sessions to run the backend and frontend servers simultaneously.

**1. Start the Backend Server**
Open a terminal, navigate to the project directory, and run the Flask application:

```bash
python backend.py
```

This will start the backend server, typically on `http://127.0.0.1:5000`.

**2. Start the Frontend Application**
Open a **second terminal**, navigate to the same project directory, and run the Streamlit application:

```bash
streamlit run frontend.py
```

This will launch the application in your default web browser, accessible at a local URL provided in the terminal. You can now interact with the application to upload files and grade OMR sheets.

-----

## About the Developers

This project was developed by:

  * **Naveen Jayaraj**

      * B.Tech CSE with AIML, 3rd Year
      * [LinkedIn Profile](https://www.linkedin.com/)

  * **Shreya Ravi K**

      * B.Tech CSE, 3rd Year
      * [LinkedIn Profile](https://www.linkedin.com/)

-----

## License

This project is licensed under the MIT License. See the LICENSE file for details.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
