import json
import re


def process_gpt_response(test_string):
    test_string = test_string.replace('```json', '')
    test_string = test_string.replace('```', '')
    pattern = re.compile('//(?<=//).*?(?=\n)\n')
    test_string = pattern.sub('\n', test_string)
    test_string = test_string.strip()
    res = json.loads(test_string)
    return res

if __name__ == "__main__":



    test_string = """
    {
        "irrelevant organizations": [],
        "relevant organizations": [
            {"501c3 nonprofit organization": "SUP30"},
            {"Austin community": "SUP2025"},
            {"Houston community": "SUP2025"}
        ],
        "irrelevant products": [],
        "relevant products": [
            {"women’s health clinics": "SUP2025"},
            {"reproductive health and pregnancy care": "SUP2025"}
        ]
    }
    """
    test_string = """
    {
    "irrelevant organizations": [],
    "relevant organizations": [
        {"Badger Wire, Inc.": ["000040", "Businesses"]}
    ],
    "irrelevant products": [],
    "relevant products": [
        {"large gauge wire": ["45203015", "Electronic Components"]},
        {"tubing": ["20106020", "Industrial Machinery"]},
        {"multi-conductor wire products": ["45203015", "Electronic Components"]},
        {"battery cable": ["45203015", "Electronic Components"]}
        ]
    }
    """

    # test_string = """```json
    # {
    #     "irrelevant organizations": [],
    #     "relevant organizations": [
    #         {"San Francisco community": "SUP10"},
    #         {"Bay Area food trucks": "SUP40"},
    #         {"private events of all sizes": "SUP10"},
    #         {"your company": "SUP40"},
    #         {"private party": "SUP10"}
    #     ],
    #     "irrelevant products": [],
    #     "relevant products": [
    #         {"food trucks": "25301040"},  // Restaurants
    #         {"covered heated seating": "SUP10"},
    #         {"free WiFi": "45203020"},  // Internet Services & Infrastructure
    #         {"beer garden": "25301040"},  // Restaurants
    #         {"big screen TVs movie nights": "25301040"},  // Restaurants
    #         {"sporting games": "25301040"},  // Restaurants
    #         {"off-site catering": "25301040"}  // Restaurants
    #     ]
    # }
    # ```"""

    res = process_gpt_response(test_string)

    # print result
    print("The converted dictionary : " + str(res))
    print('-------------------------------------\n')

    irrelevant_organizations = res['irrelevant organizations']
    relevant_organizations = res['relevant organizations']
    irrelevant_products = res['irrelevant products']
    relevant_products = res['relevant products']

