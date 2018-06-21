## Full Name: Daniella Raz
## Uniqname: drraz
## UMID: 86870313

import sys
import sqlite3
import string

# usage should be
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>

#command-line argument set-up
argument_list = [x for x in sys.argv if x in sys.argv[1:]]
table_name = argument_list[0]
table_name = table_name.title()[:-1]

if len(argument_list)>1:
    column_info = argument_list[1]
    col_name, col_value = column_info.split("=")

# connecting to database
conn = sqlite3.connect('Northwind_small.sqlite')
cur = conn.cursor()

# sqlite queries, and formatting to print out like in the sample output
if table_name == 'Customer':
    customer_names = cur.execute("SELECT Id, CompanyName FROM %s" % (table_name))
    customer_names = customer_names.fetchall()
    print("ID    Customer Name")
    for customer_id, customer_name in customer_names:
        print(customer_id, customer_name)

elif table_name == 'Employee':
    employee_names = cur.execute("SELECT Id, FirstName, LastName FROM %s" % (table_name))
    employee_names = employee_names.fetchall()
    print("ID   Employee Name")
    for employee_id, first_name, last_name in employee_names:
        print(employee_id, "  ", first_name, last_name)

else:
    if col_name == 'cust':
        order_date_from_customer = cur.execute("SELECT OrderDate FROM [Order] WHERE CustomerId = ?;", (col_value,))
        order_date_from_customer = order_date_from_customer.fetchall()
        print("Order dates")
        for date_tuple in order_date_from_customer:
            for date in date_tuple:
                print(date)
    else:
        order_dates_from_employee = cur.execute("SELECT OrderDate FROM [Order] WHERE EmployeeID = (SELECT Id from Employee WHERE LastName = ?)", (col_value,))
        order_dates_from_employee = order_dates_from_employee.fetchall()
        print("Order dates")
        for dates_in_tuple in order_dates_from_employee:
            for date in dates_in_tuple:
                print(date)

conn.close()
