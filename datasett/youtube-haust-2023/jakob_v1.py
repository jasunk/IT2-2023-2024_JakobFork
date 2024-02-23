import json
from collections import Counter
import matplotlib.pyplot as plt
with open("youtube.json") as file:
    all_channel_data: list[dict] = json.load(file)

#Returner en sortert liste basert på forekomster av key-verdi
def sorted_by_key(key:str) -> list[tuple]:
    all_values = [value[key] for value in all_channel_data]
    counted_values = Counter(all_values)

    sorted_tuples = sorted(
        counted_values.items(),
        key = lambda x: x[1],
        reverse=True
    )
    return [data_tuple for data_tuple in sorted_tuples if data_tuple[0]!="nan"]

def return_data_from(key:str, value:str) -> list[dict]:
    channels_in_selection: list[dict] = []

    for youtubechannel in all_channel_data:
        try:
            if youtubechannel[key].lower() == value.lower(): channels_in_selection.append(youtubechannel)
        except ValueError:
            return print(f"Error: ValueError in {youtubechannel[key]}")

    return channels_in_selection

def multi_key_return(returnKey:str, valueKey:str, values:list[str]) -> list[tuple]:
    return_data: list[tuple] = []
    for value in values:
        return_data.append((value, [data_field[returnKey] for data_field in all_channel_data if data_field[valueKey]==value]))

    return return_data

def multi_key_multi_value(returnKeys:list[str], valueKey:str, values:list[str]) -> dict[list[tuple]]:
    return_data: dict[list[tuple]] = {}
    for key in returnKeys:
        return_data[key] = multi_key_return(key, valueKey, values)

    return return_data
def main() -> None:
    contries_sorted_by_country:   list[tuple] = sorted_by_key("Country")[:10]
    plt.pie([country[1] for country in contries_sorted_by_country], labels=[country[0] for country in contries_sorted_by_country])
    keys_to_search:               list[str] = [datafield[0] for datafield in contries_sorted_by_country]
    subscribers_views_by_country: dict[list[tuple]] = multi_key_multi_value(["subscribers", "video views"], "Country", keys_to_search[:10])
    print(f"Top 10 countries by channel-amount:")
    print()
    for country, channel_amount in contries_sorted_by_country[:10]:
        print(f"Nr. {contries_sorted_by_country.index((country, channel_amount))+1 :>2}: {country:>15} with {channel_amount:^5} channels.")

    for key, values in subscribers_views_by_country.items():
        print()
        print(f"Average {key} per channel:")
        for val in values:
            print(f"{val[0]:>15} has an average of {sum(val[1])//len(val[1]):^15} {key} per channel.")

    plt.show()

if __name__ == '__main__':
    main()