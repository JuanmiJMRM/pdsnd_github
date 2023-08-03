import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def check_data(question, available_data):
    """
    Ask and check the data provided compare with the available_data.
    
    Returns:
        string - input data enter by the users
    """
    try:
        user_input = str(input(question)).title()
        while user_input not in available_data :
            print('It looks like your entry is incorrect.')
            print('Let\'s try again!')
            user_input = str(input(question)).title()
        
        print('Great! You\'ve chosen: {}\n'.format(user_input))
        return user_input
    
    except:
        print('There seems to be an issue with your input.')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check_data("Would you like to see data for Chicago, New York, or Washington? ", ["Chicago", "New York", "Washington"])

    filter_input = check_data("Would you like to filter the data by month, day, both or not at all (Type \"none\" for no filter)? ", ["Month", "Day", "Both", "None"])
    month = ""
    day = ""
    
    if (filter_input in ["Month", "Both"]):
        month = check_data("Which month? January, February, March, April, May, June or all (Type \"All\" for all month)? ", ['January', 'February', 'March', 'April', 'May', 'June', "All"])
    else:
        month = "All"

    if (filter_input in ["Day", "Both"]):
        day = check_data("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all (Type \"All\" for all days)? ", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All"]) #TO_DO check the input is correct and make all correct
    else:
        day = "All"

    print("\n\nOK let's go to explore {} City and filter the data by {}\n".format(city, filter_input))
    if month != "":
        print("You want to filter by {} month(s)\n".format(month))
    if day != "":
        print("You want to filter by {} day(s)\n".format(day))
    if month == "" and day == "":
        print("No filter will be applied\n")


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df["day_of_week"] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'All':           
        # filter by month to create the new dataframe
        df = df[df["month"]==month]

    if day != 'All':
        # filter by day of week to create the new dataframe
         df=df[((df["day_of_week"])==day)]

    return df

    


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most popular month is {}".format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day is {}".format(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular start hour is {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular start station is {}".format(popular_start_station))
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popular end station is {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + "," + df["End Station"]
    popular_trip = df["trip"].mode()[0]

    print("The most popular trip start in {} and finish in {}".format(popular_trip.split(",")[0], popular_trip.split(",")[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("The total travel time is {} hour(s), {} minute(s), {} second(s)".format((total_travel_time//3600), (total_travel_time%3600)//60, (total_travel_time%3600)%60))
    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("The mean travel time is {} minutes {} seconds".format((mean_travel_time//60), (mean_travel_time%60)%60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_usertypes = df["User Type"].value_counts()
    print("\nLet's go to see the display counts of user types: ")
    for label, value in count_usertypes.items():
        print ("{}: {}".format(label, value))


    # Display counts of gender
    if "Gender" in df:
        count_gender = df["Gender"].value_counts()
        print("\nLet's go to see the display counts of gender: ")
        for label, value in count_gender.items():
            print ("{}: {}".format(label, value))
        
    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("\nLet's go to see some information about the age of the users:")
        print("Oldest year of birth: {}".format(df["Birth Year"].min()))
        print("Youngest year of birth: {}".format(df["Birth Year"].max()))
        print("The most popular year of birth: {}".format(df["Birth Year"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df, n_rows):
    """ Display the information of the dataframe df. The number of rows to display is specified in n_rows """

    display = True
    i=0
    len_df = len(df)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)

    while display == True:
        answer = input("Do you want to see {} lines of the data? (Yes/No)".format(n_rows))
        if ((answer.lower() == "yes") and (len_df > i)):
            if len_df > (i + n_rows):
                print(df[i:(i + n_rows)])
                i = i + n_rows
                
            else:
                print(df[i:len_df])
                display = False
                
        elif (answer.lower() == "no") or (len_df  <= i):
            display = False
            
        else:
            print("Sorry, I don't undestand your request...")
        
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
              
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_data(df, 100)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
