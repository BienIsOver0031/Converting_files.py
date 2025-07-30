hrs = input("Enter total hours per week:")
rate = input("Enter Rate:")

hrs = float(hrs)
rate = float(rate)

gross = (hrs * rate)
tax = gross * 0.23
net_pay = gross - tax

monthly_paycheck = net_pay * 4
annual_paycheck = monthly_paycheck * 12

print("Gross:" , gross)
print("⚖️Tax:" , tax)
print("💵Net Pay:" , net_pay)
print("💰Monthly paycheck:" , monthly_paycheck)
print("💰Annual_paycheck:" , annual_paycheck)