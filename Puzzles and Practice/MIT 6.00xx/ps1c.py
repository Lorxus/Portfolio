def thirtysix_months(salary: int, rate: float, returns: float, payraise: float) -> int:
    current_savings = 0
    current_month = 0
    monthly_salary = salary/12

    for i in range(36):
        current_month += 1
        current_savings += (current_savings * returns/12)
        current_savings += (monthly_salary * rate)
        if current_month % 6 == 0:
            monthly_salary *= (1 + payraise)
        # print(monthly_salary, current_savings)
    
    # print(monthly_salary, current_savings)
    return current_savings

def close_enough(a: float, b: float) -> bool:
    return abs(a-b) < 101

print('Enter your annual salary: ')
annual_salary = int(input())

total_cost = 1000000
return_rate = 0.04
portion_down_payment = 0.25
semiannual_raise = 0.07

monthly_salary = annual_salary/12
down_payment = portion_down_payment * total_cost

current_savings = 0
current_month = 0

savings_rate = 0.5
sr_lowerbound = 0
sr_upperbound = 1

found_right_rate = False
bisection_search_count = 0


if thirtysix_months(annual_salary, 1, return_rate, semiannual_raise) < down_payment:  # check whether this is possible at all
    print('It is not possible to pay the down payment in three years.')
else:  # guaranteed possible now
    while not found_right_rate:
        bisection_search_count += 1
        t = thirtysix_months(annual_salary, savings_rate, return_rate, semiannual_raise)
        if close_enough(t, down_payment):
            print('Best savings rate:', savings_rate)
            print('Bisection search count:', bisection_search_count)
            found_right_rate = True
        # too big, go lower
        elif t > down_payment:
            # print(t)
            # print(savings_rate, 'is too much!')
            sr_upperbound = savings_rate
            savings_rate = (sr_lowerbound + sr_upperbound)/2
            # print('Trying', savings_rate, '...')
        # too small, go higher
        else:
            # print(t)
            # print(savings_rate, 'is too little!')
            sr_lowerbound = savings_rate
            savings_rate = (sr_lowerbound + sr_upperbound)/2
            # print('Trying', savings_rate, '...')