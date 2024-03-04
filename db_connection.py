#-------------------------------------------------------------------------
# AUTHOR: Joel Joshy
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import psycopg2
from psycopg2.extras import RealDictCursor
import re;

def connectDataBase():

    DB_NAME = "Assignment2"
    DB_USER = "postgres"
    DB_PASS = "1234567"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                cursor_factory=RealDictCursor)
        return conn

    except:
        print("Database not connected successfully")

    # Create a database connection object using psycopg2
    # --> add your Python code here

def createCategory(cur, id_cat, name):

    # Insert a category in the database
    # --> add your Python code here

    sql = "Insert into categories (id_cat, name) Values (%s, %s)"
    print(sql)

    recset = [id_cat, name]
    cur.execute(sql, recset)


def createDocument(cur, doc_number, doc_text, doc_title, doc_date, name):

    # 1 Get the category id based on the informed category name
    # --> add your Python code here

    cur.execute("select id_cat from categories where name = %(name)s ", {'name': name})
    recset = cur.fetchall()
    id_cat = (int(recset[0]['id_cat']))


    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here
    num_chars = 0

    for char in doc_text:
        if char not in [' ', ',', '.', '?', '!']:
            num_chars+=1

    sql = "Insert into documents (doc_number, doc_text, doc_title, doc_date, num_chars, id_cat) Values (%s, %s, %s, %s, %s, %s)"

    recset = [doc_number, doc_text, doc_title, doc_date, int(num_chars), id_cat] 
    cur.execute(sql, recset)

    # 3 Update the potential new terms
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    # --> add your Python code here
    cur.execute("select * from terms")
    recset = cur.fetchall()
    currentTerms = []
    for rec in recset:
        currentTerms.append(rec['term'])
   
    termsInDocument = []
    for term in doc_text.split(' '):
        cleanedTerm = re.sub(r'[^\w\s]', '', term.lower())
        termsInDocument.append(cleanedTerm)
        if cleanedTerm not in currentTerms:
            sql = "Insert into terms (term, num_chars) Values (%s, %s)"
            currentTerms.append(cleanedTerm)
            recset = [cleanedTerm, len(cleanedTerm)]
            cur.execute(sql, recset)
            
    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    # --> add your Python code here
    termsAndCounts = {}
    for termInDocument in termsInDocument:
        numOfTerms = 0
        for term in termsInDocument:
            if termInDocument == term:
                numOfTerms+=1
        termsAndCounts[termInDocument] = numOfTerms

    for key, value in termsAndCounts.items():
        sql = "Insert into document_terms (doc_number, term, term_count) Values (%s, %s, %s)"
        recset = [doc_number, key, value] 
        cur.execute(sql, recset)

def deleteDocument(cur, docId):

    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here
    sql = "select * from document_terms where doc_number = %(docId)s"
    cur.execute(sql, {'docId': docId})
    
    recset = cur.fetchall()

    for rec in recset:
        sql = "delete from document_terms where doc_number = %(docId)s and term=%(term)s"
        cur.execute(sql, {'docId': docId, 'term': rec['term']})
        
        sql = "select * from document_terms where term=%(term)s"
        cur.execute(sql, {'term': rec['term']})
        recset = cur.fetchall()

        print(recset)

        if len(recset) == 0:
            sql = "delete from terms where term = %(term)s"
            cur.execute(sql, {'term': rec['term']})

    # 2 Delete the document from the database
    # --> add your Python code here
    sql = "delete from documents where doc_number = %(docId)s"
    cur.execute(sql, {'docId': docId})

def updateDocument(cur, doc_number, doc_text, doc_title, doc_date, name):

    # 1 Delete the document
    # --> add your Python code here
    deleteDocument(cur, doc_number)

    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(cur, doc_number, doc_text, doc_title, doc_date, name)


def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    cur.execute("select document_terms.term, documents.doc_title, term_count from document_terms join documents on document_terms.doc_number = documents.doc_number")
    recset = cur.fetchall()
    termAndDocumentCount = {}
    for rec in recset:
        if rec['term'] in termAndDocumentCount:
            title = rec['doc_title']
            termCount = rec['term_count']
            termAndDocumentCount[rec['term']] += f", {title} : {termCount}"
        else:
            title = rec['doc_title']
            termCount = rec['term_count']
            termAndDocumentCount[rec['term']] = f"{title} : {termCount}"
    
    print(termAndDocumentCount)
        
