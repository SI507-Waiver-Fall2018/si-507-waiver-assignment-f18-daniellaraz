# these should be the only imports you need
import sys
import sqlite3
import string
# write your code here
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


conn = sqlite3.connect('Northwind_small.sqlite')
cur = conn.cursor()

if table_name == 'Customer':
    customer_names = cur.execute("SELECT CompanyName FROM %s" % (table_name))
    customer_names = customer_names.fetchall()
    print(customer_names)

elif table_name == 'Employee':
    employee_names = cur.execute("SELECT FirstName, LastName FROM %s" % (table_name))
    employee_names = employee_names.fetchall()
    print(employee_names)

else:
    employee_names = cur.execute("SELECT Id FROM Order")
    employee_names = employee_names.fetchall()
    print(employee_names)
    # if col_name == 'cust':
    #     order_date_from_customer = cur.execute("""SELECT OrderDate, CustomerId FROM Order WHERE CustomerId = ?;""", (col_value,))
    #     order_date_from_customer = order_date_from_customer.fetchall()
    #     print(order_date_from_customer)
    # else:
    #     order_dates_from_employee = cur.execute('SELECT OrderDate FROM %s WHERE EmployeeID = (SELECT Id FROM Employee WHERE LastName = %s)' %(col_value))
    #     order_dates_from_employee = order_dates_from_employee.fetchall()
    #     print(order_dates_from_employee)

conn.close()
