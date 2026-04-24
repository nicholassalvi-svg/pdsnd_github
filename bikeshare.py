
import numpy as np
import pandas as pd
import os
import time

# Reference values to support menu functionality 

CITY_DATA = [('chicago', 'chicago.csv'),
             ('new york city', 'new_york_city.csv'),
             ('washington d.c.', 'washington.csv')]
MONTH_DATA = ('january', 'february', 'march', 'april', 'may', 'june')
DAY_DATA = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
FILTER_OPTIONS = ('month', 'day', 'both', 'no filter')
DISPLAY_OPTIONS = ('raw data', 'summarized statistics')



def print_start_screen():
    '''Display a title screen'''
    
    print()
    print('=====================')
    print('   BIKESHARE DATA    ')
    print('=====================')
    print()
    print('Welcome!')
    print('This program allows you to explore bikeshare data.')
    print('This project is hosted on GitHub at https://github.com/nicholassalvi-svg/pdsnd_github')    
    print()



def clear_screen():
    '''Clear the terminal window.'''
    
    os.system("cls" if os.name == "nt" else "clear")



def get_filters():
    '''Prompt the user for city, month and day filters which will then be used to load a .csv file.'''
    
    month = None
    day = None
    check = False

    while check == False: # Check if the user input is valid. Proceed when True.
          print('Please select a city to load bikeshare data for.')
          print('Only one city at a time can be analyzed.')
          print(f'Enter the corresponding value (0 through {len(CITY_DATA)-1}) from the list.')
          print()
    
          for index, value in enumerate(CITY_DATA):
               print(f'{index} - {value[0].title()}')
          print()
          city = input('Select city: ')
          check, city = check_option(city, range(len(CITY_DATA)))
          print()
          
    check = False
    while check == False: # Check if the user input is valid. Proceed when True.
          print('Would you like to filter the data by month, day, both, or not at all?')
          print(f'Enter the corresponding value (0 through {len(FILTER_OPTIONS)-1}) from the list.')
          print()
          
          for index, value in enumerate(FILTER_OPTIONS):
              print(f'{index} - {value.title()}')
          print()

          filter_opt = input('Select filter: ')
          check, filter_opt = check_option(filter_opt, range(len(FILTER_OPTIONS)))
          print()

    check = False
    if filter_opt == 0: # Filter by month
         while check == False: # Check if the user input is valid. Proceed when True.
             print('For what month would you like to filter the data?')
             print(f'Enter the corresponding value (0 through {len(MONTH_DATA)-1}) from the list.')
             print()

             for index, value in enumerate(MONTH_DATA):
                 print(f'{index} - {value.title()}')
             print()

             month = input('Select month: ')
             check, month = check_option(month, range(len(MONTH_DATA)))
             print()

    elif filter_opt == 1: # Filter by day
         while check == False: # Check if the user input is valid. Proceed when True.
             print('For what day would you like to filter the data?')
             print(f'Enter the corresponding value (0 through {len(DAY_DATA)-1}) from the list.')
             print()

             for index, value in enumerate(DAY_DATA):
                 print(f'{index} - {value.title()}')
             print()
         
             day = input('Select day: ')
             check, day = check_option(day, range(len(DAY_DATA)))
             print()
         
    elif filter_opt == 2: # Filter month and day
         while check == False: # Check if the user input is valid. Proceed when True.
             print('For what month would you like to filter the data?')
             print(f'Enter the corresponding value (0 through {len(MONTH_DATA)-1}) from the list.')
             print()
             
             for index, value in enumerate(MONTH_DATA):
                 print(f'{index} - {value.title()}')
             print()

             month = input('Select month: ')
             check, month = check_option(month, range(len(MONTH_DATA)))
             print()
         
         check = False
         while check == False: # Check if the user input is valid. Proceed when True.
             print('For what day would you like to filter the data?')
             print(f'Enter the corresponding value (0 through {len(DAY_DATA)-1}) from the list.')
             print()
             for index, value in enumerate(DAY_DATA):
                 print(f'{index} - {value.title()}')
             print()

             day = input('Select day: ')
             check, day = check_option(day, range(len(DAY_DATA)))
             print()

    elif filter_opt == 3: # No filter
         month = None
         day = None
     
    print('SELECTED FILTERS')
    print()
    print(f'City: {CITY_DATA[city][0].title()}')
    print(f'Month: {MONTH_DATA[month].title() if month is not None else "None"}')
    print(f'Day: {DAY_DATA[day].title() if day is not None else "None"}')
    print()

    return(filter_opt, city, month, day)



def check_option(option, options):
     '''Checks user input to make sure their selection is an interger and is within the allowed values.'''

     try:
          option = int(option)
     except (TypeError, ValueError):
          print()
          print(f'!! Invalid Option: "{option}"')
          print('Plese select a valid option.')
          return False, None
     except Exception as e:
          print(f'! - Unhandled exception: {e}')
          return False, None
     
     if option not in options:
          print()
          print(f'!! Invalid Option: "{option}"')
          print('Plese select a valid option.')
          return False, None
     else:
          return True, option



