import re
import re
import pandas as pd
from datetime import datetime
#import nlu_module as mod
import pandas as pd
#from nlu_module import *

  
def is_search_query(query):
    # Implement detection logic for search queries
    search_keywords = [
        "show all", "show me","tell me","tell all","list","list all","options", 
        "information on"
    ]
    #print("Yes searched query")
    for i in search_keywords:
        if i in query.lower() :
            return True
    return False
    #return any(keyword in query.lower() for keyword in search_keywords)
# Function to check if the query is a count query
def filter_flights(flights_df, features):
    # Prepare query conditions
    query_conditions = []
    # Add conditions based on features
    if features.get('date'):
        query_conditions.append(f"`date` == '{features['date']}'")
    if features.get('airline'):
        query_conditions.append(f"`airline` == '{features['airline']}'")
    if features.get('from'):
        query_conditions.append(f"`from` == '{features['from']}'")
    if features.get('to'):
        query_conditions.append(f"`to` == '{features['to']}'")
    flights_df['price'] = pd.to_numeric(flights_df['price'], errors='coerce')
    # Handle price range conditions
    if features.get('price_min') is not None and features.get('price_max') is not None:
        query_conditions.append(f"`price` >= {features['price_min']} & `price` <= {features['price_max']}")
    elif features.get('price_min') is not None:
        query_conditions.append(f"`price` >= {features['price_min']}")
    elif features.get('price_max') is not None:
        query_conditions.append(f"`price` <= {features['price_max']}")
    # Join all conditions to form the query string
    if query_conditions:
        query = " & ".join(query_conditions)
    else:
        query = "True"
    # Apply the query and handle exceptions
    try:
        filtered_flights = flights_df.query(query)
        columns_of_interest = ['date', 'num_code', 'dep_time', 'arr_time', 'from', 'to', 'airline', 'price']
        filtered_flights = filtered_flights[columns_of_interest]

        return filtered_flights
    except Exception as e:
        print(f"Error applying query: {e}")
        return pd.DataFrame()
 
count_patterns = [
    r"how many flights", r"number of flights", r"total flights", 
    r"can you tell me the number", r"number of planes", r"how many options", 
    r"how many departures", r"tell me the available flights",
    r"available flights", r"total flights count", r"count of flights",
    r"flight count"
]
synonym_map = {
    'flights': [
        'aeroplanes', 'aircrafts', 'airflights', 'planes', 
        'airliners', 'jetliners', 'flight options', 'flight schedules'
    ],
    'options': [
        'choices', 'alternatives', 'selections', 'possibilities', 
        'varieties'
    ],
    'departures': [
        'departures', 'leavings', 'outgoings'
    ],
    'from': [
        'departure from', 'starting point', 'origin', 'departing from'
    ],
    'to': [
        'destination', 'arriving at', 'going to', 'traveling to' ,"destination is" ,"destination at"
    ],
    "Bangalore" :["Banglore","Bengaluru","Bangaluru","Bengalore","Bngalore"],
    "Hyderabad" :["Hydrebad","Hydrabad","Hyderbad","Hderabad"],
    "Delhi" : ["New Delhi","Dehli","Dilli","Dillhi","Delhii"],
    "Chennai" :["Chenai","Madras","Channai"],
    "Kolkata" :["Calcut","Calcutta","Kolkota","Kolkatha"],
    "Mumbai":["Bombay","Bombai","Mombai","Mumbay","Mumbaai"],
    "under":["below","less than","under the limit","at most"],
    "equal to" :["equivalent to","exactly"],
    "above":["at least","higher than","more than","greater than"]

}

def replace_synonyms(query, synonym_map):
    # Ensure query is a string; if it's a dictionary, extract the relevant part
    if isinstance(query, dict):
        query = query.get('query', '')  # Extract the query part or default to an empty string
    
    # Proceed with synonym replacement
    for internal_term, synonyms in synonym_map.items():
        for synonym in synonyms:
            query = re.sub(rf'\b{re.escape(synonym)}\b', internal_term, query, flags=re.IGNORECASE)
    
    return query

def match_internal_patterns(query, internal_patterns):
    # Dictionary to store matched attributes
    attributes = {
        'from': None,
        'to': None,
        'date': None,
        'airline': None,
        'price_min': None,
        'price_max': None
    }

    # Iterate over patterns and find matches for 'from', 'to', etc.
    for attr, patterns in internal_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                if attr in ['from', 'to']:  # Extract city for 'from' and 'to'
                    attributes[attr] = match.group(1).strip()  # Get the matched city
                else:
                    # For non-city attributes like 'airline' or 'date', flag them as matched
                    attributes[attr] = True

    return attributes
