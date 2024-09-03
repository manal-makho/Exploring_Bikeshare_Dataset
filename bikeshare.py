##### Manal Abo Makho


import time
import pandas as pd
import traceback 
##Scaning the data
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def entery_validation(input_message, valid_inputs, invalid_messgae):
    """
    Function that verifies the user input and if there was a problem it returns a prompt
    Args:
        (str) input_message - the message displayed to ask the user of input
        (list) valid_inputs - a list of enteries that are valid
        (str) invalid_messgae - a message to be displayed if the input is invalid
    Returns:
        (str) input - returns the input when it's valid
    """
     
    while True:
        input_value = str(input("\n"+ input_message +"\n"))
        input_value = input_value.lower()
        if input_value not in valid_inputs:
            print(invalid_messgae)
            continue
        else:
            break
    return input_value


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    
    """ City input """
    city_input_message = "Which City would like to explore? All, Chicago, New york city, Or Washington?"
    city_invalid_message = "Try to enter another city that is either: Chicago, New york city, Or Washington "
    city_valid_enteries = ('all','new york city', 'chicago', 'washington')
    # get user input for city (chicago, new york city, washington). 
    city = entery_validation(city_input_message, city_valid_enteries,city_invalid_message)

    """ Month input """
    month_input_message = "In which of the months you want to explore? is it (all, january, february, ... , june)"
    month_invalid_message = "Try to enter the month again, it wasn't a valid month!"
    month_valid_enteries = ('all','january','february','march','april','may','june','july','august','september','october','november','december')
    # get user input for month (all, january, february, ... , june)
    month = entery_validation(month_input_message, month_valid_enteries, month_invalid_message)

    """ Day input """
    day_input_messgae = "What about the day you are looking for? is it (all, monday, tuesday, ... sunday)?"
    day_inavlid_message = "You entered a not valid day, try again"
    day_valid_enteries = ('sunday','monday','all','tuesday','wednesday','thursday','friday','saturday')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = entery_validation(day_input_messgae, day_valid_enteries, day_inavlid_message)

    print('-'*40)
    return city, month, day

# in this method load the dataset based on which city the user inputs 
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    if city != 'all':
        df = pd.read_csv(CITY_DATA[city])
    else:
        dfs = []
        for city, path in CITY_DATA.items(all):
            dfC = pd.read_csv(path)
            dfs.append(dfC)
        
        df = pd.concat(dfs, ignore_index=True)
    return df

## this metohd I created to clean the data 
def clean_data(df, city):
    """
    Args:
        (pandas dataframe) df - takes a data frame with missing data probabloy and with not proper datatypes probably
        (city) df - because in the case of washington some coulmns doesn't exists
    Returns:
        (pandas dataframe) df - imputed with unknown and date handled
    """
    df = handle_dates(df, city)
    df = handle_missing(df)
    return df

# this method I created to handle the missing data
def handle_missing(df):
    df.drop(df.columns[0], axis = 1, inplace=True)
    print('We have {} missing enteries'.format(df.isnull().sum().sum()) )
    df.fillna('Unknown', inplace=True)
    print('These were filled by (Unknown) ')
    return df

## this method I created to handle the dates
def handle_dates(df, city):
    """
    Handle the dates as their datatypes using to_datetime pandas
    """
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

  
    df['start_month'] = df['Start Time'].dt.strftime('%B').str.lower()
    df['start_day'] = df['Start Time'].dt.strftime('%A').str.lower()
    df['start_year'] = df['Start Time'].dt.strftime('%Y')
    df['start_time'] = df['Start Time'].dt.strftime('%X')
    
    df['end_month'] = df['End Time'].dt.strftime('%B').str.lower()
    df['end_day'] = df['End Time'].dt.strftime('%A').str.lower()
    df['end_year'] = df['End Time'].dt.strftime('%Y')
    df['end_time'] = df['End Time'].dt.strftime('%X')
    
    if city in ('new york city', 'chicago'):
        df['Birth Year'] = pd.to_datetime(df['Birth Year'])
        df['Birth Year'] = pd.to_numeric(df['Birth Year'],errors='coerce' , downcast='integer')

    df.drop('Start Time', axis=1, inplace=True) 
    df.drop('End Time', axis=1, inplace=True) 

    return df


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_locaction = 0

    
    while view_data == 'yes':
        print(df.iloc[start_locaction:start_locaction+5])
        start_locaction=start_locaction +5
        view_data = input("Do you want to proceed showing the next 5 rows?\n").lower()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # the most common month
    print('The most frequent month is: ', df['start_month'].mode()[0])
    
    # the most common day of week
    print('The most frequent day is: ', df['start_day'].mode()[0])

    # the most common start hour
    print('The most commoon start hour is: ', df['start_time'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most commonly used start station
    print('The most commonly used start station is: ', df['Start Station'].mode()[0] )

    # most commonly used end station
    print('The most commonly used end station is: ', df['End Station'].mode()[0] )

    # most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station trip is: ', 
          df.groupby(['Start Station','End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time
    print('The total travel time in hours is: ', df['Trip Duration'].sum()/86400)

    # mean travel time
    print('The average travel time in minutes is: ', df['Trip Duration'].mean()/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

 
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # counts of user types
    print('In this city, we have diffrent types of users as follows: ')
    print(df['User Type'].value_counts())

    # this condition because the washington csv doens't include gender and year birth coulmns
    if city in ('new york city', 'chicago'):
        # counts users based on gender
        print('The total count of each gender is as follow: ')
        print('Females:', df['Gender'].value_counts().get("Female", 0))
        print('Males:', df['Gender'].value_counts().get("Male", 0))
        print('Unknown:', df['Gender'].value_counts().get("Unknown", 0))
        print('The earliest year of birth is: ', df['Birth Year'].min())

        #  most recent of birth 
        print('The most recent year of birth is: ', df['Birth Year'].max())

        #  most common year of birth
        print('The most common year of birth is: ', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    try:
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            df= clean_data(df, city)
            display_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            restart = str(input('\nWould you like to restart? Enter yes or no.\n'))
            if restart.lower() != 'yes':
                break
    except Exception as e:
        print("The program encountered an error: ", 
            type(e).__name__, " : ", e)
        traceback.print_exc()

### The Starting point of the project
if __name__ == "__main__":
	main()