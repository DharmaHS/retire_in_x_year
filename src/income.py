class Tax:
    rate = []
    def __init__(self, a:list, b:list):
        self.rate = a
        self.range = b

    def get_income_post_tax(self, income):
        income_post_tax = 0
        for i in range(1, 10):
            if self.rate[i] == 0:
                income_post_tax += (income - self.range[i-1]) * (1-self.rate[i-1])
                break
            if income >= self.range[i]:
                income_post_tax += (self.range[i] - self.range[i-1] ) * (1-self.rate[i-1])
                pass
            elif income < self.range[i]:
                income_post_tax += (income - self.range[i-1]) * (1-self.rate[i-1])
                break
            
        return income_post_tax

class Income:
    income_arr = []
    extra_money_arr = []
    living_cost_arr = []
    capital_arr = []

    def __init__(self, s, gr, sr, tr:Tax,
                    c, misc_g, cg,
                    lc, i):
        self.annual_salary = s
        self.salary_growth_rate = gr
        self.save_rate = sr
        self.initial_capital = c
        self.misc_gain = misc_g
        self.capital_growth = cg
        self.living_cost = lc
        self.inflation = i
        self.tax_rate = tr

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
