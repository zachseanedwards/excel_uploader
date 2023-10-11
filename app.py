from flask import Flask, request, render_template, send_file
import pandas as pd
from datetime import datetime
import tempfile
import os
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Create a temporary directory
            temp_dir = tempfile.TemporaryDirectory()

            try:
                # Save the uploaded file to the temporary directory
                current_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
                filename = f"{current_time}_{uploaded_file.filename}"
                file_path = os.path.join(temp_dir.name, filename)
                uploaded_file.save(file_path)

                # Read the uploaded Excel file into a Pandas DataFrame
                df = pd.read_excel(file_path)

                # Add 'output1' and 'output2' columns
                df['output1'] = df['Input'] * 10
                df['output2'] = df['Input'].astype(str) + 'a'

                # Convert the DataFrame to an Excel file in memory
                output_io = io.BytesIO()
                df.to_excel(output_io, index=False, engine='openpyxl')

                # Return the file as a response for download
                output_io.seek(0)
                return send_file(output_io, as_attachment=True, download_name=filename)
            finally:
                # Clean up the temporary directory
                temp_dir.cleanup()

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
