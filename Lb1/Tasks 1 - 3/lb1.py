import requests
import matplotlib.pyplot as plt

#Завдання 1 - 3
course= requests.get("https://bank.gov.ua/NBU_Exchange/exchange_site?json&start=20251102")

course_plot = course.json()

cur_data = {}
for item in course_plot:
    date = item['exchangedate']
    rates = item['rate']
    code = item['cc']
    
    if code not in cur_data:
        cur_data[code] = {'dates': [], 'rates': []}

    cur_data[code]['dates'].append(date)
    cur_data[code]['rates'].append(rates)

wanted_cur = ['EUR', 'USD', 'GBP']

plt.figure(figsize=(12, 7))


for cur_code, data in cur_data.items():

    if cur_code not in wanted_cur:
        continue
    
    points = zip(data['dates'], data['rates'])
    sorted_points = sorted(points, key=lambda x: x[0])
    
    if sorted_points:
        sorted_dates = [point[0] for point in sorted_points]
        sorted_rates = [point[1] for point in sorted_points]
        

        plt.plot(sorted_dates, sorted_rates, marker='o', linestyle='-', label=cur_code, linewidth=2)

start_date_str = course_plot[0]['exchangedate']
plt.title(f"Динаміка курсів EUR, USD, GBP (НБУ) з {start_date_str}")
plt.xlabel("Дата")
plt.ylabel("Курс (UAH)")
plt.grid(True, linestyle='--', alpha=0.7)

plt.xticks(rotation=45, ha='right')

plt.legend(loc='best', fontsize='large')

plt.tight_layout()

plt.show()