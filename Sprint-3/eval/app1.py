employees=[
    {"name":"John","salary":3000,"designation":"developer"},
    {"name":"Emma","salary":4000,"designation":"manager"},
    {"name":"Kelly","salary":3500,"designation":"tester"}
    
]

def max_salary_Employee(employees):
    max =0
    ans=employees[0]
    for employee in employees:
        if(employee['salary']>max):
            max=employee['salary']
            ans=employee
    print(ans)

    

max_salary_Employee(employees)