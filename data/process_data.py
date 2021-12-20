import sys


def load_data(messages_filepath, categories_filepath):
    
     """
   Use the Categories Function to Load Messages Data
    
    Arguments:
        messages_filepath -> CSV Path for file containing messages
        categories_filepath -> CSV Path for file containing categories
   
    Output:
        df ->  Messages and categories combined data
    """
    
    
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.merge(messages, categories, on='id')
    return df


def clean_data(df):
    
    """
    Data Function for Clean Categories
    Arguments:
        df -> Messages and categories combined into a single file.
    Outputs:
        df -> Merged data with messages and categories that have been cleaned up.
    """
    
    categories = df['categories'].str.split(pat=';', expand=True)
    row = categories.iloc[0]
    category_colnames = row.apply(lambda x: x[:-2])
    categories.columns = category_colnames

    for column in categories:
        categories[column] = categories[column].str[-1]
        categories[column] = pd.to_numeric(categories[column])
        
    df.drop('categories', axis=1, inplace=True)
    df = pd.concat([df, categories], axis=1)
    df.drop_duplicates(subset='id', inplace=True)
    
    return df


def save_data(df, database_filename):
    
    """
    
    SQLite Database Save Data Function
    Arguments: 
    df -> Merged data with messages and categories that have been cleaned up path to SQLite destination database 
    database filename -> Path to SQLite destination database 
    
    """
    
    
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('Messages', engine, index=False)  


def main():
    
     """
    The main function that starts the data processing functions. 
        This function performs three key functions:
            1) Load Data from Messages with Categories
            2) Clean Data in Categories
            3) Save the information to a SQLite database.
    """
    
    
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()