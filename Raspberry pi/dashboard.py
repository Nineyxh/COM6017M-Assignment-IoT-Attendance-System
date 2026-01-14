from flask import Flask, render_template_string
import csv
import os

app = Flask(__name__)

# Configuration
LOG_FILE = 'attendance_log.csv'
PORT = 8000

# HTML Template (Bootstrap 5)
HTML_TEMPLATE = 
!DOCTYPE html
html
head
    titleIoT Attendance Analyticstitle
    link href=httpscdn.jsdelivr.netnpmbootstrap@5.1.3distcssbootstrap.min.css rel=stylesheet
    meta name=viewport content=width=device-width, initial-scale=1
    meta http-equiv=refresh content=30 style
        body { background-color #f0f2f5; padding 20px; }
        .card { box-shadow 0 4px 6px rgba(0,0,0,0.1); border none; }
        .header { color #1a73e8; margin-bottom 20px; text-align center; }
    style
head
body
    div class=container
        h2 class=header📊 IoT Smart Attendance Logh2
        
        div class=card
            div class=card-body
                h5 class=card-titleReal-time Data Streamh5
                p class=text-mutedSource Local Edge Database (CSV)  Protocol HTTPp
                
                div class=table-responsive
                    table class=table table-hover
                        thead class=table-dark
                            tr
                                thTimestampth
                                thUser Identityth
                                thAccess Statusth
                            tr
                        thead
                        tbody
                            {% for row in data %}
                            tr
                                td{{ row[0] }}td
                                tdstrong{{ row[1] }}strongtd
                                tdspan class=badge bg-success{{ row[2] }}spantd
                            tr
                            {% else %}
                            trtd colspan=3 class=text-centerNo records found.tdtr
                            {% endfor %}
                        tbody
                    table
                div
                div class=mt-3 text-end
                    a href= class=btn btn-primaryRefresh Dataa
                div
            div
        div
    div
body
html


@app.route('')
def index()
    data = []
    if os.path.exists(LOG_FILE)
        try
            with open(LOG_FILE, mode='r', encoding='utf-8') as file
                reader = csv.reader(file)
                # Reverse list to show newest first
                data = list(reader)[-1]
        except Exception as e
            print(fError reading DB {e})
    return render_template_string(HTML_TEMPLATE, data=data)

if __name__ == '__main__'
    # Host on 0.0.0.0 to make it accessible via WiFi
    print(fWeb Server running on port {PORT}...)
    app.run(host='0.0.0.0', port=PORT)