import cert_scanner.system.certificate_summary_record as \
    certificate_summary_record
from cert_scanner.extract.certificate_consolidator import \
    combine_unique_cert_collections

import pandas as pd
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
# from datetime import timedelta
import datetime

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

class TestCertificateSource:
    def __init__(self, current_time=None):
        self.current_time = current_time
        self.certificate_lst = []

            # serial_number=x509.random_serial_number(),

        # Adding expired certificate reference
        self.add_summary_record(
            6565,
            -50,
           'JT',
           'Hades',
           'River Styx',
           'Charons not Carin',
           'Three Headed Dawg Ltd.',
           'encryption certifcate for TXW',
           '~/code/my_app_repo1/prod/TXW_service_config.yml')

        self.add_summary_record(
            6565,
            -50,
           'JT',
           'Hades',
           'River Styx',
           'Charons not Carin',
           'Three Headed Dawg Ltd.',
           'encryption certifcate for TXW',
           '~/code/my-main-cert-directory/TXW_enc.crt')

        self.add_summary_record(
            808,
            6,
           'JT',
           'BrambleShire',
           'Sticks-upon-Stones',
           'Sphinx Cryptically',
           'Department of Making Certs Rock',
           'SGN cert for another fine service for ABC',
           '~/code/my_app_repo1/prod/ABC_service_config.yml')

        self.add_summary_record(
            808,
            6,
           'JT',
           'BrambleShire',
           'Sticks-upon-Stones',
           'Sphinx Cryptically',
           'Department of Making Certs Rock',
           'SGN cert for another fine service for ABC',
           '~/code/my-main-cert-directory/ABC_v3-4-5.crt')

        self.add_summary_record(
            111,
            20,
           'XY',
           'OakShire',
           'Oakville',
           'Certainly Clever',
           'Cert Issuing Authority',
           'SIGNING cert for service x',
           '~/code/my_app_repo1/servicex_signing.crt')

        self.add_summary_record(
            111,
            20,
           'XY',
           'OakShire',
           'Oakville',
           'Certainly Clever',
           'Cert Issuing Authority',
           'SIGNING cert for service x',
           '~/code/my_app_repo2/x_sgn2.crt')

        self.add_summary_record(
            111,
            20,
           'XY',
           'OakShire',
           'Oakville',
           'Certainly Clever',
           'Cert Issuing Authority',
           'SIGNING cert for service x',
           '~/code/my_app_repo2/my_service_prod.yml')


        self.add_summary_record(
            111,
            20,
           'XY',
           'OakShire',
           'Oakville',
           'Certainly Clever',
           'Cert Issuing Authority',
           'SIGNING cert for service x',
           '~/code/my-main-cert-directory/x_x09.crt')

        self.add_summary_record(
            222,
            24,
           'ZZ',
           'Pineshire',
           'Pineville',
           'The Other Guys',
           'Cert Issuing Authority',
           'ENCRYPTION certificate for test QQRR',
           '~/code/my-app-repo-without-release-process/xyz.crt')

        self.add_summary_record(
            222,
            24,
           'ZZ',
           'Pineshire',
           'Pineville',
           'The Other Guys',
           'Cert Issuing Authority',
           'ENCRYPTION certificate for test QQRR',
           '~/code/test/my_xyz_config.yml')

        self.add_summary_record(
            222,
            24,
           'ZZ',
           'Pineshire',
           'Pineville',
           'The Other Guys',
           'Cert Issuing Authority',
           'ENCRYPTION certificate for test QQRR',
           '~/code/my-main-cert-directory/my_xyz_config.yml')


        self.add_summary_record(
            333,
            26,
           'QQ',
           'Elmshire',
           'Elmwood',
           'Another Bunch',
           'CIA',
           'ENCRYPT certificate for prod',
           '~/code/my_app_repo2/test/my_xyz_config.yml')


        self.add_summary_record(
            454,
            26,
           'QQ',
           'Elmshire',
           'Elmwood',
           'Another Bunch',
           'CIA',
           'ENCRYPT certificate for prod',
           '~/code/my_app_repo2/test/my_xyz_config.yml')

        # Adding an unreferenced certificate
        self.add_summary_record(
            9991999,
            88,
           'JT',
           'Pacific Ocean',
           'HMS Bounty',
           'Orphaned Certs Ltd. Thankfully.',
           'Lone Certainty Division',
           'encryption certifcate for Bligh',
           '~/code/my-main-cert-directory/Bligh_enc.crt')

        self.add_summary_record(
            770007,
            180,
           'JT',
           'Pomegranate World',
           'Many-out-of-Reach',
           'Fruitful Discussions Ltd.',
           'Swipe Cards and Certs Dept.',
           'encryption cert for another fine service for YRYR',
           '~/code/my_app_repo1/prod/YRYR_service_config.yml')

        self.add_summary_record(
            770007,
            180,
           'JT',
           'Pomegranate World',
           'Many-out-of-Reach',
           'Fruitful Discussions Ltd.',
           'Swipe Cards and Certs Dept.',
           'encryption cert for another fine service for YRYR',
           '~/code/my_app_repo1/prod/YRYR.crt')


        self.add_summary_record(
            454,
            260,
           'TY',
           'BrookShire',
           'BrookVille',
           'Yet Another Company Co.',
           'Division A',
           'ENCRYPT certificate for test service R454',
           '~/code/my_app_repo2/test/R454_config.yml')

        self.add_summary_record(
            454,
            260,
           'TY',
           'BrookShire',
           'BrookVille',
           'Yet Another Company Co.',
           'Division A',
           'ENCRYPT certificate for test service R454',
           '~/code/my-main-cert-directory/test/R454.crt')

        self.all_certs_df = self.consolidate_certificates()


    def get_certificates(self):
        certificates_df = pd.DataFrame(self.certificate_lst)
        return certificates_df

    def consolidate_certificates(self):
        all_certificates_dct = dict()
        for certificate_dct in self.certificate_lst:
            current_serial_number = certificate_dct['serial_number']
            if current_serial_number in all_certificates_dct:
                existing_certificate_dct = \
                    all_certificates_dct[current_serial_number]
                existing_certificate_dct['locations'] = \
                    existing_certificate_dct['locations'].union(
                        certificate_dct['locations'])
            else:
                all_certificates_dct[current_serial_number] = \
                    certificate_dct

        unique_certificates_lst = []
        for serial_number in all_certificates_dct:
            current_certificate_dct = all_certificates_dct[serial_number]
            unique_certificates_lst.append(current_certificate_dct)

        unique_certificates_df = pd.DataFrame(unique_certificates_lst)
        return unique_certificates_df

    def add_summary_record(self,
                           serial_number,
                           days_to_expire,
                           country_name,
                           state_or_province_name,
                           locality,
                           organisation,
                           organisational_unit,
                           common_name,
                           file_path):

        x509_certificate = \
            self.create_x509_certificate(serial_number,
                                         days_to_expire,
                                         country_name,
                                         state_or_province_name,
                                         locality,
                                         organisation,
                                         organisational_unit,
                                         common_name)
        summary_certificate_record_dct = \
            certificate_summary_record.create(x509_certificate,
                                              'asdfklsdfjskdf',
                                              file_path)

        self.certificate_lst.append(summary_certificate_record_dct)


    def create_x509_certificate(self,
                                serial_number,
                                days_to_expire,
                                country_name,
                                state_or_province_name,
                                locality,
                                organisation,
                                organisational_unit,
                                common_name):

        one_day = datetime.timedelta(1, 0, 0)
        private_key = rsa.generate_private_key(public_exponent=65537,
                                               key_size=2048,
                                               backend=default_backend())
        public_key = private_key.public_key()

        issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME,
                               country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME,
                               state_or_province_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME,
                               locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME,
                               organisation),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME,
                               organisational_unit),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])

        not_before_time = self.current_time - one_day
        not_after_time = self.current_time + (one_day * days_to_expire)

        certificate_builder = x509.CertificateBuilder(
            issuer_name=issuer, subject_name=issuer,
            public_key=private_key.public_key(),
            serial_number=serial_number,
            not_valid_before=not_before_time,
            not_valid_after=not_after_time)

        certificate = certificate_builder.sign(private_key=private_key,
                                               algorithm=hashes.SHA256(),
                                               backend=default_backend())

        return certificate
