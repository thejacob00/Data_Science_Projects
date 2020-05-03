import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier


def blight_model():
    # Read in the provided data files
    test = pd.read_csv('test.csv', dtype={'zip_code': str}, parse_dates=['ticket_issued_date'])
    train = pd.read_csv('train.csv', encoding="ISO-8859-1", dtype={'zip_code': str}, parse_dates=['ticket_issued_date'])
    latlon = pd.read_csv('latlons.csv')
    addresses = pd.read_csv('addresses.csv')

    # Convert the dates to seconds so that they can be compared properly.
    train['ticket_issued_date'] = pd.to_datetime(train['ticket_issued_date']).astype(np.int64)
    test['ticket_issued_date'] = pd.to_datetime(test['ticket_issued_date']).astype(np.int64)

    # Eliminate rows where the accused was found not responsible (compliance is null).
    # The test set does not include any such rows.
    train = train.dropna(subset=['compliance'])

    # Connect tickets to addresses, and those addresses to latitude/longitude locations.
    # Latitude/longitude is a more quantitative approach and should be a better feature.
    train = pd.merge(train, addresses, on='ticket_id')
    train = pd.merge(train, latlon, on='address')
    test = pd.merge(test, addresses, on='ticket_id')
    test = pd.merge(test, latlon, on='address')

    # Replace the agency names with numeric values
    agency_dict = {'Department of Public Works': 0, 'Buildings, Safety Engineering & Env Department': 1,
                   'Detroit Police Department': 2, 'Health Department': 3, 'Neighborhood City Halls': 4}
    train['agency_id'] = train['agency_name'].map(agency_dict)
    test['agency_id'] = test['agency_name'].map(agency_dict)

    # Save off the test ticket ids for later use
    ticket_ids = test['ticket_id']

    # Select the most useful columns from the data as potential features.
    # The most indicative features, in my estimation are:
    # --who issued the ticket (agency_id)
    # --when did the violation take place?
    # --how much is total fine?
    # --where is the violator from? (further away intuitively means less likely to pay)
    train = train[['agency_id', 'ticket_issued_date',
                  'judgment_amount', 'lat', 'lon', 'compliance']]
    test = test[['agency_id', 'ticket_issued_date',
                'judgment_amount', 'lat', 'lon']]

    # Remove rows where the address lat/lon could not be found
    train = train[~train.isnull().any(axis=1)]

    # Since we can't replace the test set, use 0
    test = test.fillna(0)

    # y_train is the single column corresponding to compliance for each ticket
    # X_train is the list of remaining columns that can be considered as features
    y_train = train['compliance']
    X_train = train.drop('compliance', axis=1)

    # Random Forest Classifier
    #
    # Different estimators and depth cost different amounts of processing time, with corresponding
    # improvements in prediction AUC:
    #
    # Estimators = 20, Depth = 5:  Runtime < 1m, AUC 0.681
    # Estimators = 50, Depth = 10:  Runtime 2m, AUC 0.715
    clf = RandomForestClassifier(n_estimators=50, max_depth=10).fit(X_train, y_train)

#    print('Accuracy of RF classifier on training set: {:.2f}'
#          .format(clf.score(X_train, y_train)))

    predictions = clf.predict_proba(test)

    return pd.Series(data=predictions[:, 1], index=ticket_ids)


print(blight_model())
