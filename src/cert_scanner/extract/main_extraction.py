import cert_scanner.extract.certificate_source as certificate_source
from cert_scanner.extract.test_certificate_source import TestCertificateSource

from datetime import datetime as dt

def extract_all_x509_certificates(use_demo, configuration_manager):
    """
    Considers whether the application is running in a demonstration or
    production setting and then attempts to identify certifificates that
    are going to expire in a date range (a year)
    Returns :
        all_certs_df: all the certificates that were identified
    """
    # Extract all the certificates, depending on whether this is
    # running in demonstration or a production setting
    all_certs_df = None
    if use_demo is True:
        current_time = dt.now()
        test_certificate_source = TestCertificateSource(current_time)
        all_certs_df = test_certificate_source.all_certs_df
    else:
        all_certs_df = \
            certificate_source.extract_certificates(
                configuration_manager.target_scanning_directory)


    if all_certs_df.empty:
        warning_message = ('No x509 certificates found '
                           'in target code directory {}. Check you '
                           'specified the right target_code_directory '
                           'in the configuration file.')
        raise ValueError(warning_message.format(
                configuration_manager.target_scanning_directory))

    print(('Identified {} x509 certificates in '
           'the directory {}\n\n').format(
                len(all_certs_df),
                configuration_manager.target_scanning_directory))

    return all_certs_df
