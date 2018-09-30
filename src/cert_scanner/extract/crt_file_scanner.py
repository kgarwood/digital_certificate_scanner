import cert_scanner.system.certificate_summary_record as \
    certificate_summary_record
from cert_scanner.util.certificate_scanner_utility import \
    create_cert_from_identifier_dct as create_cert_from_identifier_dct

import os
import fnmatch
from cryptography import x509
from cryptography.hazmat.backends import default_backend

CRT_FILTER = "*.crt"


def extract_certificates(target_directory):
    cert_summary_dct_lst = []
    for root, directories, file_names in os.walk(target_directory):
        for file_name in file_names:
            if fnmatch.fnmatch(file_name, CRT_FILTER):
                current_crt_path = os.path.join(root, file_name)
                try:
                    cert_summary_dct = \
                        extract_cert_from_crt_file(current_crt_path)
                    cert_summary_dct_lst.append(cert_summary_dct)
                except Exception as e:
                    pass

    return create_cert_from_identifier_dct(cert_summary_dct_lst)


def extract_cert_from_crt_file(current_crt_path):
    # Expects a *.crt file to only contain a single PEM data certificate
    # Note the format will resemble will have the form:
    # -----BEGIN CERTIFICATE-----
    # der format text
    # -----END CERTIFICATE-----
    with open(current_crt_path, 'r') as stream:
        encoded_data = stream.read()
        certificate = \
            x509.load_pem_x509_certificate(str.encode(encoded_data),
                                           default_backend())
        cert_summary_dct = \
            certificate_summary_record.create(certificate,
                                              encoded_data,
                                              current_crt_path)
        return cert_summary_dct
