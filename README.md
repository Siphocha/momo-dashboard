# MoMo SMS Data Processing Project

## Overview

This project is designed to process and analyze SMS data from MoMo (Mobile Money) transactions in XML format. The system provides functionalities to clean, store, retrieve, and visualize the data. The application is built using FastAPI for the backend and JavaScript for the frontend. It includes robust filtering and charting capabilities for users to explore their transactional data effectively.

## Authors
- **Ntwari Mike Chris Kevin**
- **Dushime Paulette**
- **Sipho Chakala**
- **Kayumba Blair**

## Features
- **Backend**:
  - Parses and cleans MoMo SMS XML data.
  - Stores processed data into a MySQL database.
  - Provides APIs to retrieve data using FastAPI.

- **Frontend**:
  - Dynamically displays data using JavaScript.
  - Allows filtering of transactional data based on user preferences.
  - Generates interactive charts for data visualization.

## Technologies Used

### Backend:
- **Python** (with FastAPI for API development)
- **MySQL** (for data storage)
- **XML Parsing Libraries** (for handling SMS data)

### Frontend:
- **HTML**
- **CSS**
- **JavaScript**

### Charts:
- Charting library used to display interactive visualizations (e.g., Chart.js or D3.js, if applicable)

## Installation

### Prerequisites:
- Python 3.8+
- MySQL Server
- FastApi

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/Siphocha/momo-dashboard
   cd momo-sms-project
   ```
2. Set up the backend:
   - Create a virtual environment and activate it:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Set up your MySQL database and configure the connection in the backend settings.
   - Start the FastAPI server:
     ```bash
     uvicorn main:app --reload
     ```

3. Set up the frontend:
   - Open the `index.html` file in your preferred browser.
   - Ensure the frontend is properly connected to the backend APIs.

## Usage
1. Upload your XML data to the backend via the provided endpoint or interface.
2. The backend will parse, clean, and store the data in the MySQL database.
3. Use the frontend interface to:
   - View transactional data.
   - Apply filters to retrieve specific data.
   - Visualize data using charts.

## API Endpoints
| Method | Endpoint            | Description               |
|--------|-------------------  |---------------------------|
| `GET`  | `/sms?search=`      | search any word           |
| `GET`  | `/sms?type=`        | Retrieve filtered data    |
| `GET`  | `/sms?date=`        | Retrieve filtered data    |
| `GET`  | `/sms?amount=`      | Retrieve filtered data    |

## Filtering
The frontend allows users to filter data by various criteria such as:
- Date Range
- Filter by any word
- Transaction Type
- Amount

## Charts
Interactive charts provide insights into:
- Total transactions over time.
- Distribution of transaction types.
- Monthly transaction summaries.

## Contribution
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.

---

Enjoy analyzing your MoMo SMS data with ease!
