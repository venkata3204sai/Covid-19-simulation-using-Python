import pandas as pd
import numpy as np
import sim_parameters
import helper

def create_sample_population(countries_df, specified_countries, sample_ratio):
    records = []
    person_id = 0
    for country in specified_countries:
        total_population = countries_df.loc[countries_df["country"] == country, "population"].item()
        total_sample = int(total_population / sample_ratio)
        for age_group in ["less_5", "5_to_14", "15_to_24","25_to_64", "over_65"]:
            percent_of_population = countries_df.loc[countries_df["country"] == country, age_group].item()
            number_of_sample = int(total_sample * percent_of_population / 100)
            for _ in range(number_of_sample):
                records.append((person_id, age_group, country))
                person_id+=1
    sample_population = pd.DataFrame(records, columns=["person_id", "age_group_name", "country"])
    return sample_population

def simulate(sample_population, start_date, end_date, transition_probs, holding_times):
    dates = pd.date_range(start = start_date, end = end_date)
    records = []
    for _, row in sample_population.iterrows():
        state = "H"
        staying_days = 0
        previous_state = "H"
        for date in dates:
            records.append([
                row["person_id"],
                row["age_group_name"],
                row["country"],
                date,
                state,
                staying_days,
                previous_state,
            ])
            staying_days += 1
            if staying_days >= holding_times[row["age_group_name"]][state]:
                previous_state = state
                state = np.random.choice(
                    list(transition_probs[row["age_group_name"]][state].keys()),
                    p = list(transition_probs[row["age_group_name"]][state].values())
                )
                staying_days = 0
    timeseries_data = pd.DataFrame(records, columns= list(sample_population.columns) + ["date", "state", "staying_days", "previous_state"])
    timeseries_data.to_csv("a2-covid-simulated-timeseries.csv", index = False)
    return timeseries_data

def summarise_data(timeseries_data):
    timeseries_data = timeseries_data.groupby(["date", "country", "state"]).size().reset_index(name="count")
    summarised_data = timeseries_data.pivot_table(
        index=["date", "country"],
        columns="state",
        values="count",
        fill_value=0
    ).reset_index()
    for col in ["D", "H", "I", "M", "S"]:
        if col not in summarised_data.columns:
            summarised_data[col] = 0
    summarised_data.to_csv("a2-covid-summary-timeseries.csv", index = False)
    return summarised_data

def run(countries_csv_name, countries, start_date, end_date, sample_ratio):
    countries_df = pd.read_csv(countries_csv_name)
    sample_population = create_sample_population(countries_df, countries, sample_ratio)
    timeseries_data = simulate(sample_population, start_date, end_date, sim_parameters.TRANSITION_PROBS, sim_parameters.HOLDING_TIMES)
    summarised_data = summarise_data(timeseries_data)
    helper.create_plot("a2-covid-summary-timeseries.csv", countries)