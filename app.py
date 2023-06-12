# pylint: disable=missing-function-docstring
from flask import Flask, render_template ,redirect
import sso
import dataFormat
import sys
import middleware

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


@app.route("/")
def home():
    return render_template('homepage.html')

@app.route("/start")
def start():
    return render_template('start.html')

@app.route("/PrivacyPolicy")
def privacy():
    return render_template('PrivacyPolicy.html')

@app.route("/oauth/info")
def oauthInfo():
    return render_template('OAuthInfo.html')

@app.route("/oauth/begin")
def get_begin_oauth():
    return sso.get_begin_oauth()

@app.route("/oauth/authorised")
def get_authorised_oauth():
    uuid = sso.get_authorised_oauth()
    response = redirect("/results", code=302)
    response.set_cookie( "uuid",uuid )
    return response


@app.route("/oauth/endpoint")
def get_endpoint():
    uuid = sso.get_uuid_from_cookie()
    assignments = sso.get_assignments(uuid)
    member = sso.get_user_info(uuid)
    user_submissions = sso.get_assignments(uuid)

    print("print_debug", middleware.get_data(uuid))

    assignment_names = []
    for item in assignments['enrolledAssignments']:
        assignment_names.append(item['name'])
    for item in assignments['historicAssignments']:
        assignment_names.append(item['name'])

    return render_template('assignments.html', assignments=assignment_names, member=member, submissions=user_submissions)

@app.route("/oauth/userInfo")
def get_warwick_info():
    return sso.get_warwick_info()

@app.route("/oauth/tabula/events/")
def get_upcoming_events():
    return sso.get_upcoming_events()

@app.route("/results")
def loading():
    return render_template('loading.html')

@app.route("/api/results")
def renderResults():
    try:
        uuid = sso.get_uuid_from_cookie()
    except:
        return redirect("/", code=302)
    if uuid==None:
        return redirect("/", code=302) 
    
    userData=middleware.convert_to_page(middleware.get_data(uuid))
    # try:
    #     userData=middleware.convert_to_page(middleware.get_data(uuid))
    # except:
    #     return redirect("/", code=302) 

    return render_template('Results.html',userData=userData)


# @app.route("/oauth/tabula/assignments/")
# def get_assignments(uuid):
#     return sso.get_assignments(uuid)  

if __name__ == "__main__":
    app.run(debug=True)