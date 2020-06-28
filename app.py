import validators
from flask import Flask
from lxml import html
import json
from flask import Response
import requests
app = Flask(__name__)


def getHelpUrl(urlString):
    info = requests.get(urlString)
    treeDet = html.fromstring(info.content)
    valid = validators.url(treeDet.xpath(
        '//div[@class="section specs"]/div[@class="field"][2]/span/a/@href')[0])

    if valid == True:
        return treeDet.xpath('//div[@class="section specs"]/div[@class="field"][2]/span/a/@href')[0]

    else:
        return treeDet.xpath('//div[@class="section specs"]/div[@class="field"][1]/span/a/@href')[0]


@app.route('/<name>')
def hello(name):
    page = requests.get(
        'https://www.programmableweb.com/category/all/apis?keyword='+name)
    tree = html.fromstring(page.content)
    # This will create a list of buyers:
    data = {}
    apis = tree.xpath('//tr[@class="odd"]')
    apisev = tree.xpath('//tr[@class="even"]')
    for api in apis:
        info = []

        buyers = api.xpath(
            './/td[@class="views-field views-field-pw-version-title"]/a/text()')
        links = api.xpath(
            './/td[@class="views-field views-field-pw-version-links"]/a/@href')
        if len(links) > 0:
            absolute_url = f"https://www.programmableweb.com{links[0]}"
            info.append(getHelpUrl(absolute_url))
        else:
            absolute_url = ""
        info.append(buyers[0])
        description = api.xpath(
            './/td[@class="views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8"]/text()')
        str1 = name
        info.append(str1.join(description))

        data[buyers[0]] = info
    for api in apisev:
        info = []
        buyers = api.xpath(
            './/td[@class="views-field views-field-pw-version-title"]/a/text()')

        description = api.xpath(
            './/td[@class="views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8"]/text()')
        str1 = name
        links = api.xpath(
            './/td[@class="views-field views-field-pw-version-links"]/a/@href')
        if len(links) > 0:
            absolute_url = f"https://www.programmableweb.com{links[0]}"
            info.append(getHelpUrl(absolute_url))
        else:
            absolute_url = ""
        info.append(buyers[0])
        info.append(str1.join(description))

        data[buyers[0]] = info
    return Response(json.dumps(data),  mimetype='application/json')


if __name__ == '__main__':
    app.run()
