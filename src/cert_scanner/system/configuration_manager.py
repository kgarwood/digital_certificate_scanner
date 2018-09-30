import yaml
import os

class ConfigurationManager:
    """
    Extracts options from a configuration file which are used to
    drive the scanner application.
    """

    def __init__(self, configuration_file_path):

        if not os.path.exists(configuration_file_path):
            error_message = ('The configuration file path {} '
                             'does not exist')
            raise ValueError(error_message.format(configuration_file_path))
            os.makedirs(output_directory)

        with open(configuration_file_path, 'r') as stream:
            scanner_configuration_data = yaml.load(stream)

            self.release_instructions = \
                scanner_configuration_data['release_instructions']
            self.main_certificate_directory = \
                scanner_configuration_data['main_certificate_directory']
            self.repos_with_releases = \
                scanner_configuration_data['repositories_with_releases']

            self.release_command_for_repository = dict()
            for repo in self.repos_with_releases:
                name = repo['repository_with_release']['name']
                release_command = \
                    repo['repository_with_release']['release_command']
                self.release_command_for_repository[name] = \
                    release_command

            self.repos_without_releases = set()
            for repo in scanner_configuration_data['repositories_without_releases']:
                self.repos_without_releases.add(repo['repository_without_release'])

            self.certificate_types = \
                self.process_all_certificate_types(
                    scanner_configuration_data['certificate_types'])
            self.environments= \
                self.process_all_environments(
                    scanner_configuration_data['environment_types'])
            self.target_scanning_directory = \
                self.create_canonical_directory_path(
                    scanner_configuration_data['target_scanning_directory'])
            if not os.path.exists(self.target_scanning_directory):
                error_message = ('The target directory {},'
                                 'which is where you keep all your '
                                 'code repositories - does not exist!')
                raise ValueError(error_message.format(
                                    self.target_scanning_directory))
            self.reports_output_directory = \
                self.create_canonical_directory_path(
                    scanner_configuration_data['reports_output_directory'])


    def create_canonical_directory_path(self, file_path):
        """
        Ensures that if a directory path begins with a tilda it will
        be properly expanded
        """
        if file_path.startswith("~"):
            return os.path.expanduser(file_path)
        else:
            return file_path

    def is_in_main_certificate_directory(self, file_path):
        return(self.main_certificate_directory in file_path)

    def get_release_for_file(self, file_path):
        for repository_name in self.release_command_for_repository:
            if repository_name in file_path:
                return self.release_command_for_repository[repository_name]

        for repository_name in self.repos_without_releases:
            if repository_name in file_path:
                return None

        unknown_release_message = ('Unknown release process for {}. '
                                   'Ask a colleague.')
        return(unknown_release_message.format(file_path))


    def process_all_certificate_types(self, certificate_type_data):
        certificate_types_dct = dict()
        for certificate_type_details in certificate_type_data:
            certificate_types_dct[certificate_type_details['type']] = \
                certificate_type_details['patterns']

        return certificate_types_dct

    def process_all_environments(self, certificate_environment_data):
        environments_dct = dict()
        for environment_details in certificate_environment_data:
            environment = environment_details['environment']
            environment_patterns = environment_details['patterns']
            environments_dct[environment] = environment_patterns
        return environments_dct

    def process_all_certificate_types(self, certificate_type_data):
        certificate_type_dct = dict()
        for certificate_type_details in certificate_type_data:
            certificate_type = certificate_type_details['type']
            certificate_type_patterns = certificate_type_details['patterns']
            certificate_type_dct[certificate_type] = certificate_type_patterns
        return certificate_type_dct


    def determine_certificate_type(self, description_field):
        canonical_field_value = description_field.upper()
        for certificate_type in self.certificate_types:
            pattern_lst = self.certificate_types[certificate_type]
            for pattern in pattern_lst:
                if pattern in canonical_field_value:
                    return certificate_type
        return 'Unknown certificate type'

    def determine_environment(self, description_field, file_paths):
        canonical_field_value = description_field.upper()
        for environment in self.environments:
            pattern_lst = self.environments[environment]
            for pattern in pattern_lst:
                canonical_pattern = pattern.upper()
                if canonical_pattern in canonical_field_value:
                    return environment
                else:
                    for file_path in file_paths:
                        if canonical_pattern in file_path.upper():
                            return environment

        return 'Unknown environment'


def create_configuration_manager(use_demo, configuration_file_path):
    """
    Uses the command line arguments passed to the scanner application to
    determine whether the configuration file should be used to match
    the demonstration activity or the production activity
    """
    configuration_manager = None
    if use_demo is True:
        demo_configuration_path = ('./cert_scanner/config/'
                                   'demo_scanner_configuration.yml')
        configuration_manager = \
            ConfigurationManager(demo_configuration_path)
    else:
        configuration_manager = ConfigurationManager(configuration_file_path)
    return configuration_manager
