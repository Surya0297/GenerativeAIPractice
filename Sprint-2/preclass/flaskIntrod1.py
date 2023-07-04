from flask import Flask

students={}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome To First Flask App'

@app.route('/greet/<user>')
def greet(user):
    return 'Hello '+user+"!"

@app.route('/farewell/<user>')
def farewell(user):
    return 'ByeBye '+user+"!"

@app.route('/students/create/<rollno>/<name>')
def addStudent(rollno,name):
    students[int(rollno)] = name
    print(students)
    return 'Student added '+rollno+" : "+name+"!"

@app.route('/students/read/<rollno>')
def viewStudent(rollno):
    if int(rollno) in students:
        return 'Student rollno: '+rollno+" Student Name "+students[int(rollno)]+"!"
    else:
        return 'No Student with rollno:'+rollno

@app.route('/students/update/<rollno>/<name>')
def updateStudent(rollno,name):
    if int(rollno) in students:
        prevName=students[int(rollno)]
        students[int(rollno)]=name
        return 'Student name updated from: '+prevName+" to "+name+" !"
    else:
        return 'No Student with rollno:'+rollno

@app.route('/students/delete/<rollno>')
def deleteStudent(rollno):
    if int(rollno) in students:
        del students[int(rollno)]
        return 'Student with rollno: '+rollno+" deleted !"
    else:
        return 'No Student with rollno:'+rollno


if __name__ == '__main__':
    app.run()