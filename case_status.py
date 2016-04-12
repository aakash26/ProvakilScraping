"""
A python funtion get_case_status to retrieve the case status from the url
based on the input parameters case_type,case_num and year. The scraper uses
mechanize browser and etree to scrape the details from the website.The data
is scrapped according to the xpath address of the specific values required.
"""

import sys
import mechanize
from lxml import etree

# the starting Url as give in problem definition
url = "http://courtnic.nic.in/supremecourt/casestatus_new/caseno_new.asp"


def get_case_status(case_type, case_num, year):
    try:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        html = br.open(url)
    except:
        print "unable to connect. Please check your internet connection"
        sys.exit()

    case = {}  # defining the dictionary for the case which will be the output
    conv_case = {}  # defining the dictionary for converted_case if available.
    br.select_form("caseno")   # selecting the main form on the website
    # selecting each form control and fill the values accordingLY..
    control = br.form.find_control("seltype")   # for case_type
    br[control.name] = [str(case_type)]
    control = br.form.find_control("selcyear")   # for year
    br[control.name] = [str(year)]
    control = br.form.find_control("txtnumber")   # for case_number
    br[control.name] = str(case_num)

    try:
        response = br.submit()
        tree = etree.HTML(response.read())
    except:
        print "unable to submit form. Please check internet"
        sys.exit()
    stxpath_addr = '//tr/td[3]/font/strong/text()'  # xpath address for status
    status = get_text_from_xpath(stxpath_addr, tree, 0)
    if(status == "DISPOSED"):
        flag = True
    else:
        flag = False
    case['Is_disposed'] = flag

    # xpath address for petioner's name
    petioner_xpath_addr = '//tr[2]/td[1]/font/text()'
    petioner_name = get_text_from_xpath(petioner_xpath_addr, tree, 0)
    if petioner_name:
        case['petioner'] = petioner_name  # adding the name to dictionary	    .
    else:
        case['petioner'] = "not available"

    # xpath address for respondent's name
    respondent_xpath_addr = '//tr[4]/td[1]/font/text()'
    respondent_name = get_text_from_xpath(respondent_xpath_addr, tree, 0)
    if respondent_name:
        case['respondent'] = respondent_name
    else:
        case['respondent'] = "not available"

    respondent_adv_xpath = '//tr[3]/td[2]/font/text()'
    respondent_adv_name = get_text_from_xpath(respondent_adv_xpath, tree, 0)
    if respondent_adv_name:
        case['res_advocate'] = respondent_adv_name
    else:
        case['res_advocate'] = "not available"

    petioner_adv_xpath_addr = '//tr[2]/td[2]/font/text()'
    petioner_adv_name = get_text_from_xpath(petioner_adv_xpath_addr, tree, 1)
    if petioner_adv_name:
        case['pet_advocate'] = petioner_adv_name
    else:
        case['pet_advocate'] = "not available"

    # xpath for converted case for a particular case
    converted_xpath_adr = '//tr[2]/td[1]/b/font/text()'
    convert_case = tree.xpath(converted_xpath_adr)
    # use try and except as not all cases will have the converted case value
    try:
        conv_list = str(convert_case[0]).split('/')
        conv_case['case_num'] = conv_list[0]
        conv_case['year'] = conv_list[1]
    except:
        pass
    # adding the converted case dictionary to case dictionary
    case['convert_case'] = conv_case

    print case

"""
The get_text_from_xpath returns the cleaned string value for a specified xpath.
 flag is used as petioner_adv needed to be differentiated.
"""


def get_text_from_xpath(xpath_addr, tree, flag):
    text = tree.xpath(xpath_addr)
    str_value = ''
    if(flag == 0):   # for all except petioner_advocate
        try:
            for string in text[2]:
                str_value = str_value + string
        except:
            for string in text:
                str_value = str_value + string
    else:
        for string in text:
            str_value = str_value + string
    return str_value.strip()   # returning a clean string value.

if __name__ == '__main__':
    case_type = sys.argv[1]  # get case_type from terminal
    case_num = sys.argv[2]  # get case_num from terminal
    year = sys.argv[3]  # get year from terminal
    get_case_status(case_type, case_num, year)