def hour12_display(h):
     '''Displays an hour as a string in 12 hour format.'''

     h =int(h)
     if h == 0:
          return '12:00 AM'
     elif h < 12:
          return str(h) + ':00 AM'
     elif h == 12:
          return '12:00 PM'
     else:
          return str(h - 12) + ':00 PM'



def load_data(option, city, month=False, day=False):
     '''Load .csv file based on selections. Format CSV columns needed to calculate statistics.'''
     
     print('Loading Bike Share data...') 
     start_timestamp = time.time()
     try:
         df = pd.read_csv(filepath_or_buffer=CITY_DATA[city][1], index_col=False)
         df = df.loc[:, ~df.columns.str.contains('^Unnamed')] # Remove unnamed columns
         raw_columns = df.columns
         pd.set_option('display.show_dimensions', False) # Suppress dimensions when printing
         print(f'"{CITY_DATA[city][1]}" has been loaded.')
         print(f'Done. Operation took {(time.time() - start_timestamp):.2f} seconds')
         print()
     except Exception as e:
          print(f'! - Unhandled exception: {e}')
          print()
     
     print('Formatting data...')
     start_timestamp = time.time()
     
     df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
     df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')
     df['Trip'] = df['Start Station'] + " to " + df['End Station']
         
     # This conversion might not work if data is unavailable in the file
     try:
          df['Birth Year'] = pd.to_numeric(df['Birth Year'], errors='coerce').astype('Int64')
     except Exception as e:
          print(f'! - Unhandled exception: {e}')
          print()

     print(f'Done. Operation took {(time.time() - start_timestamp):.2f} seconds')
     print()

     print('Applying filters...')
     start_timestamp = time.time()
     if (option == 0) or (option == 2): # Filter by month, or month and day
          df = df[df['Start Time'].dt.month == month+1]
          df = df.reset_index(drop=True) # Reset the index

     if(option == 1) or (option == 2): # Filter by day, or month and day
          df = df[df['Start Time'].dt.dayofweek == day]
          df = df.reset_index(drop=True) # Reset the index

     print(f'Done. Operation took {(time.time() - start_timestamp):.2f} seconds')
     print()
      
     return df, list(raw_columns)
   


