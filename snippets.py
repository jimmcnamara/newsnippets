import logging
import argparse
import psycopg2


logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection=psycopg2.connect(database="snippets")
logging.debug("Database connection established.")

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    with connection, connection.cursor() as cursor:
        try:
            cursor.execute("insert into snippets values (%s, %s)",(name, snippet))
        except:
            connection.rollback()
            cursor.execute("update snippets set message=%s where keyword=%s",(snippet,name))
    #cursor = connection.cursor()
    #try:
        #command = "insert into snippets values (%s, %s)"
        #cursor.execute(command, (name, snippet))
    #except psycopg2.IntegrityError as e:
        #connection.rollback()
        #command="update snippets set message=%s where keyword=%s"
        #cursor.execute(command,(snippet,name))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """Retrieve a snippet with an associated name."""
    logging.info("Getting snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s",(name,))
        answer=cursor.fetchone()
    #cursor = connection.cursor()
    #command = "select keyword, message from snippets where keyword=(%s)"
    #cursor.execute(command,(name,))
    #answer=cursor.fetchone()
    #connection.commit()
    logging.debug("Snippet retrieved successfully")
    if not answer:
        return "404: Snippet Not Found"
    return answer[0]
    
def catalog():
    logging.debug("getting all key-message pairs with")
    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets")
        allkeys=cursor.fetchall()
    logging.debug("All Keys retrieved successful")    
    return allkeys
    
def search(desc):
    newdesc='%'+desc+'%'
    logging.debug("getting all key-message pairs with {!r} in the message".format(desc))
    with connection, connection.cursor() as cursor:
        cursor.execute('select * from snippets where message like {!r}'.format(newdesc))
        matches=cursor.fetchall()
        if matches==[]:
            logging.debug("no matches in db")
            return("no possible matches")
    logging.debug("All matching keys returned succesfully")
    return matches
        
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")

    logging.debug("constructing a get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="name of the snippet")
    
    logging.debug("constructing a catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Returns all snippets")
    
    logging.debug("constructing a search subparser")
    search_parser = subparsers.add_parser("search", help ="Returns all snippets with the specified keyword")
    search_parser.add_argument("desc", help ="enter a term to search for")

    arguments = parser.parse_args()
    #convert parsed arguments from Namespace to dictionary
    arguments= vars(arguments)
    command = arguments.pop("command")

    if command=="put":
        name, snippet = put(**arguments)
        print("Stored %s as %s" %(snippet, name))
    elif command == "get":
        snippet= get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        snippet= catalog()
        print("Retrieved snippets: {!r}".format(snippet))
    elif command == "search":
        snippet= search(**arguments)
        print("Retrieved snippets: {!r}".format(snippet))
        


if __name__=="__main__":
	main()
