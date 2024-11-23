import re
import pandas as pd
from datetime import datetime
import nlu_module as mod
import query_translator as qt
import ticket_filter as tf
def load_flight_data(file_path):
        return pd.read_csv(file_path)

def handle_count_query(flights_df, user_query):
    # Step 1: Check if it's a count query
    flights_df = mod.preprocess_prices(flights_df)
    if mod.is_count_query(user_query):
        # Step 2: Extract attributes
        attributes = qt.extract_attributes(user_query)
        attributes['price_query'] = user_query  # Add the query to attributes for price extraction
        attributes['price_min'], attributes['price_max'] = mod.extract_price_conditions(user_query)
        print(attributes)    
        # Step 3: Filter the dataset based on extracted attributes
        filtered_flights = tf.filter_flights(flights_df, attributes)
        
        # Step 4: Return the count
        count = filtered_flights.shape[0]
        return f"There are {count} flights available."
    else:
        return "This doesn't seem like a count query."

def is_search_query(query):
    # Implement detection logic for search queries
    search_keywords = [
        "available flights","show all", "show me","tell me","tell all" "list","list all" "options", 
        "information on", "find flights"
    ]
    for i in search_keywords:
        if i in query.lower() :
            return True
    return False
    return any(keyword in query.lower() for keyword in search_keywords)
def handle_search_query(flights_df, user_query):
    # Check if it's a search query
    #if not is_search_query(user_query):
    #    return "This doesn't seem like a search query."
    # Initialize user attributes
    user_attributes = {
        'date': None,
        'from': None,
        'to': None,
        'airline': None,
        'price_min': 0,
        'price_max': float('inf')
    }
    attributes = mod.extract_attributes(user_query)
    user_attributes.update(attributes)
    while True:
        # Extract initial attributes from user query
        # Filter the dataset based on extracted attributes
        filtered_flights = mod.filter_flights(flights_df, user_attributes)
        # Check the count of available flights
        count = filtered_flights.shape[0]
        if count <= 25:
            print(filtered_flights)
            # Display all available flights
            #return filtered_flights
        else:
            # Prompt user for more details if count exceeds 30
            print(f"Found {count} flights. Please provide more details to refine your search.")
            add_query = input("Enter additional details or attributes: ")
            if add_query=="END BOT":
                return 
            def update_attributes(user_attributes, additional_attributes):
                for key, value in additional_attributes.items():
                    if value is not None:
                        if key == 'price_min' and value == 0:  # Don't overwrite if price_min is 0
                            continue
                        if key == 'price_max' and value == float('inf'):  # Don't overwrite if price_max is infinity
                            continue
                        user_attributes[key] = value
                return user_attributes
            additional_attributes = mod.extract_attributes(add_query)
            #print(additional_attributes)
            user_attributes = update_attributes(user_attributes, additional_attributes)
            #print(user_attributes)
            
            
# Example usage
test_queries = [
    "How many flights on 18th February from Chennai to Mumbai under 30000",
    "Total flights available on 12 Feb departing from Delhi to Mumbai below 40000",
    "Count of flights on 20-02-2022 from Chennai to Mumbai less than 30000",
    "Number of flights on 8 February departing Chennai to Mumbai at most 30000",
    "How many flights are there from Chennai to Mumbai on February 18 under 30000?",
    "Tell me the number of flights on 3 Feb from Chennai to Mumbai costing below 30000",
    "How many options for flights from Chennai to Mumbai on 18 February less than 50000?",
    "How many planes from Chennai to Delhi on 9 Feb for price equal to 30000?",
    "Available flights from Chennai to Mumbai on 23 February above 20000 but below 30000",
    "Number of flights on 10th March from Chennai to Mumbai between 10000 and 30000",  
    "Number of flights on 31st March to Hyderabad",  
    
    # Add more test cases as needed
]
flights_df = load_flight_data('business.csv')  # Assuming dataset is loaded
for query in test_queries:
    response = handle_count_query(flights_df, query)
    print(f"Query: {query}")
    print(f"Response: {response}\n")