from flask import Flask, render_template_string, Response
import pandas as pd
import io
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def load_dataframe():
    # Specify the path to your file
    file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 29\v.us.txt"

    try:
        # Load the file into a Pandas DataFrame
        df = pd.read_csv(file_path, sep=",", engine="python", parse_dates=['Date'], infer_datetime_format=True)

        # Filter the DataFrame for dates within the specified range
        start_date = "2008-11-10"
        end_date = "2017-11-10"
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # Drop the "OpenInt" column if it exists
        if 'OpenInt' in df.columns:
            df = df.drop(columns=['OpenInt'])

        # Convert the DataFrame to an HTML table
        html_table = df.to_html(classes='table table-striped', index=False)

        # Render the HTML table in a simple template
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Filtered Visa Data</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container">
                <h1 class="mt-5">Filtered Visa Inc. (V) Data</h1>
                {html_table}
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template)
    except Exception as e:
        return f"An error occurred while processing the file: {e}"

@app.route('/line_chart')
def line_chart():
    file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 29\v.us.txt"
    try:
        # Load and filter the DataFrame
        df = pd.read_csv(file_path, sep=",", engine="python", parse_dates=['Date'], infer_datetime_format=True)
        df = df[(df['Date'] >= "2008-11-10") & (df['Date'] <= "2017-11-10")]
        if 'OpenInt' in df.columns:
            df = df.drop(columns=['OpenInt'])

        # Plot the data
        plt.figure(figsize=(14, 7))
        plt.plot(df['Date'], df['Open'], label='Open', color='blue')
        plt.plot(df['Date'], df['High'], label='High', color='green')
        plt.plot(df['Date'], df['Low'], label='Low', color='red')
        plt.plot(df['Date'], df['Close'], label='Close', color='orange')
        plt.title('Daily Stock Prices (2008-2017)', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price', fontsize=12)
        plt.legend()
        plt.grid(True)

        # Save plot to BytesIO
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return Response(buf, mimetype='image/png')
    except Exception as e:
        return f"An error occurred while processing the file: {e}"

if __name__ == '__main__':
    app.run(debug=True)
