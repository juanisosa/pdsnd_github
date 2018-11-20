import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        try:
            city = input('\nPlease select one of the following cities to see bikeshare data: Chicago, New York City or Washington: ').lower()
            if city in CITY_DATA.keys(): #checking that the city
                break
        except KeyboardInterrupt: #To allow terminating the program during input
            print('\n')
            break
        except:
            print('\nThat\'s not a valid city name! Please try again: ')


    # get user input for month (all, january, february, ... , june)

    while True:
        try:
            month = input('\nFor which month between January and June would you like to filter the data? Please type \'all\' to not apply a filter:  ').lower()
            if month in MONTHS:
                break
            elif month == 'all':
                break
        except KeyboardInterrupt:
            print('\n')
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        try:
            day = input('\nFor which day of the week? Please enter \'all\' for all days: ').lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                break
        except KeyboardInterrupt:
            print('\n')
            break


    print('-'*40)
    return city, month, day


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time  and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day of week and hour from Start Time to create new columns plus concatinate start and end stations for route
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour
    df['route'] = df['Start Station'] + ' to ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    if month == 'all':
        #deterine most common month and convert from integer (1,...,6) into named month.
        #using grouby, size and idxmax to get the index with the highest value
        most_common_month = MONTHS[df.groupby(['month']).size().idxmax() - 1]

        print('The month with the most rides was: {}\n'.format(most_common_month.title()))

    # display the most common day of week
    #using if statement to not run if user filterd data by day of the week
    if day == 'all':
        #using grouby, size and idxmax to get the index with the highest value
        print('The most common day of the week was: {}\n'.format(df.groupby(['day_of_week']).size().idxmax()))

    # display the most common start hour

    print('The most common hour to start a trip was: {}\n'.format(df.groupby(['start_hour']).size().idxmax()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print('The most common station to start a trip was {} with {} trips starting there.\n'.format(df.groupby(['Start Station']).size().idxmax(), df.groupby(['Start Station']).size().max()))

    # display most commonly used end station

    print('The most common station to end a trip was {} with {} trips ending there.\n'.format(df.groupby(['End Station']).size().idxmax(), df.groupby(['End Station']).size().max()))

    # display most frequent combination of start station and end station trip

    print('The most common station combination was {} with {} trips.\n'.format(df.groupby(['route']).size().idxmax(), df.groupby(['route']).size().max()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in minutes by performing a sum of the Trip Duration column and dividing by 60

    print('Total travel time was for your selection was: {} minutes and {} seconds\n'.format(df['Trip Duration'].sum()//60, df['Trip Duration'].sum() % 60))

    # display mean travel time in minutes by calculating the mean of the Trip Duration column and dividing by 60

    print('The mean travel time was: {} minutes and {} seconds\n'.format(df['Trip Duration'].mean()//60, df['Trip Duration'].mean() % 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city): #modified function to include city as a parameter
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The breakdown of user types is:\n', df.groupby(['User Type']).size())

    # Display counts of gender

    if city.lower() in ['chicago', 'new york city']:
        print('\nThe breakdown of the users gender is:\n', df.groupby(['Gender']).size())

    # Display earliest, most recent, and most common year of birth

    if city.lower() in ['chicago', 'new york city']:
        print('\nThe most common year of birth of the users is: {}\n'.format(df.groupby(['Birth Year']).size().idxmax()))

        print('The oldest user was born in {}\n'.format(df['Birth Year'].min()))

        print('The youngest user was born in {}\n'.format(df['Birth Year'].max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    '''
    Asks user if they would like to see raw data. If anwser is yes, the system will display 5 rows of data and reprompt the user until answer != yes
    '''
    while True:
        try:
            cont = input('\nWould you like to see 5 rows of raw data? (Y, N): ').lower()
            if cont != 'y':
                print('-'*40)
                break
            else:
                print(df.head())
        except KeyboardInterrupt:
            print('\n')
            break


def main():
    while True:
        city, month, day = get_filters()
        #print summary of filters selected by user
        print('\nYou chose to analyze data {}, {}, {}'.format(city.title(), month.title(), day.title()))
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        #function to print raw data sample as per rubric
        raw_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            #added message to restart condition
            print('\nThank you and have a nice day!\n')
            break


if __name__ == "__main__":
	main()
