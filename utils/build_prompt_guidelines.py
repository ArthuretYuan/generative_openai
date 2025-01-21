# TO BE FINISHED !!!!


def build_prompt(prompt_version):
    mode = prompt_version['mode']
    mapping_level = prompt_version['mapping_level']
    step_one_version = prompt_version['step_one_version']
    step_two_version = prompt_version['step_two_version']
    
    # Select standard
    if mapping_level == 'L1':
        input_file = './data/classfication/txt_format/categories_codes_1level_with_public_sectors.txt'
    elif mapping_level == 'L3':
        input_file = './data/classfication/txt_format/categories_codes_3level_with_public_sectors.txt'
    f = open(input_file, "r")
    file = str(f.read())
    file_list = file.split('\n')
    new_file_list = []
    for line in file_list:
        line = line.replace(' ', ': ', 1)
        new_file_list.append(line)
    classification_standard = ('\n').join(new_file_list)
    
    input_file_guidelines = './data/classfication/txt_format/categories_codes_1level_with_new_guidelines.txt'
    f = open(input_file_guidelines, "r")
    guidelines = str(f.read())
    
    # Build prompt
    prompt_1 = ""
    prompt_2 = ""
    if mode == 'one_step_mode':
        if mapping_level == 'L1':
            prompt_1 = f"""You will be provided with the description about a company delimited by triple quotes. \
            Your objective is to categorize the company into its corresponding 'target market' category based on its description. \
            The 'target market' refers to the industry sectors that a company serves. \
            Attributes of a company: \
            (a) 'relevant organizations': Organizations, individuals, or entities that the given company currently directly serves. \
            (b) 'irrelevant organizations': Competitors, suppliers, indirect customers (e.g., clients of clients), previously served clients, and any organizations not currently directly served by the company. \
            (c) 'relevant products': the products, services, or solutions directly and currently offered by the given company. \
            (d) 'irrelevant products': Products from clients, competitors, suppliers, discontinued products, and any products not directly provided by the company. \
            The full 'target market' taxonomy with the codes are given as follows: \
            {classification_standard} \
            Use the following step-by-step instructions to generate the response: \
            Step 1 - Extract the four defined attributes from the company's description.  \
            Step 2 - Preserve the extracted attributes exactly as in the description, without rephrasing or inference. \
            Step 3 - Any attribute can be an empty list if the corresponding information cannot be extracted. \
            Step 4 - Map each organization in 'relevant organizations' to the most suitable 'target market' classification in the given taxonomy. \
            Step 5 - For each product in 'relevant products,' determine the most suitable 'target market' classification in the given taxonomy for the probable users.
            Step 6 - Present the 'target market' as the 2-digit code in the given taxonomy whenever possible. \
            Step 7 - Provide the response as a dictionary adhering to the specified format without comments or explanations. \
            Provide output in the dictionary format as follows: \
            {{
                "irrelevant organizations": [organization1, organization2, ...],
                "relevant organizations": [
                    {{"organization1": [mapping_code1, classification1]}},
                    {{"organization2": [mapping_code2, classification2]}},
                    ...
                ],
                "irrelevant products": [product1, product2, ...],
                "relevant products": [
                    {{"product1": [mapping_code1, classification1]}},
                    {{"product2": [mapping_code2, classification2]}},
                    ...
                ]
            }} \
            """
        elif mapping_level == 'L3':
            prompt_1 = f"""You will be provided with the description about a company delimited by triple quotes. \
            Your objective is to categorize the company into its corresponding 'target market' category based on its description. \
            The 'target market' refers to the industry sectors that a company serves. \
            Attributes of a company: \
            (a) "relevant organizations": Organizations, individuals, or entities that the given company currently directly serves. \
            (b) "irrelevant organizations": (1) Competitors, suppliers, indirect customers (e.g., clients of clients); (2) previously served clients; (3) any organizations not currently directly served by the company. \
            (c) "relevant products": the specific products, services, or solutions originally, directly and currently offered by the given company. \
            (d) "irrelevant products": (1) Products are not original to our company (such as free WIFI, venues, events, etc.); (2) general services (such as food, accomodation, gaming services, etc.); (3) discontinued products; (4) products from clients, competitors and suppliers; (5) any products not directly provided by the company. \
            The full 'target market' taxonomy with the codes are given as follows: \
            {classification_standard} \
            Use the following step-by-step instructions to generate the response: \
            Step 1 - Extract the four defined attributes from the company's description.  \
            Step 2 - Preserve the extracted attributes exactly as in the description, without rephrasing or inference. \
            Step 3 - Any attribute can be an empty list if the corresponding information cannot be extracted. \
            Step 4 - Map each organization in 'relevant organizations' to the most suitable 'target market' classification in the given taxonomy. \
            Step 5 - For each product in 'relevant products,' determine the most suitable 'target market' classification in the given taxonomy for the probable users.
            Step 6 - Present the 'target market' as the 6-digit code in the given taxonomy whenever possible. \
            Step 7 - If no suitable 'target market' with an 6-digit code is found, resort to the upper level with 2 or 4-digit codes accordingly. \
            Step 8 - If the extraction in 'relevant organizations' is general ('clients,' 'customers,' 'users'), assign one of the following codes: "0010", "0020", "0030". \
            Step 9 - Provide the response as a dictionary adhering to the specified format without comments or explanations. \
            Provide output in the dictionary format as follows: \
            {{
                "irrelevant organizations": ["organization1", "organization2", ...],
                "relevant organizations": [
                    {{"organization1": ["mapping_code1", "classification1"]}},
                    {{"organization2": ["mapping_code2", "classification2"]}},
                    ...
                ],
                "irrelevant products": ["product1", "product2", ...],
                "relevant products": [
                    {{"product1": ["mapping_code1", "classification1"]}},
                    {{"product2": ["mapping_code2", "classification2"]}},
                    ...
                ]
            }} \
            """
    if mode == 'two_step_mode':
        # build prompt for step 1
        if step_one_version == 'V1':
            prompt_1 = """You will be provided with the description about a company delimited by triple quotes. \
            Your objective is to extract the following four attributes from the company's description. \
            Attributes of a company: \
            (a) "relevant organizations": Organizations, individuals, or entities that the given company currently directly serves. \
            (b) "irrelevant organizations": (1) Competitors, suppliers, indirect customers (e.g., clients of clients); (2) previously served clients; (3) any organizations not currently directly served by the company. \
            (c) "relevant products": the specific products, services, or solutions originally, directly and currently offered by the given company. \
            (d) "irrelevant products": (1) Products are not original to our company (such as free WIFI, venues, events, etc.); (2) general services (such as food, accomodation, gaming services, etc.); (3) discontinued products; (4) products from clients, competitors and suppliers; (5) any products not directly provided by the company. \
            Preserve the extracted attributes exactly as in the description, without rephrasing or inference. \
            Provide the response as a dictionary adhering to the specified format without comments or explanations. \
            Provide output in the dictionary format as follows: \
            {
                "irrelevant organizations": ["organization1", "organization2", ...],
                "relevant organizations": ["organization1", "organization2", ...],
                "irrelevant products": ["product1", "product2", ...],
                "relevant products": ["product1", "product2", ...]
            } \
            """
        # build prompt for step 2
        if step_two_version == 'V1':
            if mapping_level == 'L1':
                prompt_2 = f"""You will be provided with the relevant organizations that a company serves and the relevant products that a company produces. \
                Your objective is to categorize the company into its corresponding 'target market' category based on the relevant organizations and relevant products. \
                The 'target market' refers to the industry sectors that a company serves. \
                The full 'target market' taxonomy with the codes are given as follows: \
                {classification_standard} \
                Use the following step-by-step instructions to generate the response: \
                Step 1 - Map each organization in 'relevant organizations' to the most suitable 'target market' classification in the given taxonomy. \
                Step 2 - For each product in 'relevant products', infer the organization most likely to use it, and determine the most suitable 'target market' classification that the organization belongs to in the given taxonomy. \
                Step 3 - If the product or service is aimed at a general customer group, such as patients, students, diners, player etc., then the 'target market' should be "0010".\
                Step 4 - Present the 'target market' as the 6-digit code in the given taxonomy whenever possible. \
                Step 5 - If no suitable 'target market' with an 6-digit code is found, resort to the upper level with 2 or 4-digit codes accordingly. \
                Step 6 - If the extraction in 'relevant organizations' is general ('clients,' 'customers,' 'users'), assign one of the following codes: "0010", "0020", "0030". \
                Step 7 - Provide the response as a dictionary adhering to the specified format without comments or explanations. \
                Provide output in the dictionary format as follows: \
                {{
                    "relevant organizations": [
                        {{"organization1": ["mapping_code1", "classification1"]}},
                        {{"organization2": ["mapping_code2", "classification2"]}},
                        ...
                    ],
                    "relevant products": [
                        {{"product1": ["mapping_code1", "classification1"]}},
                        {{"product2": ["mapping_code2", "classification2"]}},
                        ...
                    ]
                }} \
                """
            elif mapping_level == 'L3':
                prompt_2 = f"""You will be provided with the relevant organizations that a company serves and the relevant products that a company produces. \
                Your objective is to categorize the company into its corresponding 'target market' category based on the relevant organizations and relevant products. \
                The 'target market' refers to the industry sectors that a company serves. \
                The full 'target market' taxonomy with the codes are given as follows: \
                {classification_standard} \
                Use the following step-by-step instructions to generate the response: \
                Step 1 - Map each organization in 'relevant organizations' to the most suitable 'target market' classification in the given taxonomy. \
                Step 2 - For each product in 'relevant products', infer the organization most likely to use it, and determine the most suitable 'target market' classification that the organization belongs to in the given taxonomy. \
                Step 3 - If the product or service is aimed at a general customer group, such as patients, students, diners, player etc., then the 'target market' should be "000010".\
                Step 4 - Present the 'target market' as the 8-digit code in the given taxonomy whenever possible. \
                Step 5 - If no suitable 'target market' with an 8-digit code is found, resort to the upper level with 2, 4, or 6-digit codes accordingly. \
                Step 6 - If the extraction in 'relevant organizations' is general ('clients,' 'customers,' 'users'), assign one of the following codes: "000010", "000020", "000030", "000040". \
                Step 7 - Provide the response as a dictionary adhering to the specified format without comments or explanations. \
                Provide output in the dictionary format as follows: \
                {{
                    "relevant organizations": [
                        {{"organization1": ["mapping_code1", "classification1"]}},
                        {{"organization2": ["mapping_code2", "classification2"]}},
                        ...
                    ],
                    "relevant products": [
                        {{"product1": ["mapping_code1", "classification1"]}},
                        {{"product2": ["mapping_code2", "classification2"]}},
                        ...
                    ]
                }} \
                """
        elif step_two_version == 'V2': # with context (descriptions were fed again)
            if mapping_level == 'L1':
                prompt_2 = f"""You will be provided with 1) the description of a company, 2) the relevant organizations that a company serves, and 3) the relevant products that a company produces. \
                Your objective is to categorize the company into its corresponding 'target market' category based on the relevant organizations and relevant products. \
                The 'target market' refers to the industry sectors that a company serves. \
                The full 'target market' taxonomy with the codes are given as follows: \
                {classification_standard} \
                Use the following step-by-step instructions to generate the response: \
                Step 1 - Map each organization in 'relevant organizations' to the most suitable 'target market' classification in the given taxonomy with the help of the description. \
                Step 2 - For each product in 'relevant products', infer the organization most likely to use it with the help of the description, and determine the most suitable 'target market' classification that the organization belongs to in the given taxonomy. \
                Step 3 - If the product or service is aimed at a general customer group, such as patients, students, diners, player etc., then the 'target market' should be "65".\
                Step 4 - Present the 'target market' as the 6-digit code in the given taxonomy whenever possible. \
                Step 5 - If no suitable 'target market' with an 6-digit code is found, resort to the upper level with 2 or 4-digit codes accordingly. \
                Step 6 - If the extraction in 'relevant organizations' is general ('clients,' 'customers,' 'users'), assign one of the following codes: "65", "70", "75". \
                Step 7 - Provide the response as a dictionary adhering to the specified format without comments or explanations. \
                Provide output in the dictionary format as follows: \
                {{
                    "relevant organizations": [
                        {{"organization1": ["mapping_code1", "classification1"]}},
                        {{"organization2": ["mapping_code2", "classification2"]}},
                        ...
                    ],
                    "relevant products": [
                        {{"product1": ["mapping_code1", "classification1"]}},
                        {{"product2": ["mapping_code2", "classification2"]}},
                        ...
                    ]
                }} \
                """
            elif mapping_level == 'L3':
                prompt_2 = f"""You will be provided with 1) the description of a company, 2) the relevant organizations that a company serves, and 3) the relevant products that a company produces. \
                Your objective is to categorize the company into its corresponding 'target market' category based on the relevant organizations and relevant products. \
                The 'target market' refers to the industry sectors that a company serves. \
                The full 'target market' taxonomy with the codes are given as follows: \
                {classification_standard} \
                Use the following step-by-step instructions to generate the response: \
                Step 1 - Map each organization in 'relevant organizations' to the most suitable 'target market' classification in the given taxonomy with the help of the description. \
                Step 2 - For each product in 'relevant products', infer the organization most likely to use it with the help of the description, and determine the most suitable 'target market' classification that the organization belongs to in the given taxonomy. \
                Step 3 - If the product or service is aimed at a general customer group, such as patients, students, diners, player etc., then the 'target market' should be "00".\
                Step 4 - Present the 'target market' as the 6-digit code in the given taxonomy whenever possible. \
                Step 5 - If no suitable 'target market' with an 6-digit code is found, resort to the upper level with 2 or 4-digit codes accordingly. \
                Step 6 - For each 'target market' inferred from 'relevant organizations' and 'relevant products', add information about the company's specialization in public or private entities within that market. 'public' means that the organization in 'relevant organizations' or organizations inferred from 'relevant products' are public administrations or sectors run by the government, whereas 'private' means that they are private businesses controlled by private individuals and groups. For each of 'public' and 'private', give a value from 'yes', 'no' or 'not explicitly said'. Only answer 'yes' or 'no' if the response is explicitly supported by the description, otherwise answer "not explicitly said". \
                Step 7 - Provide the response as a dictionary adhering to the specified format without comments or explanations. \
                Provide output in the dictionary format as follows: \
                {{
                    "relevant organizations": [
                        {{"organization1": ["mapping_code1", "classification1", {{"public":"", "private":""}}]}},
                        {{"organization2": ["mapping_code2", "classification2", {{"public":"", "private":""}}]}},
                        ...
                    ],
                    "relevant products": [
                        {{"product1": ["mapping_code1", "classification1", {{"public":"", "private":""}}]}},
                        {{"product2": ["mapping_code2", "classification2", {{"public":"", "private":""}}]}},
                        ...
                    ]
                }} \
                """
        elif step_two_version == 'V3': # with context + guidelines
            if mapping_level == 'L1':
                prompt_2 = f"""You will be provided with 1) the description of a company, 2) the relevant organizations that a company serves, and 3) the relevant products that a company produces. \
                There are 13 classes with 2-digital TM-codes and the definition in the provided file.
                {guidelines} \
                Use the following step-by-step instructions to generate the response: \
                Step 1 - Map each organization in 'relevant organizations' to the most suitable TM-code in the provided file based on the definition with the help of the description. \
                Step 2 - For each product in 'relevant products', infer the organization most likely to use it with the help of the description, and determine the most suitable TM-code in the provided file that the organization belongs to based on the definition. \
                Step 3 - If a company provides their products or services directly to natural persons in general or groups of natural persons, e.g. women, students, elderly persons, cancer patients, university graduates, etc.  then the TM-code should be "00".\
                Step 4 - Do not give comments or explanations just provide the response as a dictionary with the following format: \
                {{
                    "relevant organizations": [
                        {{"organization 1": "TM-code 1"}},
                        {{"organization 2": "TM-code 2"}},
                        ...
                    ],
                    "relevant products": [
                        {{"product 1": "TM-code 1"}},
                        {{"product 2": "TM-code 2"}},
                        ...
                    ]
                }} \
                """
                
    return prompt_1, prompt_2