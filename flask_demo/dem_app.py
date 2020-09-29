from flask import Flask, render_template, request , session
from UseDatabase import UseDatabase
from checker_decorator import check_login

app = Flask(__name__)
app.config['dbconfig'] = {'host': '127.0.0.1',
             'user': 'vsearch',
             'password' : 'vsearchlogDB',
             'database' : 'vsearchlogDB'}


#
# @app.route('/')
# def hello()->str:
#     return "hello world"


# @app.route('/add3')
# def add3()->int:
#     return "6"

@app.route('/entry')
def entry()->'html':
    return render_template('entry.html', the_title='Welcome to KB')

@app.route('/search4', methods=['POST'])
def search()->'html':
    phrase = request.form['phrase']
    letters = request.form['letters']

    title = 'Here are your results: '
    result = str(set(letters).intersection(set(phrase)))
    try:
        write_log(request,result)
    except Exception as e:
        print('Observed exeception : ' + str(e))

    return render_template('results.html',
                           the_phrase = phrase,
                           the_letters=letters ,
                           the_results = result,
                           the_title = title)
def write_log(req:'flask_request', res:str)->None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        SQL= """insert into log
                (phrase, letters, ip, browser_string, results)
                values
                (%s, %s, %s, %s, %s)"""
        try:
            cursor.execute(SQL, (req.form['phrase'],
                             req.form['letters'],
                             req.remote_addr,
                             req.user_agent.browser,
                             res))
        except Exception as e :
            print('Observed error : ' + str(e))

@app.route('/viewlog')
@check_login
def viewlog()->'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        SQL = """select phrase, letters, ip, browser_string, results
                    from log"""
        cursor.execute(SQL)
        contents = cursor.fetchall()

    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    # with open('log.text', 'a') as log:
    #     print(contents,titles,file=log)

    return render_template('viewlog.html',
                               the_title='View Logs',
                               the_row_titles = titles,
                               the_data= contents,)

app.secret_key='Hello123'

@app.route('/setuser/<user>')
def setUser(user:str)->str:
    session['user']=user
    return 'User value set to : ' + session['user']
@app.route('/getuser')
def getUser()->str:
    return 'Logged in as : ' + str(session['user'])


@app.route('/login')
def login()->str:
    session['logged_in'] = True
    return 'Logged in'

@app.route('/logout')
def logout()->str:
    if 'logged_in' in session:
        session.pop('logged_in')
    return 'Logged out'

@app.route('/status')
def status()->str:
    if 'logged_in' in session:
        return 'Logged in'
    return 'Logged out'

@app.route('/page1')
@check_login
def page1():
    return 'This is Page1'

@app.route('/page2')
@check_login
def page2():
    return 'This is Page2'


if __name__=='__main__':
    app.run(debug = True)


