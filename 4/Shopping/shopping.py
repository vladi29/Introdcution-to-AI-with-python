import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = list()
    deep_evidence = list()
    labels = list()
    evidences_columns = [
        'Administrative', 
        'Administrative_Duration',
        'Informational',
        'Informational_Duration',
        'ProductRelated',
        'ProductRelated_Duration',
        'BounceRates',
        'ExitRates',
        'PageValues',
        'SpecialDay',
        'Month',
        'OperatingSystems',
        'Browser',
        'Region',
        'TrafficType',
        'VisitorType',
        'Weekend'
        ]

    with open(filename) as File:
        reader = csv.DictReader(File)
        for row in reader:
            deep_evidence = []
            for evdnc in evidences_columns:
                deep_evidence.append(row[evdnc])
            evidence.append(deep_evidence)

            if row['Revenue'] == 'TRUE':
                labels.append(1)
            else:
                labels.append(0)
            
        for data in evidence:
            if data[10] == 'Jan':
                data[10] = 0
            elif data[10] == 'Feb':
                data[10] = 1
            elif data[10] == 'Mar':
                data[10] = 2
            elif data[10] == 'Apr':
                data[10] = 3
            elif data[10] == 'May':
                data[10] = 4
            elif data[10] == 'Jun':
                data[10] = 5
            elif data[10] == 'Jul':
                data[10] = 6
            elif data[10] == 'Aug':
                data[10] = 7
            elif data[10] == 'Sep':
                data[10] = 8
            elif data[10] == 'Oct':
                data[10] = 9
            elif data[10] == 'Nov':
                data[10] = 10
            else:
                data[10] = 11
        
        for data in evidence:
            if data[15] == 'Returning_Visitor':
                data[15] = 1
            else: 
                data[15] = 0
        
        for data in evidence:
            if data[16] == 'TRUE':
                data[16] = 1
            else:
                data[16] = 0

        #print(f'evidence: {evidence}')
        #print(f'labels: {labels}')
        return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    sensitivity = float()
    n_sensitivity = 0
    specificity = float()
    n_specificity = 0

    for i in range(len(labels)):
        if labels[i] == 0:
            n_specificity += 1
            if predictions[i] == 0:
                specificity += 1
            
        elif labels[i] == 1:
            n_sensitivity += 1
            if predictions[i] == 1:
                sensitivity += 1

    sensitivity = sensitivity/n_sensitivity
    specificity = specificity/n_specificity

    return (sensitivity, specificity)   

if __name__ == "__main__":
    main()
