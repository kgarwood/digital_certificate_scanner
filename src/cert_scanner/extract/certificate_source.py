import cert_scanner.system.certificate_summary_record as \
    certificate_summary_record
import cert_scanner.extract.crt_file_scanner as crt_file_scanner
import cert_scanner.extract.yml_file_scanner as yml_file_scanner
from cert_scanner.extract.certificate_consolidator import \
    combine_unique_cert_collections

import pandas as pd

"""
This module scans a target directory and uses multiple methods to
identify digital certificate data in directory files.  For now, these
methods are:
(1) identify certificates in *.crt files that contain certificate
    records expressed as PEM data
(2) identify certificates in *.yml files that have certificate
    records expresses as DER data in attribute headings for
    'signatureVerificationCertificates' and
    'encryptionCertificate'

Each method returns a dictionary stucture that hashes a certificate's
serial number to a certificate_summary_record.  It's possible that the
same certificate record may appear in multiple files and may be returned
by multiple methods.

This module consolidates all of the dictionaries to create a single
dictionary, where each serial number corresponds to one
certificate_summary_record which may combine the file locations supplied
by the methods used to identify the certificates.
"""


def extract_certificates(target_directory_path):
    crt_based_certificates_dct = \
        crt_file_scanner.extract_certificates(target_directory_path)
    yml_based_certificates_dct = \
        yml_file_scanner.extract_certificates(target_directory_path)

    all_certificates_dct = dict()
    combine_unique_cert_collections(
        all_certificates_dct,
        crt_based_certificates_dct)
    combine_unique_cert_collections(
        all_certificates_dct,
        yml_based_certificates_dct)

    # Convert the dictionary to a data frame
    certificate_record_lst = []
    for identifier in all_certificates_dct:
        certificate_record_lst.append(all_certificates_dct[identifier])
    unique_certificates_df = pd.DataFrame(certificate_record_lst)
    return unique_certificates_df
