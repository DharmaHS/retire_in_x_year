class Tax:
    rate = []
    def __init__(self, a:list, b:list):
        self.rate = a
        self.range = b

    def get_income_post_tax(self, income):
        for x in self.rate:
            #TODO: implement income tax
            pass
        return 0

class Income:
    salary_arr = []



    def __init__(self, s, gr, sr, tr:Tax,
                    c, misc_g, cg,
                    lc, i, r):
        self.annual_salary = s
        self.salary_growth_rate = gr
        self.save_rate = sr
        self.initial_capital = c
        self.misc_growth = misc_g
        self.capital_growth = cg
        self.living_cost = lc
        self.inflation = i
        self.rent = r
        self.tax_rate = tr

        for i in range(1, 60):
            current_income = self.annual_salary * pow(self.salary_growth_rate, i)
            current_income = self.tax_rate.get_income_post_tax(current_income)
            self.salary_arr
