import matplotlib.pyplot as plt
import income


def arr_dif_bigger(arr):
    arr_dif1 = arr[1] - arr[0]
    arr_dif2 = arr[2] - arr[1]
    if arr_dif2 > arr_dif1:
        return True
    else:
        return False


def years_to_retire(me:income.Income):
    """
    years_to_retire:
    returns: years to retire, money plot
    """
    year_list = []
    capital_arr = []
    income_arr = []
    extra_money_arr = []
    living_cost_arr = []

    for i in range(0, 60):
        future_arr = []
        future_capital = me.capital_arr[i]
        for j in range(1,4):
            future_living_cost = me.living_cost_arr[i] * pow(me.inflation, j)
            future_capital -= future_living_cost
            future_arr.append(future_capital * pow(me.capital_growth, j))

        if arr_dif_bigger(future_arr) == True:
            for j in range(0, i):
                year_list.append(j)
                capital_arr.append(me.capital_arr[j])
                income_arr.append(me.income_arr[j])
                living_cost_arr.append(me.living_cost_arr[j])
                extra_money_arr.append(me.extra_money_arr[j])
            for j in range(1, 10):
                year_list.append(i + j - 1)
                capital_arr.append(capital_arr[i+j-2] * me.capital_growth - living_cost_arr[i+j-2] * me.inflation)
                income_arr.append(0)
                living_cost_arr.append(living_cost_arr[i+j-2] * me.inflation)
                extra_money_arr.append(0)

            plt.plot(year_list, capital_arr, label="money on investment")
            plt.plot(year_list, living_cost_arr, label="annual living cost")
            plt.plot(year_list, income_arr, label="annual work income post tax")
            plt.plot(year_list, extra_money_arr, label="annual extra money (saved to bank)")
            plt.xlabel('Years')
            plt.ylabel('CAD($)')
            response_title = "you can retire after "+ str(i+1) +" year of working"
            plt.title(response_title)
            plt.legend()
            plt.show()
            return i+1
    print(-1)
    return -1


if __name__=="__main__":
    tax1_bracket_rate = [0.15, 0.205, 0.26, 0.29, 0.33, 0]
    tax1_bracket_range = [0, 50197, 100392, 155625, 211708, 0]
    tax1 = income.Tax(tax1_bracket_rate, tax1_bracket_range)
    
    my_tax_rate = 0.17

    my_salary = 79435
    my_salary_growth = 1.03
    my_save_rate = 0.2
    my_capital = 15000
    my_misc_gain = 16000
    my_capital_growth = 1.107
    my_living_cost = 33320
    my_inflation = 1.02
    me = income.Income(my_salary, my_salary_growth, my_save_rate, tax1, 
                        my_capital, my_misc_gain, my_capital_growth, 
                        my_living_cost, my_inflation)
    year = years_to_retire(me)
    