from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

def load_data():
    df = pd.read_csv("student_data.csv")
    print("CSV columns:", df.columns.tolist())  # Debug line
    return df


def find_result(student_id, section):
    student_id = int(student_id)
    section = section.upper()
    students = load_data()

    result = students[(students["id"] == student_id) & (students["section"] == section)]

    if not result.empty:
        student = result.iloc[0]
        first_name = student["name"].split()[0]
        return {
            "id": student["id"],
            "name": student["name"],
            "marks": student["marks"],
            "remark": student["remark"]
        }
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        Sid = request.form["regID"]
        Ssec = request.form["regSec"]
        if not Sid.isdigit() or len(Sid) > 8:
            return render_template("index.html", message="Invalid Registration ID. It must be an integer with at most 8 digits.")
        
        if not Ssec.isalpha() or len(Ssec) != 1:
            return render_template("index.html", message="Invalid Section. It must be a single alphabet letter.")

        result = find_result(Sid, Ssec)
        if result is None:
            return render_template("index.html", message="❗ No student record found. Please check your ID and section.")
        return render_template("result.html", Tname=result["name"], Tmark=result["marks"], Tremark=result["remark"])
    return render_template("index.html", message=False)



if __name__ == "__main__":
    app.run(debug=True)
