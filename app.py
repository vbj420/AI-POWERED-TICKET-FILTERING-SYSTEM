import tkinter as tk
from tkinter import scrolledtext
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
    response_text.insert(tk.END, f"Query: {query}\n")
    if query.lower()=="help":
        
        string = """Welcome to the Flight Booking Bot Application!
This application provides a user-friendly interface for querying flight information from a dataset. You can enter queries about available flights, including specifics such as departure dates, cities, airlines, and price ranges. The bot will process your query, perform the necessary data filtering, and display the results directly within the app.
Features include:
    Count of available flights based on your query.
    Detailed search results with options to refine your search if too many results are found.
    Interactive input and output within a single, streamlined interface.
Get started by entering your flight query, and let the bot handle the rest!"""
        string  += '''This is Minuscle implementation and has higher upscaling scope. Some points to note are
Cities are limited to domestic with in India which have airport. And the data set we are supporting is from February to March 
the Airlines can be either Air India or Vistara : No Other airline will be accepted'''
        response_text.insert(tk.END, f"Count Response: {string}\n")


    count_response = handle_count_query(flights_df, query)
    response_text.insert(tk.END, f"Response: {count_response}\n")

    user_attributes = mod.extract_attributes(query)
    search_response = handle_search_query(flights_df, query, user_attributes)
    
    if "HUGE" in search_response:
        response_text.insert(tk.END, f"Response : HUGE result. Please refine your search.\n")
        while True:
            add_query = tk.simpledialog.askstring("Additional Details", "Enter additional details or attributes:")
            if add_query is None:
                break
            response_text.insert(tk.END, f"Query: {add_query}\n")     
            
            additional_attributes = mod.extract_attributes(add_query)
            user_attributes = update_attributes(user_attributes, additional_attributes)
            filtered_flights = mod.filter_flights(flights_df, user_attributes)
            count = filtered_flights.shape[0]
            if count <= 25 and count != 0:
                response_text.insert(tk.END, f"Refined Search Results:\n{filtered_flights.to_string(index=False)}\n")
                break
            response_text.insert(tk.END, f"RESPONSE : Refined count: {count}. Please refine further.\n")
    elif isinstance(search_response, pd.DataFrame):
        response_text.insert(tk.END, f"Search Results:\n{search_response.to_string(index=False)}\n")
    
    response_text.config(state=tk.DISABLED)

# Tkinter setup
root = tk.Tk()
root.title("Flight Booking Bot")

tk.Label(root, text="Enter your query:").pack(pady=10)
query_entry = tk.Entry(root, width=50)
query_entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=show_results)
search_button.pack(pady=10)

response_text = scrolledtext.ScrolledText(root, width=80, height=20, state=tk.DISABLED)
response_text.pack(pady=10)

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
