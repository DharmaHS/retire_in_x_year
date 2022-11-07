import matplotlib.pyplot as plt
import income


def arr_dif_bigger(arr):
    arr_dif1 = arr[1] - arr[0]
    arr_dif2 = arr[2] - arr[1]
    if arr_dif2 > arr_dif1:
        return True
    else:
        return False


def years_to_retire(annual_salary, salary_growth_rate, tax_rate,
                    annual_save_rate,
                    initial_capital, misc_gain,
                    capital_growth,
                    living_cost, inflation, rent_cost):
    """
    years_to_retire:
    returns: years to retire, money plot
    """
    capital_arr = []
    living_cost_arr = []
    income_arr = []
    extra_money_arr = []
    year_list = []

    living_cost += rent_cost

    
    current_capital = initial_capital
    for i in range(1, 60):
        year_list.append(i)

        current_salary = annual_salary * pow(salary_growth_rate, i)

        income_after_tax = current_salary * (1-tax_rate)
        income_arr.append(current_salary)
        money_saved = income_after_tax * annual_save_rate
        money_after_save = income_after_tax - money_saved
        extra_money_arr.append(money_saved)

        current_living_cost = living_cost * pow(inflation, i)
        living_cost_arr.append(current_living_cost)

        current_capital += misc_gain
        current_capital += money_after_save
        current_capital -= current_living_cost
        current_capital *= capital_growth
        capital_arr.append(current_capital)

        future_arr = []
        future_capital = current_capital
        for j in range(1,4):
            future_living_cost  = current_living_cost * pow(inflation, j)
            future_capital -= future_living_cost
            future_arr.append(future_capital * pow(capital_growth, j))

        if arr_dif_bigger(future_arr) == True:
            for j in range(1, 10):
                year_list.append(i + j)
                income_arr.append(0)
                living_cost_arr.append(living_cost_arr[i+j-2] * inflation)
                capital_arr.append(capital_arr[i+j-2] * capital_growth)
                extra_money_arr.append(0)

            print(i)
            plt.plot(year_list, capital_arr, label="money on investment")
            plt.plot(year_list, living_cost_arr, label="annual living cost")
            plt.plot(year_list, income_arr, label="annual work income post tax")
            plt.plot(year_list, extra_money_arr, label="annual extra money (saved to bank)")
            plt.xlabel('Years')
            plt.ylabel('CAD($)')
            _response_year = "you can retire after "+ str(i) +" year of working"
            plt.title(_response_year)
            plt.legend()
            plt.show()
            return i

    return -1


if __name__=="__main__":
    tax1_bracket_rate = [0.15, 0.205, 0.26, 0.29, 0.33]
    tax1_bracket_range = [50197, 100392, 155625, 211708]
    tax1 = income.Tax(tax1_bracket_rate, tax1_bracket_range)
    
    my_tax_rate = 0.17

    my_salary = 79435
    my_salary_growth = 1.03
    my_save_rate = 0.1
    my_capital = 15000
    my_misc_gain = 16000
    my_capital_growth = 1.107
    my_living_cost = 33320
    my_inflation = 1.02
    my_rent = 0
    me = income.Income(my_salary, my_salary_growth, tax1, my_save_rate, my_capital, my_misc_gain, my_capital_growth, my_living_cost, my_inflation, my_rent)
    year = years_to_retire(my_salary, my_salary_growth, my_tax_rate, my_save_rate, my_capital, my_misc_gain, my_capital_growth, my_living_cost, my_inflation, my_rent)
    