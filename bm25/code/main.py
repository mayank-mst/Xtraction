from indexer import generator
from ranker import search

generator()
option = ""
while option != "q":
    print ("\n")
    print ("Enter search query")
    keywords = input(":: ")
    results = search(keywords)
    if results:
    	print("\nThe Matching Documents Are:")
    	for result in results:
        	print (result[0])
    else:
    	print("No Result Found.") 	