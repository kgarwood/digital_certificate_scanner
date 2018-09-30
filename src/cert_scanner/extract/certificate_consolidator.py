def combine_unique_cert_collections(all_certfificates_dct,
                                    current_certificates_dct):

    for serial_number in current_certificates_dct:
        if serial_number in all_certfificates_dct:
            # Preserve certificate record in the master dictionary but
            # add all the file locations that are known from occurences in
            # the other cert_dict
            all_certificate_dct = \
                all_certfificates_dct[serial_number]
            current_certificate_dct = current_certificates_dct[serial_number]

            all_certificate_dct['locations'] = \
                all_certificate_dct['locations'].union(
                    current_certificate_dct['locations'])

            all_certificate_dct['required_releases'] = \
                all_certificate_dct['required_releases'].union(
                    current_certificate_dct['required_releases'])

        else:
            all_certfificates_dct[serial_number] = \
                current_certificates_dct[serial_number]
