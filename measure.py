import os
import logging
import numpy as np
from src.utils import measure
from collections import defaultdict
import pandas as pd

logging.basicConfig(level=logging.INFO)

def main():
    """
    Main function to write down measurements results to the CSV file in res folder.
    """
    # check if res folder exists and create if not
    res_dir = 'res'
    os.makedirs(res_dir, exist_ok=True)

    # check if parsed folder exists 
    parsed_data_dir = os.path.join('data', 'parsed')
    if not os.path.exists(parsed_data_dir):
        raise Exception("No folder named 'parsed' in 'data'")
    # check if parsed folder is empty 
    if not os.listdir(parsed_data_dir):
        raise Exception("Folder 'parsed' is empty")

    # get list of groups
    groups = os.listdir(parsed_data_dir)
    logging.info(f"Groups: {groups}")
    
    # get list of samples (subfolders inside groups)
    for group in groups:
        # check if group folder exist and is not empty
        group_dir = os.path.join(parsed_data_dir, group)
        if not os.path.exists(group_dir):
            raise Exception(f"No folder named '{group}' in 'parsed'")
        if not os.listdir(group_dir):
            raise Exception(f"Folder '{group}' is empty")

        # iterate through each sample folder
        for sample in os.listdir(group_dir):
            sample_dir = os.path.join(group_dir, sample)
            if not os.path.exists(sample_dir):
                raise Exception(f"No folder named '{sample}' in '{group}'")
            if not os.listdir(sample_dir):
                raise Exception(f"Folder '{sample}' is empty")

            files = os.listdir(sample_dir)
            logging.info(f"Files in sample {sample}: {files}")

            # check if there is already a file with measurements
            if os.path.isfile(f'res/measurements.csv'):
                measurements = pd.read_csv('res/measurements.csv')
                # create dictionary from the dataframe
                measurements = measurements.to_dict('list')
            else:
                measurements = defaultdict(list) # set measurements dictionary

            # for each file, read data and compute measurements
            for file in files:
                # check if measurements is not dictionary
                if not isinstance(measurements, dict):
                    measurements = measurements.to_dict('list')
                file_path = os.path.join(sample_dir, file)
                logging.info(f"Reading data from {file_path}")
                data = np.loadtxt(file_path, delimiter=",")
                logging.info(f"Data: {data}")

                # read shifted_axons from the file
                growth_arr = np.loadtxt(file_path, delimiter=",")
                genotype = str(group) # set name of the axon
                name_of_measurement = str(file.split('.')[0]) # set name of the measurement
                # set columns names 
                columns = ['Genotype', 'Sample', 'NameOfMeasurement', 'Time', 'CoordinateOfTip', 'Axon length ($\mu m$)', 'Speed from $t_{i-1}$ to $t_{i}$ ($\mu m / \text{sec}$)',
                    'Axon growth distance from $t_{i-1}$ to $t_{i}$ ($\mu m$)',  'Angle change from $t_{i-1}$ to $t_{i}$ (%)', 'Total growth during all time ($\mu m$)', 
                    'Total speed during all time ($\mu m / \text{sec}$)', 'Total angle change (%)']
                
                measurements = measure(growth_arr, measurements, columns, genotype, sample, name_of_measurement)

            # save measurements to CSV file
            output_path = os.path.join(res_dir, 'measurements.csv')
            logging.info(f"Saving measurements to {output_path}")
            pd.DataFrame(measurements).to_csv(output_path, index=False)

if __name__ == "__main__":
    main()