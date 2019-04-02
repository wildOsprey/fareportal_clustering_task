## Clustering task

### Data

Company provided a .csv data file (sample_searches) that includes a sample set of searches performed for flights on their websites.
Each entry row contains the user inputted search parameters (e.g., origin, destination, departure date, return date, number of passengers, etc.).
In addition to these search parameters, there are a number of additional columns with corresponding results to each search (e.g., cheapest total fare).

### Data description:

1. portal_id - unique identifier assigned to each travel portal (Cheapoair, Onetravel etc.)
searched_date - date of search
2. origin - airport source code of origin city (start point of air journey)
3. destination- airport source code of destination city (end point of air journey)
4. departure_date - date&time of departure
5. return_date date&time of the return
6. number_of_adults number of adults entered into the search query or booked in a transaction
7. number_of_children number of children entered into the search query or booked in a transaction
8. number_of_seniors number of senior entered into the search query or booked in a transaction
9. flight_class preferred class of flight journey put by customer during flight search
10. cheapest_total_fare cheapest ticket price per search
11. cheapest_engine engine which provides the cheapest tickets (GDS, SABRE etc.)
12. unique_airlines possible unique bundle of airlines which carries out a flight:
KE - one airline;
MU*AC - 2 airlines;
MU * AC ** NH - 3 airlines, etc.
13. country_code marketing affiliate country code
14. region marketing affiliate region name
15. city marketing affiliate city name

### Task 

1. Create a clustering algorithm to group or bucket the searches.
2. These groupings may be based on any of the available data columns or new features you feel necessary to generate.
3. Please briefly state the reasons for choosing your algorithm, and list any potential features you feel may be useful for model improvement.
 
