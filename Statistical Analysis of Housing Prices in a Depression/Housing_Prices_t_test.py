import pandas as pd
import scipy.stats as stats

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''

    university_towns = get_list_of_university_towns()
    housing_data = convert_housing_data_to_quarters()
    recession_start, recession_bottom = get_recession_start(), get_recession_bottom()
    univ_data = pd.merge(university_towns, housing_data, how='inner', left_on=['State', 'RegionName'], right_index=True)
    matched_data = list(zip(univ_data['State'], univ_data['RegionName']))
    non_univ_data = housing_data.drop(matched_data, axis=0).copy()
    univ_data['Decline'] = univ_data[recession_start] - univ_data[recession_bottom]
    non_univ_data['Decline'] = non_univ_data[recession_start] - non_univ_data[recession_bottom]
    t_test_result = stats.ttest_ind(univ_data['Decline'], non_univ_data['Decline'], nan_policy='omit')
    #
    p = t_test_result.pvalue
    if (p < 0.01):
        different = True
    else:
        different = False
    if (t_test_result.statistic > 0):
        better = 'non-university town'
    else:
        better = 'university town'

    return (different, p, better)

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''

    df = pd.read_csv('university_towns.txt', sep="\n", header=None)
    df.columns = ['RegionName']

    # All of the state entries in the file have a trailing [edit] in the text.
    # By finding these entries, we can get the list of states.
    state = ''
    stateList = []
    for i in df['RegionName']:
        if '[edit]' in i:
            state = i.replace('[edit]', '')
            stateList.append(state)
        else:
            stateList.append(state)
    df['State'] = stateList
    df = df[df['RegionName'].str.find('[edit]') == -1]
    # Remove parenthetical expressions
    df['RegionName'] = df['RegionName'].str.replace(r' \(.*', '')
    # Remove brackets
    df['RegionName'] = df['RegionName'].str.replace(r'\[.*\]', '')
    df = df.reindex(columns=['State', 'RegionName'])
    df = df.reset_index(drop=True)
    return df

# Note:  get_recession_start, get_recession_end, and get_recession_bottom
# have some redundant code--partial credit on the project was awarded
# for the answer to each question and they were required to be calculated separately.
def get_recession_start():
    '''Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3'''

    df = pd.read_excel('gdplev.xls', skiprows=219, usecols='E,G')
    df.columns = ['Quarter', 'GDP']
    retVal = 'no recession'
    qtrs_down = 0
    qtrs_up = 0
    in_recession = False
    for i in range(1, len(df) - 1):
        if (df['GDP'][i] < df['GDP'][i - 1]) & (not in_recession):
            qtrs_down += 1
            qtrs_up = 0
            if (qtrs_down == 2):
                in_recession = True
                retVal = df['Quarter'][i - 1]
        elif (df['GDP'][i] > df['GDP'][i - 1]):
            qtrs_up += 1
            qtrs_down = 0
            if (qtrs_up == 2) & in_recession:
                break

    return retVal


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a
    string value in a format such as 2005q3'''

    df = pd.read_excel('gdplev.xls', skiprows=219, usecols='E,G')
    df.columns = ['Quarter', 'GDP']
    retVal = 'no recession'
    qtrs_down = 0
    qtrs_up = 0
    in_recession = False
    for i in range(1, len(df) - 1):
        if (df['GDP'][i] < df['GDP'][i - 1]) & (not in_recession):
            qtrs_down += 1
            qtrs_up = 0
            if (qtrs_down == 2):
                in_recession = True
        elif (df['GDP'][i] > df['GDP'][i - 1]):
            qtrs_up += 1
            qtrs_down = 0
            if (qtrs_up == 2) & in_recession:
                retVal = df['Quarter'][i]
                break

    return retVal


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a
    string value in a format such as 2005q3'''

    df = pd.read_excel('gdplev.xls', skiprows=219, usecols='E,G')
    df.columns = ['Quarter', 'GDP']
    retVal = 'no recession'
    lowPoint = -1
    qtrs_down = 0
    qtrs_up = 0
    in_recession = False
    for i in range(1, len(df) - 1):
        if (df['GDP'][i] < df['GDP'][i - 1]) & (not in_recession):
            qtrs_down += 1
            qtrs_up = 0
            if (qtrs_down == 2):
                in_recession = True
        elif (df['GDP'][i] > df['GDP'][i - 1]):
            qtrs_up += 1
            qtrs_down = 0
            if (qtrs_up == 2) & in_recession:
                break
        if in_recession:
            if lowPoint == -1:
                retVal = df['Quarter'][i]
                lowPoint = df['GDP'][i]
            elif df['GDP'][i] < lowPoint:
                retVal = df['Quarter'][i]
                lowPoint = df['GDP'][i]

    return retVal


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''

    df = pd.read_csv('City_Zhvi_AllHomes.csv')
    df = df.drop(['RegionID', 'Metro', 'CountyName', 'SizeRank'], axis=1)
    df = df.loc[:, ~df.columns.str.contains('^199')]
    df['State'] = df['State'].replace(states)
    df = df.set_index(['State', 'RegionName'])
    df.columns = pd.PeriodIndex(pd.to_datetime(df.columns), freq='Q').map(str)
    df = df.rename(columns=lambda x: x.replace('Q', 'q'))
    df = df.groupby(by=df.columns, axis=1).mean()
    return df

# Main
res = run_ttest()
if(res[0] == True):
    print('Null hypothesis was rejected with p=%.6f' % res[1] , ';\n', res[2], 's are less susceptible to real estate value declining in a recession.', sep="")
else:
    print('Null hypothesis could not be rejected; p=%.6f' % res[1], sep="")
