### Step 1 - Import All the Required Libraries ###
import pandas as pd #Used to work on Dataframes
import ast #To get a literal from a string of words
from nltk.stem.porter import PorterStemmer #To remove similar words from vectors
from sklearn.feature_extraction.text import CountVectorizer #To make a Bag of Words
from sklearn.metrics.pairwise import cosine_similarity #To compute similarity between two vectors

### Step 2 - Load the Dataset ###
#The movies and credits dataset is loaded
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

### Step 3 - Data Preprocessing ###
#Merge Movies and Credits together so we can work on a single dataframe
df = movies.merge(credits, on='title')
#Our new dataframe consisting only 7 columns
updated_df = df[['id', 'title', 'keywords', 'overview', 'genres', 'cast', 'crew']]

#This line is used to turn off any warning messages from pandas
pd.set_option('mode.chained_assignment', None)
#Drop the null Columns (overview had 3 null rows)
updated_df.dropna(inplace = True)

#Some Dataset Transformations
#Convert the dictionary by extracting the names of the genre
def extractor(ob): #Function to extract only the names
    words = []
    for i in ast.literal_eval(ob):
        words.append(i['name'])
    return words
#Update the Keywords and Genre by extracting only 
updated_df['genres'] = updated_df['genres'].apply(extractor)
updated_df['keywords'] = updated_df['keywords'].apply(extractor)

#Since we have so many casts in the picture, we take only the top 10 cast of the movies
def cast_extractor(ob):
    cast = []
    count = 0
    for i in ast.literal_eval(ob):
        if count != 10:     
            cast.append(i['name'])
            count += 1
        else:
            break
    return cast
#Update the Cast Column by top 10 Casts
updated_df['cast'] = updated_df['cast'].apply(cast_extractor)

#Get only the directors of the crew, as people sometimes lean towards the director of the film
def get_director(ob):
    director = []
    for i in ast.literal_eval(ob):
        if i['job'] == 'Director':
            director.append(i['name'])
            break
    return director
        
#Update the crew column with the director only
updated_df['crew'] = updated_df['crew'].apply(get_director)

#Some splitting and spacing transformations
updated_df['overview'] = updated_df['overview'].apply(lambda x:x.split())
updated_df['genres'] = updated_df['genres'].apply(lambda x:[i.replace(" ", "") for i in x])
updated_df['keywords'] = updated_df['keywords'].apply(lambda x:[i.replace(" ", "") for i in x])
updated_df['cast'] = updated_df['cast'].apply(lambda x:[i.replace(" ", "") for i in x])
updated_df['crew'] = updated_df['crew'].apply(lambda x:[i.replace(" ", "") for i in x])
Title = updated_df['title'].str.strip('()').str.split(',')

#Add a new tag column consisting of all the columns except id
updated_df['tags'] = Title + updated_df['cast'] + updated_df['crew'] + updated_df['overview'] + updated_df['genres'] + updated_df['keywords']

#New Dataframe consisting only 3 columns, this will be helpful as we will perform bag of words and similarity...
#Only on 1 column to keep it simple
new_df = updated_df[['id', 'title',  'tags']]
#Convert the tags into a single string from multiple ones
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
#Convert the tags into lower case so that 'action' and 'Action' are not taken different
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
#End of Data Preprocessing

## Step 4 - Take the feature vectors of the tags column and remove similar meaning words ##
#This process is used to create a bag of words for each row, then with the similarity of the words in the tags from two..
#movies, the recommendation takes place through angle between the vectors in the 6900th dimension space
#Set the number of words we need in a tag, while ignoring simple english words like and, are, or, etc.
cv = CountVectorizer(max_features=4200, stop_words='english')

#Call the function from the library 
ps = PorterStemmer()

#A function to remove similar words from the tags column
def remover(text):
    final = [] 
    for i in text.split():
        final.append(ps.stem(i))
    return " ".join(final)

#Apply the function and see the results
new_df['tags'] = new_df['tags'].apply(remover)

#Assign the vectors to the newly transformed tags column
vectors = cv.fit_transform(new_df['tags']).toarray()

## Step 5 - Compute the similarity of the generated vectors ##
#Find the similarity of the vectors
similarity = cosine_similarity(vectors)

## Step 6 - Make a Movie Recommendation Function to give top 12 Movies ## 
#Function to recommend movies based on the input movie
def recommendme(movie):
    movie_index = new_df[new_df['title'] == movie].index[0] #Get the index of the input movie from the new_df and not movie id
    distances = similarity[movie_index] #Compute the similarity of this film with all the other films
    #Give the top 10 movies from reverse sorted list with highest similarity
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:13]
    #Get the titles of each indexes we enumerated to find the movie
    for i in movies_list:
        print(new_df.iloc[i[0]].title) #Print the title of the respective sr. no.
#Run the function recommendme to get Movie recommendation
recommendme("Batman v Superman: Dawn of Justice")
