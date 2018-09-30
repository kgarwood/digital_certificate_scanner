
import cert_scanner.util.certificate_scanner_utility as \
    certificate_scanner_utility


def test_list_with_duplicate_identifiers():
    cert_summary1_dct = dict()
    cert_summary1_dct['serial_number'] = '101'
    cert_summary1_dct['locations'] = {'c', 'd', 'e'}

    cert_summary2_dct = dict()
    cert_summary2_dct['serial_number'] = '101'
    cert_summary2_dct['locations'] = {'a', 'b', 'c', 'd'}

    cert_summary3_dct = dict()
    cert_summary3_dct['serial_number'] = '301'
    cert_summary3_dct['locations'] = {'f', 'g'}

    cert_summary_dct_lst = \
        [cert_summary1_dct, cert_summary2_dct, cert_summary3_dct]

    cert_from_identifier_dct = \
        certificate_scanner_utility.create_cert_from_identifier_dct(
            cert_summary_dct_lst)

    assert len(cert_from_identifier_dct) == 2

    actual_101_locations = cert_from_identifier_dct['101']['locations']
    expected_101_locations = {'a', 'b', 'c', 'd', 'e'}
    assert actual_101_locations == expected_101_locations

    actual_301_locations = cert_from_identifier_dct['301']['locations']
    expected_301_locations = {'f', 'g'}
    assert actual_301_locations == expected_301_locations
