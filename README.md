# X509 Certificate Scanner


The Certificate Scanner is a Python-based application that detects x509
certificates in files within a target directory.  It then produces
reports showing when a certificate will expire, what files it appears in
and what release activities may be associated with publishing changes.

This is a prototype application and its development is ongoing.  Most of the
documentation for this project will appear on its own Wiki.

# License
This code base is open sourced under the
[MIT License]: https://opensource.org/licenses/MIT.

## Invocation
There are two ways to invoke the application.  Follow these steps:

### Demonstration Mode
The scanner will generate a collection of fake x509 certificates in memory
and pretend as if it had read them from some target directory.  It will
generate reports in the directory ```certificate_scanner/report_results```

```
PYTHONPATH=. python3 ./cert_scanner/scanner.py --demo
```

This repository features an certificate scanner application that identifies
expiring digital certificates within a target directory and tells which
files they appear in.  

### Production Mode
In production mode, the application will scan a directory containing your
code repositories and output the results in a directory you specify. The
scanner depends entirely on a YML configuration file that is based on:
```
certificate_scanner/src/cert_scanner/demo_scanner_configuration.yml
```
Make a copy of it and adapt it to suit characteristics of your project.

```
PYTHONPATH=. python3 ./cert_scanner/scanner.py --configuration-path [path]
```

## Starting Point for Developers
The starting point in the code is
```
certificate_scanner/src/cert_scanner/scanner.py
```

To run the test cases:
```
./src/pre-commit.sh
```
