# Security and fabrication safety policy

## Supported code

Security fixes are applied to the current default branch. Historical commits and generated layout files are not maintained as supported releases unless explicitly tagged and documented.

## Important trust boundary

`trapping_array_pcell.lym` is executable Python packaged as a KLayout macro. Importing or enabling a `.lym` file should therefore be treated as executing code on the local workstation.

Repository code must not introduce:

- network calls or telemetry;
- credential, token, browser-cookie or keychain access;
- arbitrary shell or subprocess execution;
- writes outside the documented KLayout macro installation directory or an explicitly selected output path;
- hidden persistence mechanisms;
- automatic upload of layouts, process data or machine information.

The current macro intentionally writes its embedded library modules under the user's KLayout macro directory during installation. That behavior must remain visible and documented.

## Sensitive design data

GDSII/OASIS files and process layouts may contain proprietary fabrication information. Generated layouts must not be committed by default. Review repository status before every push and keep confidential masks outside the repository.

## Engineering and fabrication boundary

The software is a geometry-generation aid. It is not a qualified foundry rule deck, process approval, safety interlock or fabrication authorization. Users remain responsible for DRC, process compatibility, material compatibility, device safety and institutional/foundry review.

## Reporting a vulnerability

Use GitHub private vulnerability reporting when it is enabled for this repository. Otherwise contact the repository owner privately through GitHub. Do not publish credentials, proprietary mask data or exploit details in a public issue before remediation is coordinated.
