# -*- coding: utf-8 -*-

from __future__ import (division,
                        absolute_import,
                        print_function,
                        unicode_literals)

import datetime
import re
from urllib.parse import urljoin, urlsplit

from lxml import etree
import requests


def get_nc_urls(thredds_url):
    caturl = thredds_url.replace('.html', '.xml')

    parsed_uri = urlsplit(caturl)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    response = requests.get(caturl)
    ROOT = etree.XML(response.content)
    dataset_el = list(filter(lambda x: re.match(r'(.*?.nc$)', x.attrib['urlPath']) is not None,
                             ROOT.xpath('//*[contains(@urlPath, ".nc")]')))

    service_el = ROOT.xpath('//*[contains(@name, "odap")]')[0]

    dataset_urls = [urljoin(domain, urljoin(service_el.attrib['base'], el.attrib['urlPath'])) for el in
                    dataset_el]  # noqa

    return dataset_urls


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds() * 1000)


def datetime_to_string(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
