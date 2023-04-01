# MongoDB-Article-Library
This project is a Python-based search system that uses MongoDB to store and retrieve articles from a large database of academic publications. 
This project was split into two phases, the first phase required making a connection to the mongodb server and creating a database. 
From there we load a json file into the database. The user is required to enter a valid port number and json file, which must be in the current directory. 
The second phase required the use of mongodb queries to extract and add information from the database we created in phase 1. 
At the start of execution, the user is prompted to enter a valid port number, the same port number that was used for phase 1 to ensure connection. 
Our main program displays a selection menu that allows users to access information from a publications database that was provided to us. 
Five options are presented: (1) Search for articles, (2) Search for authors, (3) List venues, (4) Add an Article and finally (5) exit the program. 
Both Search functions return a list of results that coincide with the keyword the user has entered, from there the user can select a specific article or author and learn more about them. 
The overall flow of the program can be visualized by the flow chart that is presented at the end of the report.
