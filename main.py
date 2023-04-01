#Authors: Ghunaym Yahya and Maithili Jadhav
#Date: November 15, 2022
#Purpose: This program completes one of four operations on the MongoDB server created in Phase 1.
#Resources:

from pymongo import MongoClient
import uuid

#First we will connect to the server, which was also used in Phase 1.
port = input("port number: ")
#We must ensure that the port number entered by the user is valid. We will use a try and except to check whether or not the port number is valid.
try: 
    myclient = MongoClient("mongodb://localhost:{}/".format(port))
except:
    print("Invalid port number.") #If there was an error in the try block we will exit the program and give an Invalid port number error to the user. 
    exit()

db = myclient['291db']

def menu_options():
    '''
    Displays menu options and returns the user's selection. Also checks for the validity of the user's input.
    '''
    user_input = 0
    
    while user_input not in [1, 2, 3, 4,5]:
        print("---Select an Option---")
        print("1 - Search for Articles")
        print("2 - Search for Authors")
        print("3 - List the Venues")
        print("4 - Add an Article")
        print("5 - Exit the Program")

        user_input = input("Enter selection: ")
        print()

        try:
            user_input = int(user_input)
        except:
            print("Invalid entry.")
            print()

    return user_input

def search_for_articles():
    '''
    Prompts the user to enter in keywords and the system will retrieve all articles that match all those keywords.
    For each matching article, the id, the title, the year and the venue fields are displayed.
    The user is able to select an article to see all fields including the abstract and the authors in addition to the fields shown before.
    '''
    
    collection = db["dblp"]
    user = input("Enter one or more unique keyword: ")
    array_of_strings = user.split() # split the user input 
    search = '' 
    for string in array_of_strings:
        search += '"' + string + '"' #so words are searched indvidually as a whole
    pipeline = [{"$match": { "$text": { "$search": search}}}] 
    results = collection.aggregate(pipeline) #grouping results together
    x = 1
    for result in results:
           print("| {} | id: {} | title: {} | year: {} | venue: {} |".format(x,result['id'], result['title'], result['year'], result['venue']))
           x += 1
    print()
    user2 = input("Type the id of the article you would like to select: ") #asking user to select an article they want more info on
    id = collection.find({"id": user2}) #search the title to get the id
    x = 1
    for result in id:
        print("| {} | id: {} | title: {} | year: {} | venue: {} | abstract: {} | authors: {} |".format(x,result['id'], result['title'], result['year'], result['venue'],result['abstract'],result['authors']))
        x += 1
    print()
    references = collection.find({"references": user2}) #find the id in the reference field
    for ref in references:
        print("reference: ")
        print("|id: {} | title: {} | year: {} |".format(ref['id'], ref['title'], ref['year']))

def search_for_authors():
    '''
    Prompts the user to enter in keywords and the system will retrieve all authors whose names contain those keywords.
    For each author,the author's name and the number of publications are listed.
    The user us able to select an author and see the title, year and venue of all articles by that author. 
    The result is sorted based on year with more recent articles shown first.
    '''
    user_keyword_input = input("Enter a keyword: ") #Prompting the user to enter in a singular keyword.
    array_of_strings = user_keyword_input.split() #Here we are splitting the user input.
    while len(array_of_strings) > 1: #This while loop will ensure only one keyword was entered, otherwise the user will be prompted to enter a keyword again.
        user_keyword_input = input("You are only allowed to input one keyword, try again: ")
    collection = db["dblp"] #Collection we'll be using.
    pipeline = [{"$match": { "$text": { "$search": user_keyword_input}}},{'$unwind' : '$authors'}, #Seperating the authors.
    {'$match': {'authors': {'$regex': chr(92) + "b" + user_keyword_input + chr(92) + "b",'$options':'i'}}}, #Finding all the Author's names that match the keywords that the user inputs. The options handle case sensitivity. --> chr(92) is the '\', \bword\b allows whole words
    {'$group': { '_id':'$authors', 'Number of Publications':{'$sum': 1}}}] #Group, this will return the name of the author as well as the number of publications. Number of publications is simply the number of times the author appears, so we count those instances.
    
    results = collection.aggregate(pipeline) #Putting all the results together.
    x = 0
    for result in results: #Printing each result in a neat format.
        x += 1
        print("| {} | Name: {} | Number of Publications: {} |".format(x,result['_id'],result['Number of Publications'])) #We print the Name of the Author and the number of publications.

    user_author_selection = input("Please select an author you would like to learn more about: ") #Asking the user to select an author they want to learn more about.
    
    pipe = [{'$unwind':'$authors'}, #Seperating the Authors.
    {'$match': {'authors': { '$regex': user_author_selection,'$options':'i' } }}, #Matching the author's names with the user input.
    {'$sort' : {'year' : -1}},{"$project": {"id":0,"_id":0,"references":0,"n_citation":0}}] #Sorting by year, with the latest articles first.
   
    outputs = collection.aggregate(pipe) #Putting the results together.
    y = 1
    for output in outputs: 
        print("| {} | Name: {} | Title: {} | Year: {} | Venue: {} |".format(y,output['authors'], output['title'], output['year'], output['venue']))
        y += 1

def list_the_venues():
    '''
    The user is prompted to enter a number n, and in return is shown the listing of the top n venues.
    For each venue, the venue, the number of articles in that venue, and the number of articles that reference a paper in that venue is shown.
    The result is sorted based on the number of papers that reference the venue with the top most cited venues shown first. 
    '''
    #enter a number n
    collection = db['dblp']
    n = int(input("Enter a number: "))
    #list top n venues
    print("Top",n,"venues: ")
    venues = collection.aggregate([{"$group": {"_id": "$venue", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": n}]) #returns the number of times a venue appears in the articles
    x = 1
    for venue in venues:
        print("|{}| Venue: ".format(x),venue["_id"])
        print("Number of articles in that venue: ", venue["count"])
        x += 1
        print()

def add_an_article():
    '''
    The user is able to add an article to the collection by providing a unique id, a title, a list of authors, and a year.
    The fields abstract and venue are set to null, references are set to an empty array and n_citations are set to zero. 
    '''
        #generate new uid
    collection = db['dblp']
    valid = False
    while not valid:
        #uuid4 generates a random userID
        uid = str(uuid.uuid4())
        #print()
        if collection.find_one({"id":uid}) == None:
            valid = True
            #print(uid)

    title = input("Create a title: ")
    list_authors = []
    valid = False
    while not valid:
        auth_in = input("press Y to add author, press N to stop adding authors :").lower()
        if auth_in == 'y':
            add_auth = input("Type to add author: ")
            list_authors.append(add_auth)
            
        elif auth_in == 'n':
            break
        else:
            print("invalid input try again")

    year = input("Enter a year: ")
    collection.insert_one({"authors":list_authors,"n_citation":None,"title":title,"venue":None,"year":year,"id":uid}) 

def exit():
    '''
    This function is called when the user elects to terminate the program.
    '''
    pass

def main():
    while (1): 
        user_input = menu_options()
        if user_input == 1:
            search_for_articles()
            print()
        elif user_input == 2:
            search_for_authors()
            print()
        elif user_input == 3:
            list_the_venues()
            print()
        elif user_input == 4:
            add_an_article()
            print()
        elif user_input == 5:
            break #exit() does not exit from loop
            print()

main()