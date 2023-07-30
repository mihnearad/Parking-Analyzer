import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import psycopg2
import datetime
import analysis_function
from analysis_function import run_analysis_all_periods  
from config import DATABASE_CONFIG



# Function to insert data for all spots
def insert_data_all_spots():
    try:
        # Establish the connection
        conn = psycopg2.connect(database=DATABASE_CONFIG['database'], user=DATABASE_CONFIG['user'], password=DATABASE_CONFIG['password'], host=DATABASE_CONFIG['host'], port=DATABASE_CONFIG['port'])
        cur = conn.cursor()

        # Get the selected date and time
        selected_date = date_entry.get_date()
        hour = hour_var.get()
        minute = minute_var.get()
        second = second_var.get()
        current_datetime = datetime.datetime(selected_date.year, selected_date.month, selected_date.day, int(hour), int(minute), int(second))
        timestamp_value = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Loop through each parking spot and insert data
        for spot_id in range(1, 11):
            occupied_status = occupied_status_vars[spot_id].get()
            parking_orientation = parking_orientation_vars[spot_id].get()

            # Skip the spot if "n/a" option is selected
            if occupied_status == "n/a":
                continue

            # Insert data for the current parking spot
            insert_query = """
                INSERT INTO public.parking_data (date, time, parking_spot_id, occupied_status, parking_orientation)
                VALUES (%s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (current_datetime.date(), timestamp_value, spot_id, occupied_status, parking_orientation))

        # Commit the changes
        conn.commit()

        messagebox.showinfo("Data Insertion", "Data Inserted Successfully")

        # Close the cursor and connection
        cur.close()
        conn.close()
    except (Exception, psycopg2.Error) as error:
        print("Error while inserting data into the table:", error)

# Create the main window
root = tk.Tk()
root.geometry("450x820")  # Adjusted the size to fit the new widgets
root.title("Parking Data Entry")

# Date and time selection
date_time_frame = tk.Frame(root)
date_time_frame.pack(anchor="w", padx=10)

date_label = tk.Label(date_time_frame, text="Date:")
date_label.pack(side="left")

date_entry = DateEntry(date_time_frame, date_pattern='dd/mm/y')
date_entry.pack(side="left")

time_label = tk.Label(date_time_frame, text="Time:")
time_label.pack(side="left")

hour_var = tk.StringVar(root, value="00")  # Default value
hour_entry = tk.Spinbox(date_time_frame, from_=0, to=23, textvariable=hour_var, width=2)
hour_entry.pack(side="left")

minute_var = tk.StringVar(root, value="00")  # Default value
minute_entry = tk.Spinbox(date_time_frame, from_=0, to=59, textvariable=minute_var, width=2)
minute_entry.pack(side="left")

second_var = tk.StringVar(root, value="00")  # Default value
second_entry = tk.Spinbox(date_time_frame, from_=0, to=59, textvariable=second_var, width=2)
second_entry.pack(side="left")

# Create variables to store occupied status and parking orientation for each spot
occupied_status_vars = {}
parking_orientation_vars = {}



# Create input fields for each parking spot
for spot_id in range(1, 11):
    spot_frame = tk.Frame(root, relief="solid", borderwidth=1)
    spot_frame.pack(pady=10, padx=10, anchor="w")

    # Occupied status
    occupied_status_label = tk.Label(spot_frame, text=f"Parking Spot {spot_id}: Occupied")
    occupied_status_label.grid(row=0, column=0, sticky="w")

    occupied_status_var = tk.StringVar(root, value="Yes")  # Default value
    occupied_status_vars[spot_id] = occupied_status_var

    occupied_status_yes = tk.Radiobutton(spot_frame, text="Yes", variable=occupied_status_var, value="Yes")
    occupied_status_yes.grid(row=0, column=1, sticky="w")

    occupied_status_no = tk.Radiobutton(spot_frame, text="No", variable=occupied_status_var, value="No")
    occupied_status_no.grid(row=0, column=2, sticky="w")

    occupied_status_na = tk.Radiobutton(spot_frame, text="N/A", variable=occupied_status_var, value="n/a")
    occupied_status_na.grid(row=0, column=3, sticky="w")

    # Parking orientation
    parking_orientation_label = tk.Label(spot_frame, text=f"Parking Spot {spot_id}: Parking Orientation")
    parking_orientation_label.grid(row=1, column=0, sticky="w")

    parking_orientation_var = tk.StringVar(root, value="Front")  # Default value
    parking_orientation_vars[spot_id] = parking_orientation_var

    parking_orientation_front = tk.Radiobutton(spot_frame, text="Front", variable=parking_orientation_var,
                                               value="Front")
    parking_orientation_front.grid(row=1, column=1, sticky="w")

    parking_orientation_back = tk.Radiobutton(spot_frame, text="Back", variable=parking_orientation_var, value="Back")
    parking_orientation_back.grid(row=1, column=2, sticky="w")

    parking_orientation_na = tk.Radiobutton(spot_frame, text="N/A", variable=parking_orientation_var, value="N/A")
    parking_orientation_na.grid(row=1, column=3, sticky="w")

# Submit button to insert data for all spots
submit_button = tk.Button(root, text="Submit All Spots", command=insert_data_all_spots)
submit_button.pack(anchor="w", padx=10)

# Create a new button for displaying graphs for all time periods
analysis_all_periods_button = tk.Button(root, text="Show All Time Periods", command=run_analysis_all_periods)
analysis_all_periods_button.pack(anchor="w", padx=10)

# Button to run the analysis
analysis_button = tk.Button(root, text="Run Analysis per Time-Period", command=analysis_function.run_analysis)
analysis_button.pack(anchor="w", padx=10)


# Start the main loop
root.mainloop()
