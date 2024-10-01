# training_insights_test

This repository is a command line application created to gain training insights from any json data file in the format provided in the example file (trainings.txt).

Python version used - Python 3.12.0

To execute the file, open command line and navigate to the directory where the code is present. The output file folder is created in the same directory as the code.

To learn about the arguments to be provided to the code run the following command.
 ```bash
python3 generate_training_insights.py -h
```

To execute file:
```bash
generate_training_insights.py [-h] [-i INPUT_FILE] [-o OUTPUT] [-y YEAR] [-t TRAININGS] [-d DATE]
```
Example command:
```bash
python3 generate_training_insights.py -i 'trainings.txt' -o 'sample_output' -y '2024' -t 'Electrical Safety for Labs,X-Ray Safety' -d '10/01/2023'
```
Note: input_file is a required argument.

'-o', '-y', '-t', '-d' are optional arguments which are of string type. The default values of the arguments are as follows:

-o - './output_files' (Output files are created in this directory)

-y - '2024' (as provided in the programming exercise description)

-t - ['Electrical Safety for Labs', 'X-Ray Safety', 'Laboratory Safety Training'] (as provided in the programming exercise description)

-d - '10/01/2023' (as provided in the programming exercise description. Format accepted is 'mm/dd/yyyy')

To run application with default argument values:
```bash
python3 generate_training_insights.py [-i INPUT_FILE]
```
Example command for default argument values:
```bash
python3 generate_training_insights.py -i 'trainings.txt'
```

All output files are created in either the default folder or the folder named specified in the arguments.

In the repository, the output_files folder contains the results of the default values mentioned in the programming exercise with trainings.txt as the input file.

Output File Generated Description: The output files are created for solving the questions in the programming exercise description.

<b>completed_trainings.json</b> - List each completed training with a count of how many people have completed that training.

<b>fiscal_year_trainings.json</b> - Given a list of trainings and a fiscal year (defined as 7/1/n-1 – 6/30/n), for each specified training, list all people that completed that training in the specified fiscal year.

<b>expired_trainings.json</b> - Given a date, find all people that have any completed trainings that have already expired, or will expire within one month of the specified date.
