import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image

import os
import sys

import income


def arr_dif_bigger(arr):
    '''
    Param: arr
    Return: Bool whether rate increases from 0-1 to 1-2
    '''
    arr_dif1 = arr[1] - arr[0]
    arr_dif2 = arr[2] - arr[1]
    if arr_dif2 > arr_dif1:
        return True
    else:
        return False


def years_to_retire(me:income.Income):
    '''
    Param: income.Income
    Return: years to retire, money plot
    '''
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

            fig, ax = plt.subplots()
            fig.subplots_adjust(wspace=0.6, hspace=0.6, left=0.15, bottom=0.1, right=0.85, top=0.9)
            ax.plot(year_list, capital_arr, label="money on investment")
            ax.plot(year_list, living_cost_arr, label="annual living cost")
            ax.plot(year_list, income_arr, label="annual work income post tax")
            ax.plot(year_list, extra_money_arr, label="annual extra money (saved to bank)")
            ax.ticklabel_format(style = "plain")
            ax.set_xlabel("Years")
            ax.set_ylabel("Money")
            ax.set_title("The money curve")
            return True, fig, i

    return False, None, "i"


class App(ctk.CTk):
    '''
    Main window class
    '''
    def __init__(self):
        super().__init__()

        self.var = ctk.IntVar()

        self.geometry("1200x1000")
        self.title("When can I retire? (use S&P 500)")
        self.minsize(1200, 1000)

        # create scalable grid system
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1)
        self.grid_columnconfigure((0,1,2,3,4,5), weight=1)

        # all the boxes
        self.title_label = ctk.CTkLabel(master=self, text="When can you retire?", text_font=["helvetica", 20])
        self.title_label.grid(row=0, column=1, columnspan=3)
        self.income_info_label = ctk.CTkLabel(master=self, text="Income information", text_font=["helvetica", 18])
        self.income_info_label.grid(row=1, column=0, columnspan=2)
        self.tax_info_label = ctk.CTkLabel(master=self, text="Tax information", text_font=["helvetica", 18])
        self.tax_info_label.grid(row=1, column=3, columnspan=2)

        # salary and living cost
        self.salary_label = ctk.CTkLabel(master=self, text="Salary", text_font=["helvetica", 14])
        self.salary_label.grid(row=2, column=0, padx=20)
        self.salary_box = ctk.CTkTextbox(master=self, height=16)
        self.salary_box.grid(row=2, column=1, padx=20)
        self.salary_growth_label = ctk.CTkLabel(master=self, text="Salary Growth (% per yr)", text_font=["helvetica", 14])
        self.salary_growth_label.grid(row=3, column=0, padx=20)
        self.Salary_growth_box = ctk.CTkTextbox(master=self, height=16)
        self.Salary_growth_box.grid(row=3, column=1, padx=20)
        self.save_label = ctk.CTkLabel(master=self, text="% save to bank", text_font=["helvetica", 14])
        self.save_label.grid(row=4, column=0)
        self.save_box = ctk.CTkTextbox(master=self, height=16)
        self.save_box.grid(row=4, column=1, padx=20)
        self.initial_capital_label = ctk.CTkLabel(master=self, text="Initial capital", text_font=["helvetica", 14])
        self.initial_capital_label.grid(row=5, column=0)
        self.initial_capital_box = ctk.CTkTextbox(master=self, height=16)
        self.initial_capital_box.grid(row=5, column=1, padx=20)
        self.misc_gain_label = ctk.CTkLabel(master=self, text="Annual extra money", text_font=["helvetica", 14])
        self.misc_gain_label.grid(row=6, column=0, padx=20)
        self.misc_gain_box = ctk.CTkTextbox(master=self, height=16)
        self.misc_gain_box.grid(row=6, column=1, padx=20)
        self.capital_growth_label = ctk.CTkLabel(master=self, text="Annual capital growth (~10.8%)", text_font=["helvetica", 14])
        self.capital_growth_label.grid(row=7, column=0, padx=20)
        self.capital_growth_box = ctk.CTkTextbox(master=self, height=16)
        self.capital_growth_box.grid(row=7, column=1, padx=20)
        self.living_cost_label = ctk.CTkLabel(master=self, text="Annual living cost", text_font=["helvetica", 14])
        self.living_cost_label.grid(row=8, column=0, padx=20)
        self.living_cost_box = ctk.CTkTextbox(master=self, height=16)
        self.living_cost_box.grid(row=8, column=1, padx=20)
        self.inflation_label = ctk.CTkLabel(master=self, text="Annual inflation (% per yr)", text_font=["helvetica", 14])
        self.inflation_label.grid(row=9, column=0, padx=20)
        self.inflation_box = ctk.CTkTextbox(master=self, height=16)
        self.inflation_box.grid(row=9, column=1, padx=20)

        self.divider = ctk.CTkFrame(master = self, width=80, height=16, fg_color=("#EBEBEC", "#212325"))
        self.divider.grid(row=3, column=2)

        # tax related stuff
        self.tax_rate_label = ctk.CTkLabel(master=self, text="Tax rate (%)", text_font=["helvetica", 14])
        self.tax_rate_label.grid(row=2, column=3, padx=20)
        self.tax_range_label = ctk.CTkLabel(master=self, text="Tax rate cut off range", text_font=["helvetica", 14])
        self.tax_range_label.grid(row=2, column=4, padx=20)
        self.tax_rate_1 = ctk.CTkTextbox(master=self, height=16)
        self.tax_rate_1.grid(row=3, column=3, padx=20)
        self.tax_range_1 = ctk.CTkLabel(master=self, text="0~", text_font=["helvetica", 14])
        self.tax_range_1.grid(row=3, column=4, padx=20)
        self.tax_rate_2 = ctk.CTkTextbox(master=self, height=16)
        self.tax_rate_2.grid(row=4, column=3, padx=20)
        self.tax_range_2 = ctk.CTkTextbox(master=self, height=16)
        self.tax_range_2.grid(row=4, column=4, padx=20)
        self.tax_rate_3 = ctk.CTkTextbox(master=self, height=16)
        self.tax_rate_3.grid(row=5, column=3, padx=20)
        self.tax_range_3 = ctk.CTkTextbox(master=self, height=16)
        self.tax_range_3.grid(row=5, column=4, padx=20)
        self.tax_rate_4 = ctk.CTkTextbox(master=self, height=16)
        self.tax_rate_4.grid(row=6, column=3, padx=20)
        self.tax_range_4 = ctk.CTkTextbox(master=self, height=16)
        self.tax_range_4.grid(row=6, column=4, padx=20)
        self.tax_rate_5 = ctk.CTkTextbox(master=self, height=16)
        self.tax_rate_5.grid(row=7, column=3, padx=20)
        self.tax_range_5 = ctk.CTkTextbox(master=self, height=16)
        self.tax_range_5.grid(row=7, column=4, padx=20)

        self.calculate_button = ctk.CTkButton(master=self, text="Calculate", command=self.calculate_button_event)
        self.calculate_button.grid(row=9, column=3, padx=20)

        self.protocol("WM_DELETE_WINDOW", quit)


    def check_input_valid(self, val):
        if val == "\n":
            val = "0"
        return float(val)



    def calculate_button_event(self):
        '''
        Command: calculate button
        Function: Does input check and get the retire year,
        opens a window to the result
        '''

        # get input for salary and living cost info
        my_salary = self.salary_box.get("0.0", "end")
        my_salary = self.check_input_valid(my_salary)
        my_salary_growth = self.Salary_growth_box.get("0.0", "end")
        my_salary_growth = self.check_input_valid(my_salary_growth)/100 + 1
        my_save_rate = self.save_box.get("0.0", "end")
        my_save_rate = self.check_input_valid(my_save_rate)/100
        my_capital = self.initial_capital_box.get("0.0", "end")
        my_capital = self.check_input_valid(my_capital)
        my_misc_gain = self.misc_gain_box.get("0.0", "end")
        my_misc_gain = self.check_input_valid(my_misc_gain)
        my_capital_growth = self.capital_growth_box.get("0.0", "end")
        my_capital_growth = self.check_input_valid(my_capital_growth)/100 + 1
        my_living_cost = self.living_cost_box.get("0.0", "end")
        my_living_cost = self.check_input_valid(my_living_cost)
        my_inflation = self.inflation_box.get("0.0", "end")
        my_inflation = self.check_input_valid(my_inflation)/100 + 1

        my_tax_rate = [self.tax_rate_1.get("0.0", "end"), self.tax_rate_2.get("0.0", "end"), self.tax_rate_3.get("0.0", "end"), self.tax_rate_4.get("0.0", "end"), self.tax_rate_5.get("0.0", "end")]
        my_tax_range = [0, self.tax_range_2.get("0.0", "end"), self.tax_range_3.get("0.0", "end"), self.tax_range_4.get("0.0", "end"), self.tax_range_5.get("0.0", "end")]
        for x in my_tax_rate:
            my_tax_rate[my_tax_rate.index(x)] = self.check_input_valid(x)/100
        for x in my_tax_range:
            my_tax_range[my_tax_range.index(x)] = self.check_input_valid(x)
        my_tax_rate.append(0)
        my_tax_range.append(0)

        my_tax = income.Tax(my_tax_rate, my_tax_range)
        me = income.Income(my_salary, my_salary_growth, my_save_rate, my_tax, 
                            my_capital, my_misc_gain, my_capital_growth, 
                            my_living_cost, my_inflation)

        can_retire, figure, num_of_year = years_to_retire(me)

        top = ctk.CTkToplevel()
        top.pack_propagate(False)
        top.geometry("1000x800")
        top.title("Result")
        top.grid_rowconfigure((0,1,2), weight=1)
        top.grid_columnconfigure((0), weight=1)
        result_str = "You can retire in " + str(num_of_year) + " years."   
        ctk.CTkLabel(master=top, text=result_str, text_font=["helvetica", 14]).grid(row=0, column=0)

        if can_retire:
            chart = FigureCanvasTkAgg(figure, top)
            chart.get_tk_widget().grid(row=2, column=0)
            
            additional_msg =    '''Note:
This plan works assuming a world war doesn't start
or the next economic crisis happen, and as long as
you budget stuff correctly, you're all set!
                                '''
            msg_text_box = ctk.CTkTextbox(master=top, height=130, width=400, text_font=["helvetica", 13])
            msg_text_box.grid(row=1, column=0)
            msg_text_box.insert('end', additional_msg)
            # ! ctk still developing parts of this
            # msg_text_box.config(state='disabled')

        else:
            shit_str =  '''i: imaginary, not real.
As in you don't get to retire in safety with the
salary you have and the life style you want.
Not in this economy at least.

Too bad, try changing something.
                        '''
            shit_text_box = ctk.CTkTextbox(master=top, height=130, width=360, text_font=["helvetica", 13])
            shit_text_box.grid(row=1, column=0)
            shit_text_box.insert('end', shit_str)
            # ! look at the last ! comment
            # shit_text_box.config(state='disabled')
        top.protocol("WM_DELETE_WINDOW", top.destroy)

        top.mainloop()
        

if __name__=="__main__":
    '''
    Driver function
    '''
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
