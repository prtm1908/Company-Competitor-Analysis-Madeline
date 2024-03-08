# Company-Competitor-Analysis-Madeline

Company Competitor Analysis is a web application designed to help users analyze and compare companies within a specific industry. Users can input a company name, and the application will identify its competitors, provide detailed comparisons, and offer valuable insights. The application stores all data in a PostgreSQL database and utilizes a FastAPI backend for efficient performance.

## Setup Steps:

1. **Clone the Repository:**
   ```
   git clone https://github.com/prtm1908/Company-Competitor-Analysis-Madeline.git
   ```

2. **Navigate to the Project Directory**

3. **Create an empty folder 'static' in the Directory**

4. **Install Dependencies:**
   Make sure you have Python and pip installed on your system. Then, install the required dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

5. **Set Up PostgreSQL Database:**
   Install PostgreSQL if you haven't already. Create a new database and note down the connection details (database name, username, password) and fill them out in database.yaml file.
   
6. **Set Up Gemini:**
   Enter your Google Generative AI API key in the .env file.

7. **Run FastAPI Server:**
   Start the FastAPI server using uvicorn:
   ```
   uvicorn app:app --reload
   ```
