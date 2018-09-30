from cryptography.x509.oid import NameOID
import datetime
import os.path

"""
This module contains code that creates a certificate summary record.
A record includes these parts:
(1) attributes for the certificate record such as serial number,
    organisation, certificate authority etc.
(2) a set of locations for files that contain the certificate record
(3) the encoded data block that was decoded to obtain the certificate
    record
"""


def create(cert, encoded_data, file_path):

    certificate_summary_dct = dict()
    certificate_summary_dct['serial_number'] = str(cert.serial_number)
    certificate_summary_dct['required_releases'] = set()
    certificate_summary_dct['expiry_date'] = cert.not_valid_after
    certificate_summary_dct['days_left'] = \
        (cert.not_valid_after - datetime.datetime.now()).days
    certificate_summary_dct['data'] = encoded_data

    certificate_summary_dct['file_extension_type'] = \
        (os.path.splitext(file_path)[1]).lower()

    try:
        certificate_summary_dct['certificate_authority'] = \
            cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    except Exception as e:
        certificate_summary_dct['certificate_authority'] = 'Unknown'

    certificate_summary_dct['identifier'] = \
        certificate_summary_dct['certificate_authority'] + \
        certificate_summary_dct['serial_number']

    try:
        certificate_summary_dct['organisation_name'] = \
            cert.subject.get_attributes_for_oid(
                NameOID.ORGANIZATION_NAME)[0].value
    except Exception as e:
        certificate_summary_dct['organisation_name'] = 'Unknown'

    # certificate_summary_dct['type'] = \
    #     __derive_cert_type(certificate_summary_dct['certificate_authority'])

    # Initially a set will contain just one file path.  Later on when
    # the certificate summary records are consolidated, one record will
    # exist for each serial number and all the file paths will be combined
    certificate_summary_dct['locations'] = set()
    certificate_summary_dct['locations'].add(file_path)
    return certificate_summary_dct
