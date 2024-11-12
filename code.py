import argparse
from pathlib import Path

from pygrpm.dicom.sr import make_sr_from_text
from pygrpm.dicom import DicomReader

def find_dicom_files(path):

    reader = DicomReader(path)
    return reader.build_dicom_list()

def make_sr_file(dicom_list,output_path):

    # Make SR DICOM dataset from text
    sr_with_text = make_sr_from_text(text=f'Hello {dicom_list[0].PatientID}', dicom_to_refer=dicom_list)

    # Afterward, can be written to a file like this:
    sr_with_text.save_as(Path(output_path) / './example_sr.dcm')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Your script description.")
    parser.add_argument("--input_path", type=str, required=True, help="Path to the input data")
    parser.add_argument("--output_path", type=str, required=True, help="Path to where the output should be saved")
    parser.add_argument("--series_instance_uid", type=str, required=False, help="Unique identifier for the series")
    args = parser.parse_args()

    # args.series_instance_uid is not used in this example
    # Generate a list of dicom data in the input directory
    dicom_list=find_dicom_files(args.input_path)

    # Generate a hello world SR File
    make_sr_file(dicom_list,args.output_path)
