# AI-POWERED-TICKET-FILTERING-SYSTEM
An AI-driven solution that allows users to filter and retrieve tickets based on natural language queries. This system interprets and translates user inputs into technical filter criteria, providing an intuitive, user-friendly interface for effective ticket management.

A simple and interactive bot that is built upon the basics of NLP. Although not used any linked LLM , This bot analyzes the structure and content of the query entered by the user and identifies whether it is a valid query related to our Ticket-Management and identifies the given attributes and the required from the query input.

![image](https://github.com/user-attachments/assets/cf31d875-0b8b-4698-96a8-ebce62c87d2a)


METHODOLOGIES:
1.	Natural Language Processing
2.	Synonym Mapping
3.	Query Parsing and Attribute Extraction
4.	Data Filtering
5.	Feedback Mechanism using Caching

![image](https://github.com/user-attachments/assets/bc6cd9a5-3cda-42f5-aa4a-cb67746fcd2e)


DATASET:
The dataset contains information about flight booking options for flight travel between India's top 6 metro cities. There are 300261 data points and 11 features in the cleaned dataset.
WORK-FLOW:
  FRONT-END:
  Used the Tkinter library to build a graphical interface for querying flight information from a dataset. It allows users to input flight-related queries, filter results based on various attributes, and display them  
  directly in the interface.
  This processes queries for both counting available flights and searching for flight details. Additionally offers guidance and a way to refine broad searches.
  
  STRUCTURE AND LOGIC BEHIND:
  The modules.py file seems to play a critical role in supporting the core functionality of the main application (app.py).It contains helper functions designed to extract,process,and filter user-provided information.
  Attribute Extraction from User Queries:
  This responsible for extracting structured information from unstructured user input (such as natural language queries). This extraction might rely on keyword matching or more sophisticated natural language processing   (NLP) techniques. The module could use regular expressions or a custom NLP parser

Handling Price Ranges:
Parsing user input to identify specific price constraints.Creating lower and upper bounds for price filtering (e.g., price_min, price_max).Returning structured information that can be used by the main filtering function in app.py.
The helper function extracts various attributes from the query, including:
•	Departure and arrival locations (e.g., from Chennai, to Mumbai)
•	Travel date (e.g., date: 2024-02-18)
•	Price constraints (e.g., price_max: 30,000)
In app.py, the filtering logic uses the extracted price_min and price_max values to apply constraints to the flight dataset (flights_df), ensuring only flights within the specified price range are returned.

![image](https://github.com/user-attachments/assets/493ce9c4-28d0-419a-beb6-b1a9dcddc5ef)


Synonym Mapping(modules.py):
In natural language, users can express the same intent in multiple ways using synonyms. For instance:
•	"Show flights" can be expressed as "List flights", or "Display flights".
•	"Price below 30,000" can also be expressed as "less than 30,000", "under 30,000", or "maximum 30,000".
•	Chennai and Mumbai can be written as Madras or Bombay
modules.py helps map these synonyms to a consistent internal representation that app.py can understand. It may use simple string matching, regular expressions, or a predefined synonym dictionary to achieve this

![image](https://github.com/user-attachments/assets/a7ca96a7-3e29-412e-9b26-9add9a0e21ad)

 
Feedback Mechanism using Caching:
Using a feedback mechanism with caching for effective ticket filtering is a smart way to optimize both the user experience and system performance. In this approach, caching helps to store the results of user queries, and the feedback mechanism guides the user to refine or adjust their queries based on cached data. Let me explain how this combination works in the context of your ticket filtering system.
•	The number of flights that match the user’s criteria.
•	Suggestions to modify the query if no flights are found or if the criteria are too restrictive.
•	Cached results allow for faster responses, improving the overall user experience by reducing the delay caused by repetitive queries.
Query: Count of planes on March 5 from Chennai to Delhi price with less that 40000.
 
![image](https://github.com/user-attachments/assets/01bac71e-afde-48bb-bce6-ad4111b46b8b)

![image](https://github.com/user-attachments/assets/8c7c95dc-c2f0-4d3a-b3b4-c7e87ae75df1)

