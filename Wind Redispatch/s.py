import pandas as pd

# Load the data 
input_data = pd.read_csv('input_data.csv')

# Define
zonal_forecasts = {
    'East': 2625,
    'West': 1406.25,
    'North': 1875,
    'South': 6093.75
}

# Calculate the total state forecast or we have it as 120000
total_state_forecast = sum(zonal_forecasts.values())

# making dictionaries to store redistributed forecasts and remaining capacity
redistributed_forecasts = {}
remaining_capacity = {}

# Doing Iteration from every wind farm
for _, row in input_data.iterrows():
    wind_farm = row['Plant_Name']
    forecast = row['Forecast']
    capacity = row['Capacity']

    # Calculating  the redistribution factor 
    redistribution_factor = forecast / capacity

    # Distribute the forecast to regions/zones based on their forecasts
    # Applying all the conditions as given in assignment
    for zone, zone_forecast in zonal_forecasts.items():
        # Calculate the forecast for this wind farm in this zone
        forecast_in_zone = redistribution_factor * zone_forecast

        # Calculate the available capacity for redistribution
        available_capacity = capacity - redistributed_forecasts.get(wind_farm, 0)

        # Checking that forecast exceeds the remaining capacity
        if forecast_in_zone > available_capacity:
            forecast_in_zone = available_capacity

        # Update the redistributed 
        if wind_farm in redistributed_forecasts:
            redistributed_forecasts[wind_farm] += forecast_in_zone
        else:
            redistributed_forecasts[wind_farm] = forecast_in_zone

        # Update capacity
        remaining_capacity[wind_farm] = available_capacity

# Check if redistributed forecasts == state-level forecast
total_redistributed_forecast = sum(redistributed_forecasts.values())

# Ratio for redistributed forecasts to match the state-level forecast
for wind_farm in redistributed_forecasts:
    redistributed_forecasts[wind_farm] *= total_state_forecast / total_redistributed_forecast

# Print values(output)
for wind_farm, forecast in redistributed_forecasts.items():
    print(f'Wind Farm: {wind_farm}, Redistributed Forecast: {forecast}')

# Final checking for redistributed forecasts now match the state-level forecast
total_redistributed_forecast = sum(redistributed_forecasts.values())
print(f'Total Redistributed Forecast: {total_redistributed_forecast}')
