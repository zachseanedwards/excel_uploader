from flask import Flask, request, render_template, send_file
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Define the hardcoded paths for uploads and downloads directories
UPLOADS_DIR = 'C:\\Users\\zachs\\hello\\.venv\\file_uploader\\uploads'
DOWNLOADS_DIR = 'C:\\Users\\zachs\\hello\\.venv\\file_uploader\\downloads'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Generate a unique filename with the current date and time
            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
            filename = f"{current_time}_{uploaded_file.filename}"
            file_path = os.path.join(UPLOADS_DIR, filename)
            uploaded_file.save(file_path)

            # Read the uploaded Excel file into a Pandas DataFrame
            df = pd.read_excel(file_path)

            # Add 'output1' and 'output2' columns
            df['output1'] = df['Input'] * 10
            df['output2'] = df['Input'].astype(str) + 'a'

            # Save the modified DataFrame as a new Excel file in the downloads directory
            output_path = os.path.join(DOWNLOADS_DIR, filename)
            df.to_excel(output_path, index=False, engine='openpyxl')

            return send_file(output_path, as_attachment=True, download_name=filename)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
