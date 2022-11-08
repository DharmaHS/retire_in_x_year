class Tax:
    rate = []
    def __init__(self, _tax_rate_list:list, _tax_range_list:list):
        self.rate = _tax_rate_list
        self.range = _tax_range_list

    def get_income_post_tax(self, _income):
        '''
        Param: income
        Return: income post tax
        '''
        income_post_tax = 0
        for i in range(1, 10):
            if self.rate[i] == 0:
                income_post_tax += (_income - self.range[i-1]) * (1-self.rate[i-1])
                break
            if _income >= self.range[i]:
                income_post_tax += (self.range[i] - self.range[i-1] ) * (1-self.rate[i-1])
                pass
            elif _income < self.range[i]:
                income_post_tax += (_income - self.range[i-1]) * (1-self.rate[i-1])
                break
            
        return income_post_tax

class Income:
    ''' income info.
        param: init(
            annual_salary, salary_growth_rate, save_rate, tax_rate:Tax,
            initial_capital, misc_gain, capital_growth,
            living_cost(include rent), inflation rate
        )
    '''
    income_arr = []
    extra_money_arr = []
    living_cost_arr = []
    capital_arr = []

    def __init__(self, _salary, _salary_growth_rate, _save_rate, _tax_rate:Tax,
                    _initial_capital, _misc_gain, _capital_gain,
                    _living_cost, _inflation):
        self.annual_salary = _salary
        self.salary_growth_rate = _salary_growth_rate
        self.save_rate = _save_rate
        self.initial_capital = _initial_capital
        self.misc_gain = _misc_gain
        self.capital_growth = _capital_gain
        self.living_cost = _living_cost
        self.inflation = _inflation
        self.tax_rate = _tax_rate

        current_capital = self.initial_capital
        for i in range(1, 61):
            # income after tax, with amount saved
            current_income = self.annual_salary * pow(self.salary_growth_rate, i)
            current_income = self.tax_rate.get_income_post_tax(current_income)
            self.income_arr.append(current_income)
            money_after_save = current_income - current_income * self.save_rate
            self.extra_money_arr.append(current_income * self.save_rate)
            self.living_cost_arr.append(self.living_cost * pow(self.inflation, i))
            
            # capital invest to S&P 500, living expense
            current_capital += money_after_save
            current_capital += self.misc_gain
            current_capital -= self.living_cost * pow(self.inflation, i)
            current_capital *= self.capital_growth
            self.capital_arr.append(current_capital)
