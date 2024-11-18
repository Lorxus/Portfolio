print('Enter your annual salary: ')
annual_salary = int(input())
print('Enter the portion of your salary to save, as a decimal: ')
portion_saved = float(input())
print('Enter the cost of your dream home: ')
total_cost = int(input())
print('Enter the semiannual raise, as a decimal: ')
semiannual_raise = float(input())

current_savings = 0
portion_down_payment = 0.25
return_rate = 0.04
monthly_salary = annual_salary/12
current_month = 0
down_payment = portion_down_payment * total_cost

while current_savings < down_payment:
    current_month += 1
    current_savings += current_savings * return_rate/12
    current_savings += monthly_salary * portion_saved
    if current_month % 6 == 0:
        monthly_salary *= (1 + semiannual_raise)

print('Number of months:', current_month)