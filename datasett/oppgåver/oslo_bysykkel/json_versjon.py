import json, calendar
from collections import Counter
import matplotlib.pyplot as plt

#åpner JSON-dokumentet
with open('sykkel.json', 'r') as f:
    data = json.load(f)




#Bruker lambda for funksjoner som kun trenger én linje
SORTER = lambda x: sorted(Counter(x).items(), key=lambda x: x[1], reverse=True)


#Lambda-tilnærming til return_repetitions og return_sorted_repetitions som står under
RETURN_REPETITIONS =        lambda data, keys: [data[i][_] for i in range(len(data)-1) for _ in keys]
RETURN_SORTED_REPITITIONS = lambda data, keys: SORTER(RETURN_REPETITIONS(data, keys))

"""
def return_repetitions(data, keys):
    _ = []
    for i in range(len(data)-1):
        for chosen_keys in [data[i][_] for _ in keys]:
            _.append(chosen_keys)
    return _
"""

def return_sorted_repetitions(data, keys):
    return SORTER(RETURN_REPETITIONS(data, keys))

def return_weekday(data, keys):
    _ = RETURN_REPETITIONS(data, keys)
    _ = [calendar.day_name[calendar.weekday(int(_[:4]), int(_[5:7]), int(_[8:10]))] for _ in _]
    return SORTER(_)

#Henter ut de tre mest og minst brukte stasjonene
topp_3 = return_sorted_repetitions(data, ["start_station_name"])[:3]
bunn_3 = return_sorted_repetitions(data, ["start_station_name"])[-3:]
bunn_3 = bunn_3[::-1]

#Formaterer utskrift på forskjellige måter
format_1 = lambda x, y: f"{y.index(x)+1}. Er {x[0]}, med {x[1]} turer."
format_2 = lambda x, y: f"{y.index(x)+1}. Var på {x[1]} turer, med start på {x[0]}."

valgt_format = format_1

#Utskrift
print("Topp 3:")
for _ in [valgt_format(x, topp_3) for x in topp_3]:
    print(_)

print("\nBunn 3:")
for _ in [valgt_format(x, bunn_3) for x in bunn_3]:
    print(_)

#Henter ut en touple med ukedager og antall turer
ukedager = return_weekday(data, ["started_at"])

#definerer x- og y-verdier for plotting
x_vals = [_[0] for _ in ukedager]
y_vals = [_[1] for _ in ukedager]

plt.subplot(2, 1, 1)
plt.bar(x_vals, y_vals)

plt.subplot(2,1,2)
plt.pie(y_vals, labels = x_vals, autopct='%1.1f%%')
plt.show()

