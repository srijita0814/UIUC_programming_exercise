# required imports
import argparse
import os
import json
import datetime
import collections

output_folder = ''

# read JSON file
def read_file(file_name):
    with open(file_name) as f:
        try:
            training_data = json.load(f)
        except Exception as e:  # if file is not in correct format
            print("Error: Incorrect file data. Data in file needs to be in JSON format matching training.txt.")
            exit()
    return training_data

# write JSON output file
def write_file(dict_data, file_name):
    json_object = json.dumps(dict_data, indent=4)
    with open(output_folder+'/'+file_name+".json", "w") as outfile:
        outfile.write(json_object)

# count number of people who have completed trainings
def completed_trainings(training_data):
    training_count = {} # Dictionary to add trainings and count
    for person in training_data:
        courses = []
        for training in person['completions']:
            training_name = training['name']
            if training_name not in courses:
                courses.append(training_name)
                training_count[training_name] = training_count.get(training_name, 0) + 1
    # Covert to required JSON format
    training_count = [{'training_name': key, 'count': value} for key, value in training_count.items()]
    write_file(training_count, "completed_trainings")

# list all people that completed trainings present in training list in the specified fiscal year
def fiscal_year_trainings(training_data, trainings_list, year):
    results = {
    "fiscal_year": year
    }
    people_trained = collections.defaultdict(list)
    # initilize dictionary of trainings with people name
    for i in trainings_list:
        people_trained[i]
    fiscal_year_start = datetime.datetime.strptime('07/01/'+str(year-1), "%m/%d/%Y")
    fiscal_year_end = datetime.datetime.strptime('06/30/'+str(year), "%m/%d/%Y")
    for person in training_data:
        p_name = person['name']
        for training in person['completions']:
            training_name = training['name']
            if training_name not in trainings_list:
                continue
            training_time = datetime.datetime.strptime(training['timestamp'], "%m/%d/%Y")
            # check training is within fiscal year and name is not duplicated
            if (fiscal_year_start <= training_time <= fiscal_year_end) and p_name not in people_trained[training_name]:
                people_trained[training_name].append(p_name)
    # Covert to required JSON format
    people_trained = [{'training_name': key, 'people_trained': value} for key, value in people_trained.items()]
    results['results'] = people_trained
    write_file(results, "fiscal_year_trainings")

# given a date, find all people that have any completed trainings that have already expired, or will expire within one month of the specified date
def expired_trainings(training_data, expiry_date):
    expiry = datetime.datetime.strptime(expiry_date, "%m/%d/%Y")
    expected_expiry = expiry + datetime.timedelta(days=30)
    people_trained = {'expiry_date': expiry_date, 'people': []}
    for person in training_data:
        # dictionary to store the most recent course completions
        courses = {}
        p_data = {'person_name': person['name'], 'trainings': []}
        for training in person['completions']:
            expires = datetime.datetime.strptime(training['expires'], "%m/%d/%Y") if training['expires'] else None
            if expires:
                if training['name'] not in courses:
                    if expires < expiry:
                        courses[training['name']] = 'expired'
                    # if expiration date is within 30 days after the given date, it is expiring soon
                    elif expiry <= expires <= expected_expiry:
                        courses[training['name']] = 'expires soon'
                else:
                    # check if we need to update the status
                    if expiry <= expires <= expected_expiry and courses[training['name']] == 'expired':
                        courses[training['name']] = 'expires soon'
        if courses:
            p_data['trainings'] = [{'name': key, 'status': value} for key, value in courses.items()]
        # only add the person if they have any valid training completions
        if p_data['trainings']:
            people_trained['people'].append(p_data)
    write_file(people_trained, "expired_trainings")

# parser to read arguments provided when file is run from console
def create_parser():
    parser = argparse.ArgumentParser(description="Command-line app for Trainings Insights")
    parser.add_argument('-i', '--input_file', help='Input file to process')
    parser.add_argument('-o', '--output', type=str, help='Output files folder name')
    parser.add_argument('-y', '--year', type=str, help='Year required to comute trainings completed in a fiscal year')
    parser.add_argument('-t', '--trainings', type=str, help='Comma separated list of trainings in a fiscal year')
    parser.add_argument('-d', '--date', type=str, help='Date in mm/dd/yyyy format to identify people with either expired or about to expire trainings')
    return parser

# main function that is executed when application is run
def main():
    global output_folder
    fiscal_year = ''
    training_list = ''
    expiry_date = ''

    parser = create_parser()
    args = parser.parse_args()

    # checks to see if arguments have been provided on input
    if args.input_file:
        file_name = args.input_file
        data = read_file(file_name)
    elif not args.input_file:
        print("Input file is a required field. Please try again with input file parameter.")
        parser.print_help()
        exit()
    if args.output:
        output_folder = './'+args.output
    else:
        output_folder = './output_files'
    if args.year:
        fiscal_year = int(args.year)
    else:
        fiscal_year = 2024
    if args.trainings:
        k = args.trainings.split(',')
        training_list = k
    else:
        training_list = ['Electrical Safety for Labs', 'X-Ray Safety', 'Laboratory Safety Training']
    if args.date:
        expiry_date = args.date
    else:
        expiry_date = '10/01/2023'

    # create output folder if not present
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    data = read_file(file_name) # get data
    completed_trainings(data) # Task 1 - generates json output file - completed_trainings.json
    fiscal_year_trainings(data, training_list, fiscal_year) # Task 2 - generates json output file - fiscal_year_trainings.json
    expired_trainings(data, expiry_date) # Task 3 - generates json output file - expired_trainings.json

if __name__ == "__main__":
    main()
