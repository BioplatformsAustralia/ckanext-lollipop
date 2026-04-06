[![Tests](https://github.com/BioplatformsAustralia/ckanext-lollipop/workflows/Tests/badge.svg?branch=main)](https://github.com/BioplatformsAustralia/ckanext-lollipop/actions)

# ckanext-lollipop

ckanext-lollipop is a CKAN extension that requires non-logged in users 
to complete a CAPTCHA to use CKAN and access pages that are expensive
to render.

Ideally, this will reduce the impact of bots and crawlers on the CKAN
install.

When logged in, users are not required to complete a CAPTCHA

## Naming inspiration

ckanext-lollipop is named after the guards that control pedestrian 
crossings - typically for school children

The intention of ckanext-lollipop is let the important traffic pass
(normal users) and stop undesired traffic (bots, crawlers)

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?            |
| --------------- | ---------------------- |
| 2.8 and earlier | not tested             |
| 2.9             | yes                    |
| 2.10            | yes, but still testing |
| 2.11 and later  | yes, but still testing |


## Installation

To install ckanext-lollipop:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/BioplatformsAustralia/ckanext-lollipop.git
    cd ckanext-lollipop
    pip install -e .
	pip install -r requirements.txt

3. Add `lollipop` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

ckanext-lollipop sets a cookie if the CAPTCHA has been completed
successfully.   This cookie has a default expiration of 

This can be adjusted with the following config setting to control how
often a non-logged in user is required to complete the CAPTCHA.

        # ckanext-lollipop Expiry duration of the CAPTCHA cookie in days
        ckanext.lollipop.cookie_expiry = 7

The following setting is the name of the cookie that is set:

        # ckanext-lollipop CAPTCHA cookie name
        ckanext.lollipop.cookie_name = ckanext-lollipop-yum


## Developer installation

To install ckanext-lollipop for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/BioplatformsAustralia/ckanext-lollipop.git
    cd ckanext-lollipop
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Developer installation

To install ckanext-lollipop for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/BioplatformsAustralia/ckanext-lollipop.git
    cd ckanext-lollipop
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-lollipop

If ckanext-lollipop should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## Acknowledgements

This work was supported by Bioplatforms Australia.

Bioplatforms Australia is made possible through investment funding provided
by the Commonwealth Government National Collaborative Research
Infrastructure Strategy (NCRIS).

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
