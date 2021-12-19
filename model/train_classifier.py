"""

   Disaster Response Pipeline: 
    Classifier Trainer Project 
        > python train_classifier.py <path to sqllite  destination db> <path to the pickle file>
    
    Sample Script Execution:
        > python train_classifier.py ../data/InsertDatabaseName.db classifier.pkl
    
    Arguments:
        1) SQLite destination database path (e.g. dInsertDatabaseName.db) 
        2) Pickle file name where ML model should be saved (e.g. classifier.pkl)
"""


import sys


def load_data(database_filepath):
       
    """ 
    
    Function to Load Data from a Database

    Arguments:
        database filepath -> SQLite target database path (for example, InsertDatabaseName.db)
        X -> a dataframe with features as output
        Y->  Labels are stored in a dataframe.
        category names -> is a list of categories 

"""
    
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql_table('DisasterMessages', engine)
    X = df['message']
    Y = df.iloc[:, 4:]
    category_names = list(df.columns[4:])
    return X, Y, category_names


def tokenize(text):
    
    """
    Tokenize the text function
    
    Arguments:
        text -> A text message that must be tokenized
    
    Output:
        clean_tokens -> A list of tokens retrieved from the supplied text 
    
    """
    
    text = re.sub(r"[^a-zA-Z0-9]", ' ', text.lower())
    
    words = word_tokenize(text)
   
    words = [w for w in words if w not in stopwords.words('english')]
  
    lemmatizer = WordNetLemmatizer()
    
    lem = [lemmatizer.lemmatize(w, pos='n').strip() for w in words]
    
    lem = [lemmatizer.lemmatize(w, pos='v').strip() for w in lem]

    return lem


def build_model():
    
    """
    
    Build Pipeline is a function that allows you to create a pipeline.

    A Scikit-ML Pipeline that processes text messages and applies a classifier as an output.

    """
    
    pipeline = Pipeline([
                        ('vect', CountVectorizer(tokenizer=tokenize)),
                        ('tfidf', TfidfTransformer()),
                        ('clf', MultiOutputClassifier(RandomForestClassifier()))
                        ])

    parameters = {'clf__estimator__n_estimators': [50, 100],
                  'clf__estimator__min_samples_split': [2, 3, 4],
                  'clf__estimator__criterion': ['entropy', 'gini']
                 }
    
    cv = GridSearchCV(pipeline, param_grid=parameters)
    
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    
    """
    Displays the model's performance on test data.

    Arguments: 
        model: trained model 
        X_test: feature testing 
        Y_test: target testing  
        category_names: target labels
"""
    
    Y_pred = model.predict(X_test)
        
    for i in range(len(category_names)):
        print("Cat:", category_names[i],"\n", classification_report(Y_test.iloc[:, i].values, Y_pred[:, i]))
        print('Accuracy of %25s: %.2f' %(category_names[i], accuracy_score(Y_test.iloc[:, i].values, Y_pred[:,i])))


def save_model(model, model_filepath):
    
    """
    Saves the model to a Python pickle file  
    
   Arguments: 
        model: trained model
        model_filepath: path to save model

    """
    
    pickle.dump(model, open(model_filepath, "wb"))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