def summary_stats(df, city_raw_columns):
     '''Calculate and display summary statistics based on the loaded .csv file.'''
     
     print('SUMMARY STATISTICS')
     print()
     print('POPULAR TRAVEL TIMES')
     print('Calculating statistics...')
     start_timestamp = time.time()
     print()

     start_months = df['Start Time'].dt.month
     most_common_months = start_months.mode()
     months_ct = start_months.value_counts()
     most_common_months_ct = list(months_ct[most_common_months])
     most_common_months_display = [MONTH_DATA[i-1].title() for i in most_common_months]
     print(f'Most common month(s): {', '.join(most_common_months_display)}')
     print(', '.join(f'{x:,}' for x in most_common_months_ct), 'trips')

     start_days = df['Start Time'].dt.dayofweek
     most_common_days = start_days.mode()
     days_ct = start_days.value_counts()
     most_common_days_ct = list(days_ct[most_common_days])
     most_common_days_display = [DAY_DATA[i].title() for i in most_common_days]
     print(f'Most common day(s) of week: {', '.join(most_common_days_display)}')
     print(', '.join(f'{x:,}' for x in most_common_days_ct), 'trips')

     start_hours = df['Start Time'].dt.hour
     most_common_hours = start_hours.mode()
     hours_ct = start_hours.value_counts()
     most_common_hours_ct = list(hours_ct[most_common_hours])
     most_common_hour_display = [hour12_display(h) for h in most_common_hours]
     print(f'Most common hour(s) of day: {', '.join(most_common_hour_display)}')
     print(', '.join(f'{x:,}' for x in most_common_hours_ct), 'trips')

     print()
     print(f'Done. Operation took {(time.time() - start_timestamp):.2f} seconds')
     print()
     print('POPULAR STATIONS AND TRIPS')
     print('Calculating statistics...')
     start_timestamp = time.time()
     print()

     most_common_start_stn = df['Start Station'].mode()
     start_stn_ct = df['Start Station'].value_counts()
     most_common_start_stn_ct = list(start_stn_ct[most_common_start_stn])
     print(f'Most common start station(s): {', '.join(most_common_start_stn)}')
     print(', '.join(f'{x:,}' for x in most_common_start_stn_ct), 'trips')
          
     most_common_end_stn = df['End Station'].mode()
     end_stn_ct = df['End Station'].value_counts()
     most_common_end_stn_ct = list(end_stn_ct[most_common_end_stn])
     print(f'Most common end station(s): {', '.join(most_common_end_stn)}')
     print(', '.join(f'{x:,}' for x in most_common_end_stn_ct), 'trips')

     most_common_trip = df['Trip'].mode()
     trip_ct = df['Trip'].value_counts()
     most_common_trip_ct = list(trip_ct[most_common_trip])
     print(f'Most common trip(s): {', '.join(most_common_trip)}')
     print(', '.join(f'{x:,}' for x in most_common_trip_ct), 'trips')
     print()

     print(f'Done. Operation took {(time.time() - start_timestamp):.2f} seconds')
     print()

     print('TRIP DURATION')
     print('Calculating statistics...')
     start_timestamp = time.time()
     print()

     total_travel_time = (df['Trip Duration'].sum() / 60)
     print(f'Total travel time: {total_travel_time:,.2f} minutes')

     avg_travel_time = (df['Trip Duration'].mean() / 60)
     print(f'Average travel time: {avg_travel_time:,.2f} minutes')
     print(f'{trip_ct.sum():,} trips')
     print()

     print(f'Done. Operation took {(time.time() - start_timestamp):.2f} seconds')
     print()

     print('USER INFORMATION')
     print('Calculating statistics...')
     start_timestamp = time.time()
     print()

     print('User Type totals: \n')
     user_totals = df.groupby(['User Type']).size().map('{:,}'.format).to_string()
     print(user_totals)
     print()

     print('Gender totals:')
     if 'Gender' in city_raw_columns:
          print()
          gender_totals = df.groupby(['Gender']).size().map('{:,}'.format).to_string()
          print(gender_totals)
     else: 
          print('Gender data not present file.')
          
     print()
     print('User birthday information')
     if 'Birth Year' in city_raw_columns:
          print()
          min_birth_year = df['Birth Year'].min()
          print(f'Earliest birth year: {min_birth_year}')

          max_birth_year = df['Birth Year'].max()
          print(f'Most recent birth year: {max_birth_year}')

          mode_birth_year = df['Birth Year'].mode()
          birth_years = df['Birth Year'].value_counts()
          mode_birth_year_ct = list(birth_years[mode_birth_year])
          print(f'Most common birth year(s): {', '.join(map(str, mode_birth_year))}')
          print(', '.join(f'({x:,}' for x in mode_birth_year_ct), 'users)')
               
     else: 
          print('Birthday data not present file.')
          
     print()
     print(f'Done. Operation took {(time.time() - start_timestamp):.2f} seconds')
     print()

     time.sleep(5) # Wait 5 seconds



def raw_data(df, city_raw_columns):
     '''Display the raw data from the loaded .csv file, 5 rows at a time.'''

     print('RAW DATA')
     print()
     print('Displaying the fist 5 rows of raw data.')
     print()
     for i in range(0,len(df),5):
          print(df.iloc[i:i+5].loc[:,city_raw_columns])
          i += 5
          print()
          print('Display the next 5 rows of data?')
          proceed = input('Enter "Q" to quit this function. Otherwise enter any other value: ').lower()
          print()
          
          if proceed == 'q':
               print
               return



def main():
     '''The main program loop.'''

     clear_screen()

     while True:
          print_start_screen()
          
          print('SELECT CITY AND FILTERS')
          print()

          print('Would you like to proceed?')
          proceed = input('Enter "Q" to quit. Otherwise enter any other value: ').lower()
          print()
          
          if proceed == 'q':
               clear_screen()
               break
          proceed = None

          filter_opt, city, month, day = get_filters()
          
          print('LOAD CITY DATA')
          print()

          print('Would you like to proceed?')
          proceed = input('Enter "Q" to quit. Enter "R" to restart. Otherwise enter any other value: ').lower()
          print()

          if proceed == 'q':
               clear_screen()
               break
          if proceed == 'r':
               clear_screen()
               continue
          proceed = None

          city_dataframe, city_raw_columns = load_data(filter_opt, city, month, day)

          while True:

               check = False
               while check == False:
                    print('Would you like to view the raw data or see summary statistics?')
                    print(f'Enter the corresponding value (0 through {len(DISPLAY_OPTIONS)-1}) from the list.')
                    print()
                    for index, value in enumerate(DISPLAY_OPTIONS):
                         print(f'{index} - {value.title()}')
                    print()
                    display_opt = input('Select display option: ')
                    check, display_opt = check_option(display_opt, range(len(DISPLAY_OPTIONS)))
                    print()

               if display_opt == 0:
                    raw_data(city_dataframe, city_raw_columns)
               elif display_opt == 1:
                    summary_stats(city_dataframe, city_raw_columns)

               print(f'Would you continue exploring the {CITY_DATA[city][0].title()} bike share data?')
               proceed = input('Enter "Q" to quit. Otherwise enter any other value: ').lower()
               print()

               if proceed == 'q':
                    clear_screen()
                    break



if __name__ == "__main__":
	main()