def extract_attributes(user_query):
    user_query = replace_synonyms(user_query, synonym_map)   
    #print(user_query)
    # Match query against internal patterns

    attributes = {
        'date': None,
        'from': None,
        'to': None,
        'airline': None,
        'price_min': None,
        'price_max': None
    }
    valid_cities = ['Chennai', 'Mumbai', 'Hyderabad', 'Delhi', 'Kolkata', 'Bangalore']

    # Regex patterns
    from_pattern = r'(?i)\bfrom\s+(\w+)\b'
    to_pattern = r'(?i)\bto\s+(\w+)\b'
    # Patterns to extract 'from' and 'to' locations
    #from_pattern = r'(?i)\b(?:from|leaving from|departing from)\s+([A-Za-z]+)\b'
    #to_pattern = r'(?i)\b(?:to|towards)\s+([A-Za-z]+)\b'
    
    # Date patterns
    date_patterns = [
        r'(?i)\b(\d{1,2}(?:st|nd|rd|th)? (?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?: \d{4})?)\b',
        r'(?i)\b(\d{1,2} (?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?: \d{4})?)\b',
        r'(?i)\b(\d{1,2}[-/](?:0[1-9]|1[0-2])[-/](?:\d{2}|\d{4}))\b',
        r'(?i)\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) \d{1,2}\b',
        r'(?i)\b(\d{1,2}(?:st|nd|rd|th)? of (?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?: \d{4})?)\b',
        r'(?i)\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?) \d{1,2}(?:st|nd|rd|th)?\b'
    ]

    # Extract date
    for pattern in date_patterns:
        date_match = re.search(pattern, user_query)
        if date_match:
            date_str = date_match.group(0)
            normalized_date = normalize_date(date_str)
            if normalized_date:
                attributes['date'] = normalized_date
                break

    # Extract 'from' location
    from_match = re.search(from_pattern, user_query)
    if from_match:
        closest_city = from_match.group(1).capitalize()
        attributes['from'] = closest_city
        
    # Extract 'to' location
    # Extract 'to' location
    to_match = re.search(to_pattern, user_query)
    if to_match:
        city = to_match.group(1).capitalize()
        attributes['to'] = city
        
    # Extract airline
    known_airlines = ['Vistara', 'Air India']  # Add more airlines as needed
    for airline in known_airlines:
        if airline.lower() in user_query.lower():
            attributes['airline'] = airline

    # Extract price conditions
    price_conditions = {
        'under': '<=',
        'below': '<=',
        'less than': '<',
        'equal to': '==',
        'greater than': '>',
        'more than': '>',
        'at least': '>=',
        'more than or equal to': '>='
    }

    for condition in price_conditions:
        price_match = re.search(rf'{condition}\s*(\d+)', user_query, re.IGNORECASE)
        if price_match:
            price_value = int(price_match.group(1))
            if condition in ['under', 'below', 'less than']:
                attributes['price_max'] = price_value
                attributes['price_min'] = 0
            elif condition in ['greater than', 'more than', 'at least']:
                attributes['price_min'] = price_value
                attributes['price_max'] = float('inf')
            elif condition == 'equal to':
                attributes['price_min'] = price_value
                attributes['price_max'] = price_value

    # Default price range if not set
    if attributes['price_min'] is None:
        attributes['price_min'] = 0
    if attributes['price_max'] is None:
        attributes['price_max'] = float('inf')

    return attributes

def is_count_query(user_query):
    # Normalize the user query
    normalized_query = normalize_query(user_query, synonym_map)
    
    # Check if it matches any count pattern
    normalized_query = normalized_query.lower()  # Ensure case insensitivity
    for pattern in count_patterns:
        if re.search(pattern, normalized_query):
            return True
    return False
count_patterns = [
    r"how many flights", r"number of flights", r"total flights", 
    r"can you tell me the number", r"number of planes", r"how many options", 
    r"how many departures", r"tell me the available flights",
    r"available flights", r"total flights count", r"count of flights",
    r"flight count"
]

from math import inf
def preprocess_prices(df):
    # Remove commas from the 'price' column and convert to integer
    df['price'] = df['price'].replace(',', '', regex=True).astype(int)
    #print(df)
    return df

