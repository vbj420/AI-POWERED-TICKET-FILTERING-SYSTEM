import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import pandas as pd
import modules as mod

# Load flight data
def load_flight_data(file_path):
    return pd.read_csv(file_path)

# Handle count query
def handle_count_query(flights_df, user_query):
    flights_df = mod.preprocess_prices(flights_df)
    if mod.is_count_query(user_query):
        attributes = mod.extract_attributes(user_query)
        attributes['price_query'] = user_query
        attributes['price_min'], attributes['price_max'] = mod.extract_price_conditions(user_query)
        filtered_flights = mod.filter_flights(flights_df, attributes)
        count = filtered_flights.shape[0]
        return f"There are {count} flights available."
    else:
        return "This doesn't seem like a count query."

# Handle search query
def handle_search_query(flights_df, user_query, user_attributes):
    attributes = mod.extract_attributes(user_query)
    user_attributes = update_attributes(user_attributes, attributes)
    filtered_flights = mod.filter_flights(flights_df, user_attributes)
    count = filtered_flights.shape[0]
    
    if count <= 25 and count != 0:
        return filtered_flights
    else:
        return ("HUGE", count)

# Update attributes
def update_attributes(user_attributes, additional_attributes):
    for key, value in additional_attributes.items():
        if value is not None:
            if key == 'price_min' and value == 0:
                continue
            if key == 'price_max' and value == float('inf'):
                continue
            user_attributes[key] = value
    return user_attributes

# Show results in Tkinter
def show_results():
    query = query_entry.get()
    response_text.config(state=tk.NORMAL)
    
    # Display query and response
    response_text.insert(tk.END, f"Query: {query}\n")
    if query.lower() == "help":
        help_message = """Welcome to the Flight Booking Bot Application!
This application provides a user-friendly interface for querying flight information from a dataset. You can enter queries about available flights, including specifics such as departure dates, cities, airlines, and price ranges. The bot will process your query, perform the necessary data filtering, and display the results directly within the app.
Features include:
    Count of available flights based on your query.
    Detailed search results with options to refine your search if too many results are found.
    Interactive input and output within a single, streamlined interface.
Get started by entering your flight query, and let the bot handle the rest!

This is a basic implementation with scope for future enhancement. Please note:
- Cities are limited to domestic locations within India with airports.
- The dataset covers flights from February to March.
- Supported airlines are Air India and Vistara. No other airlines are accepted."""
        response_text.insert(tk.END, f"Help Response: {help_message}\n")
    
    count_response = handle_count_query(flights_df, query)
    response_text.insert(tk.END, f"Count Response: {count_response}\n")

    user_attributes = mod.extract_attributes(query)
    search_response = handle_search_query(flights_df, query, user_attributes)
    
    if "HUGE" in search_response:
        response_text.insert(tk.END, f"HUGE result. Please refine your search.\n")
        while True:
            add_query = simpledialog.askstring("Additional Details", "Enter additional details or attributes:")
            if add_query is None:
                break
            additional_attributes = mod.extract_attributes(add_query)
            user_attributes = update_attributes(user_attributes, additional_attributes)
            filtered_flights = mod.filter_flights(flights_df, user_attributes)
            count = filtered_flights.shape[0]
            if count <= 25 and count != 0:
                messagebox.showinfo("Refined Search Results", f"Refined Search Results:\n{filtered_flights.to_string(index=False)}")
                break
            response_text.insert(tk.END, f"Refined count: {count}. Please refine further.\n")
    elif isinstance(search_response, pd.DataFrame):
        messagebox.showinfo("Search Results", f"Search Results:\n{search_response.to_string(index=False)}")
    
    response_text.config(state=tk.DISABLED)

# Tkinter setup
root = tk.Tk()
root.title("Flight Booking Bot")

# Create frames for layout
query_frame = tk.Frame(root)
query_frame.pack(side=tk.RIGHT, padx=10, pady=10)

response_frame = tk.Frame(root)
response_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

tk.Label(query_frame, text="Enter your query:").pack(pady=10)
query_entry = tk.Entry(query_frame, width=50)
query_entry.pack(pady=5)

search_button = tk.Button(query_frame, text="Search", command=show_results)
search_button.pack(pady=10)

response_text = scrolledtext.ScrolledText(response_frame, width=80, height=20, state=tk.DISABLED)
response_text.pack(pady=10, fill=tk.BOTH, expand=True)

# Load data
flights_df = load_flight_data('data/business.csv')  # Adjust path as needed
user_attributes = {
    'date': None,
    'from': None,
    'to': None,
    'airline': None,
    'price_min': 0,
    'price_max': float('inf')
}

root.mainloop()
