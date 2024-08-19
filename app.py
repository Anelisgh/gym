from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")

# Create Supabase client
supabase: Client = create_client(url, key)

print(f"Supabase URL: {url}")
print(f"Supabase Key: {key}")


# Test query
response = supabase.from_('gym_sessions').select('*').execute()

print("Supabase response:", response)
print("Data:", response.data)
print("Count:", response.count)

@app.route('/')
def index():
    try:
        response = supabase.from_('gym_sessions').select('*').execute()
        print("Supabase response:", response)
        sessions = response.data
        print("Sessions:", sessions)  # Debug line
    except Exception as e:
        print("Error fetching data from Supabase:", e)
        sessions = []

    return render_template('index.html', sessions=sessions)
@app.route('/add', methods=['POST'])
def add_session():
    date = request.form.get('date')
    workout = request.form.get('workout')
    
    try:
        # Insert into Supabase
        response = supabase.from_('gym_sessions').insert({
            "date": date,
            "workout": workout,
        }).execute()
        
        print("Insert response:", response)
        
        return redirect(url_for('index'))
    except Exception as e:
        print("Error inserting data into Supabase:", e)
        return "An error occurred."

if __name__ == '__main__':
    app.run(debug=True)