def extract_price_conditions(query):
    # Initialize default values
    price_min = 0
    price_max = inf

    # Regex patterns for price extraction
    price_patterns = {
        'between': r'\b(?:between|from)\s*(\d+)\s*(?:and|to)\s*(\d+)\b',
        'above_below': r'\b(?:above|greater than)\s*(\d+)\s*(?:but\s*below|and\s*less than)\s*(\d+)\b',
        'greater_less': r'\b(?:greater than|more than)\s*(\d+)\s*(?:but\s*less than|and\s*below)\s*(\d+)\b',
        'under': r'\b(?:under|below|at most|up to|less than)\s*(\d+)\b',
        'above': r'\b(?:above|greater than|more than)\s*(\d+)\b',
        'exactly': r'\b(?:exactly|equal to)\s*(\d+)\b'
    }
    # Search for patterns in the query
    for key, pattern in price_patterns.items():
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            if key == 'under':
                price_max = int(match.group(1))
            elif key == 'between':
                price_min = int(match.group(1))
                price_max = int(match.group(2))
            elif key in ['above_below', 'greater_less']:
                price_min = int(match.group(1))
                price_max = int(match.group(2))
            elif key == 'above':
                price_min = int(match.group(1))
                price_max = inf
            elif key == 'exactly':
                price_min = int(match.group(1))
                price_max = int(match.group(1))
            break

    return price_min, price_max
def normalize_query(query, synonym_map):
    # Ensure query is a string, if it's a dict, convert or extract the relevant field
    if isinstance(query, dict):
        query = query.get('query', '')  # Extract the query part if it's stored in a 'query' key, or default to an empty string
    
    # Proceed with string normalization
    query = query.lower()
    
    for standard_term, synonyms in synonym_map.items():
        for synonym in synonyms:
            # Replace synonyms with the standard term
            if synonym in query:
                query = re.sub(r'\b{}\b'.format(re.escape(synonym)), standard_term, query)
    
    return query

# Define known airlines
known_airlines = ['Air India', 'Vistara']

# Define city names for normalization
city_names = ['Chennai', 'Mumbai', 'Delhi',"Kolkata","Bangalore","Hyderabad"]

# Function to normalize city names
def normalize_city(city_name):
    # Normalize city name by capitalizing the first letter
    city_name = city_name.title().strip()
    if city_name in city_names:
        return city_name
    return None

def normalize_date(date_str):
    # Set default year
    default_year = 2022
    
    # Define month names and their abbreviations
    month_names = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12,
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5,
        'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10,
        'nov': 11, 'dec': 12
    }

    # Remove ordinal suffixes
    date_str = re.sub(r'(\d+)(?:st|nd|rd|th)', r'\1', date_str, flags=re.IGNORECASE)
    
    # Handle month before day (e.g., February 12)
    month_names_lower = {k.lower(): v for k, v in month_names.items()}
    for month_str, month_number in month_names_lower.items():
        pattern = re.compile(rf'({month_str})(?:\s+|\s*)(\d{{1,2}})', re.IGNORECASE)
        match = pattern.search(date_str)
        if match:
            month = str(month_number).zfill(2)
            day = match.group(2).zfill(2)
            return f'{day}-{month}-{default_year}'

    # Handle direct month and day concatenated formats
    for month_name, month_number in month_names.items():
        pattern = re.compile(rf'(\d{{1,2}})(?:\s*{month_name}|{month_name})(?!\d)', re.IGNORECASE)
        match = pattern.search(date_str)
        if match:
            day = match.group(1).zfill(2)
            month = str(month_number).zfill(2)
            return f'{day}-{month}-{default_year}'

    # Handle month and day with separators or spaces
    date_str = re.sub(
        r'(\d{1,2})\s*(?:[-/.,\s]*\s*|(?:of\s*)?)(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)',
        r'\1 \2',
        date_str,
        flags=re.IGNORECASE
    )

    # Match the date pattern with month names
    match = re.search(r'(\d{1,2})\s*(\w+)', date_str, re.IGNORECASE)
    if match:
        day = match.group(1).zfill(2)
        month_str = match.group(2).lower()
        month = month_names_lower.get(month_str)
        if month:
            return f'{day}-{str(month).zfill(2)}-{default_year}'

    # Handle numerical month/day formats like "12/02" or "12-02"
    match = re.search(r'(\d{1,2})\s*[-/]\s*(\d{1,2})', date_str)
    if match:
        day = match.group(1).zfill(2)
        month = match.group(2).zfill(2)
        return f'{day}-{month}-{default_year}'

    # Handle formats with dots and year in different positions
    match = re.search(r'(\d{1,2})[./-](\d{1,2})(?:[./-](\d{4}))?', date_str)
    if match:
        day = match.group(1).zfill(2)
        month = match.group(2).zfill(2)
        year = match.group(3) if match.group(3) else default_year
        return f'{day}-{month}-{year}'

    return None

