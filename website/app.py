from flask import Flask, request, send_from_directory
import pandas as pd
import os
app = Flask(__name__)

@app.route('/captures/<path:filename>')
def serve_image(filename):

    captures_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "captures"
    )

    return send_from_directory(captures_path, filename)

@app.route("/")
def home():

    try:
        search = request.args.get("search", "")

        import os

        excel_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "vehicles.xlsx"
        )
        print(excel_path)

        df = pd.read_excel(excel_path)
        print(df.columns.tolist())
        print(df.head())

        if search:
            df = df[df["Vehicle\nNumber"].astype(str).str.contains(
                search,
                case=False,
                na=False
            )]

        total_vehicles = len(df)

        if total_vehicles > 0:
            last_vehicle = df.iloc[-1]["Vehicle\nNumber"]
        else:
            last_vehicle = "N/A"

        # Photo Preview
        if "Photo" in df.columns:
            df["Photo"] = df["Photo"].apply(
                lambda x: f'<img src="/{x}" width="120">'
            )

        table_html = df.to_html(
            index=False,
            classes="table",
            border=0,
            escape=False
        )

    except Exception as e:
        total_vehicles = 0
        last_vehicle = "N/A"
        table_html = f"<h3>Error: {e}</h3>"
        search = ""

    return f"""
    <html>

    <head>

        <title>Car Wash Management System</title>
        <meta http-equiv="refresh" content="30">

        <style>

        body{{
           margin:0;
           padding:30px;
           font-family:'Segoe UI',sans-serif;
           background:#0f172a;
           color:white;
         }}

         h1{{
            font-size:38px;
            margin-bottom:5px;
         }}

         h3{{
            color:#94a3b8;
            margin-bottom:25px;
         }}

         .card{{
            display:inline-block;
            background:rgba(255,255,255,0.08);
            backdrop-filter:blur(10px);
            padding:25px;
            margin:10px;
            border-radius:18px;
            min-width:250px;
            box-shadow:0 8px 25px rgba(0,0,0,0.3);
            transition:0.3s;
         }}

         .card:hover{{
            transform:translateY(-5px);
         }}

         .table{{
            width:100%;
            border-collapse:collapse;
            background:#1e293b;
            border-radius:15px;
            overflow:hidden;
         }}

         .table th{{
            background:#2563eb;
            color:white;
            padding:15px;
         }}

         .table td{{
            padding:12px;
            border-bottom:1px solid #334155;
            text-align:center;
         }}

.table tr:hover{{
    background:#334155;
}}

input{{
    padding:12px;
    width:300px;
    border:none;
    border-radius:10px;
    outline:none;
}}

button{{
    padding:12px 20px;
    border:none;
    border-radius:10px;
    background:linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );
    color:white;
    cursor:pointer;
    font-weight:bold;
}}

button:hover{{
    opacity:0.9;
}}

img{{
    width:150px;
    border-radius:12px;
    transition:0.3s;
}}

img:hover{{
    transform:scale(1.08);
}}

hr{{
    border:1px solid #334155;
}}

</style>

    </head>

    <body>

        <h1>🚗 Car Wash Management System</h1>

        <h3>Automatic Number Plate Detection & Vehicle Entry Monitoring</h3>

        <p>Welcome Danish Singh Chambial!</p>

        <hr>

        <form method="GET">
            <input
                type="text"
                name="search"
                placeholder="Search Vehicle\nNumber"
                value="{search}"
            >

            <button type="submit">
                Search
            </button>
        </form>

        <br>

        <div class="card">
            <h2>{total_vehicles}</h2>
            <p>Total Vehicles</p>
        </div>

        <div class="card">
            <h2>{last_vehicle}</h2>
            <p>Last Vehicle</p>
        </div>

        <br><br>

        <h2>Vehicle Records</h2>

        {table_html}

    </body>

    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)