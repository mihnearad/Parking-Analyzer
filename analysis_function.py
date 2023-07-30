import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from config import DATABASE_CONFIG


def create_engine_from_config():
    db_string = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
    return create_engine(db_string)



def run_analysis():
  
    # Create the SQLAlchemy engine
    engine = create_engine_from_config()

    # Query to fetch the data
    query = "SELECT * FROM public.parking_data"

    # Read the data into a DataFrame
    df = pd.read_sql(query, engine)

    # Close the connection
    engine.dispose()

    # Convert the 'time' column to datetime object
    df['datetime'] = pd.to_datetime(df['time'])

    # Define the time categories
    time_categories = {
        'Morning': (7, 12),
        'Mid-Day': (12, 16),
        'Evening': (16, 21),
        'Night': (21, 7)
    }

    # Create a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    axs = axs.flatten()

    # Iterate over each time category and generate the corresponding graph
    for i, (category, (start_hour, end_hour)) in enumerate(time_categories.items()):
        # Filter the data based on the time category
        if start_hour < end_hour:
            mask = (df['datetime'].dt.hour >= start_hour) & (df['datetime'].dt.hour < end_hour)
        else:
            mask = (df['datetime'].dt.hour >= start_hour) | (df['datetime'].dt.hour < end_hour)
        df_time_category = df[mask]
    
        # Check if the DataFrame is empty
        if df_time_category.empty:
            print(f"No data available for {category}")
            continue
    
        # Count the frequency of front and back parking for each spot
        spot_parking_orientation = df_time_category.groupby(['parking_spot_id', 'parking_orientation']).size().unstack().fillna(0)

        # Stacked bar plot of parking orientation for each spot
        spot_parking_orientation.plot(kind='bar', stacked=True, ax=axs[i])
        axs[i].set_xlabel('Parking Spot')
        axs[i].set_ylabel('Frequency')
        axs[i].set_title(f'Parking Orientation for Each Parking Spot ({category})')
        axs[i].legend(title='Parking Orientation')

    # Adjust the layout and show the plot
    plt.tight_layout()
    plt.show()

def run_analysis_all_periods():



    # Create the SQLAlchemy engine
    engine = create_engine_from_config()

    # Query to fetch the data
    query = "SELECT * FROM public.parking_data"

    # Read the data into a DataFrame
    df = pd.read_sql(query, engine)

    # Close the connection
    engine.dispose()

    # Convert the 'time' column to datetime object
    df['datetime'] = pd.to_datetime(df['time'])

    # Count the frequency of front and back parking for each spot
    spot_parking_orientation = df.groupby(['parking_spot_id', 'parking_orientation']).size().unstack().fillna(0)

    # Stacked bar plot of parking orientation for each spot
    spot_parking_orientation.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.xlabel('Parking Spot')
    plt.ylabel('Frequency')
    plt.title('Parking Orientation for Each Parking Spot')
    plt.legend(title='Parking Orientation')
    plt.show()
