import cert_scanner.system.certificate_summary_record as \
    certificate_summary_record
from cert_scanner.util.certificate_scanner_utility import \
    create_cert_from_identifier_dct as create_cert_from_identifier_dct

from cryptography import x509
from cryptography.hazmat.backends import default_backend
import yaml
import base64
import os
import fnmatch

YML_FILTER = "*.yml"


def extract_certificates(target_directory):
    """
    This routine scans the target directory for any YAML file ending in *.yml
    which meets two conditions:
       (1) It contains an encryption certificate through a top level tag like
           this:
            encryptionCertificate:
                x509: [encoded der text representing an encryption certificate]
       (2) It contains at least one signing certificate through a top level tag
           like this:
            signatureVerificationCertificates:
                - x509: [encoded der text representing a signing certificate]
                ...
                ...

    If these two conditions are met, then the digital certificates are included
    in a dictionary that hashes certs based on a unique identifier, which is a
    combination of [serial number] + [certificate authority] attributes that
    are read from the x509 cert data structure.

    Note that the same certificate may appear in multiple configuration files.
    This routine combines all of the configuration files that a cert
    appears in.
    """
    # Part 1: Identify all encryption and signing certificates in valid
    # service configuration YML files.
    crt_from_file_path = dict()
    cert_summary_dct_lst = []
    for root, directories, file_names in os.walk(target_directory):
        for file_name in file_names:
            if fnmatch.fnmatch(file_name, YML_FILTER):
                current_yml_path = os.path.join(root, file_name)
                current_yml_file_cert_lst = \
                    extract_cert_from_yml_file(
                        current_yml_path,
                        crt_from_file_path)
                cert_summary_dct_lst.extend(current_yml_file_cert_lst)

    # Part 2: Produce a dictionary that hashes the unique identifier of a
    # cert with the cert data structure.  Whenever it determines that the
    # dictionary already contains an entry for an identifier, it will add the
    # file locations together.
    return create_cert_from_identifier_dct(cert_summary_dct_lst)


def extract_cert_from_yml_file(yml_file_path, crt_from_file_path):
    # Expects a *.yml configuration files which will contain two tags:
    #     signatureVerificationCertificates:
    #         - x509: [der text for cert 1]
    #         - x509: [der text for cert 2]
    #         - x509: [der text for cert n]
    #
    #     encryptionCertificate:
    #         x509: [der text for a cert]
    #
    # Assuming a *.yml file contains both of these tags, it will decode the
    # der text for each x509 certificate and produce a
    # certificate_summary_record
    cert_lst = []
    try:
        with open(yml_file_path, 'r') as stream:
            config_data = yaml.load(stream)
            encryption_cert, encoded_data = \
                extract_encryption_cert(config_data)
            signing_cert_from_data_dct = \
                extract_signing_certs(config_data)

            # if we manage to obtain encryption and signing signatures
            # without any exceptions being thrown, then we can be confident
            # that we have encountered a service configuration file
            encryption_cert_summary_dct = \
                certificate_summary_record.create(encryption_cert,
                                                  encoded_data,
                                                  yml_file_path)
            cert_lst.append(encryption_cert_summary_dct)

            for encoded_data in signing_cert_from_data_dct:
                signing_cert = signing_cert_from_data_dct[encoded_data]
                signing_cert_summary_dct = \
                    certificate_summary_record.create(signing_cert,
                                                      encoded_data,
                                                      yml_file_path)
                cert_lst.append(signing_cert_summary_dct)

        return cert_lst

    except Exception as e:
        # We don't care what problems YML files have if they don't have
        # signature or encryption attributes
        pass
    return cert_lst


def extract_encryption_cert(config_file_data):
    encryption_certificate = config_file_data['encryptionCertificate']
    encryption_encoded_data = encryption_certificate['x509']
    x509_bytes = base64.b64decode(encryption_encoded_data)
    cert = x509.load_der_x509_certificate(x509_bytes, default_backend())
    return (cert, encryption_encoded_data)


def extract_signing_certs(config_file_data):
    cert_from_data_dct = dict()
    signing_certs = config_file_data['signatureVerificationCertificates']
    for signing_cert in signing_certs:
        signing_encoded_data = signing_cert['x509']
        x509_bytes = base64.b64decode(signing_encoded_data)
        cert = x509.load_der_x509_certificate(x509_bytes, default_backend())
        cert_from_data_dct[signing_encoded_data] = cert
    return cert_from_data_dct
