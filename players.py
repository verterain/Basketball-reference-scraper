import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_last5_data(player_name):
    # Get first letter of last name and name abbreviation for the sake of basketball reference url construction - for instance, for Kawhi Leonard it's 'leonaka01'
    name_abbrev = ''.join([player_name.split()[1][:5], player_name.split()[0][:2], '01']).lower()
    initial = name_abbrev[0].lower()
    # Fetch the url & HTML content
    url = f"https://www.basketball-reference.com/players/{initial}/{name_abbrev}.html"
    response = requests.get(url)
    # Parse the HTML content and extract the 'Last 5 games table'
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', id='last5')
   
    try: 
        # Get headers for the dataframe
        headers = [th.get_text() for th in table.find_all('th', scope='col')]
        # Extract the data for the table's rows and columns
        rows = table.find_all('tr')[1:6]
        data = []
        for row in rows:
            # Handle the date cell seperately, as it's 'th' element, not 'td' like the rest
            date_cell = row.find('th', {'data-stat':'date'})
            if date_cell:
                date = date_cell.get_text()
            else:
                continue
            # Extract the stats from the rest of the cells 
            cells = row.find_all('td')
            row_data = [date] + [cell.get_text() for cell in cells]
            data.append(row_data)
            # Create & return the df
            df = pd.DataFrame(data, columns=headers)
            df.columns.values[2] = 'At/Vs'
        return df
    except Exception as e:
        print(f"No data for player by the name {player_name} available")