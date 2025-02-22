import json
import time
import openai
from openai import OpenAI
from settings import OPENAI_API_KEY


openai.api_key = OPENAI_API_KEY
openai.default_headers = {"OpenAI-Beta": "assistants=v2"}

client = OpenAI()

# file = client.files.create(
#   file=open("./sample_categories.json", "rb"),
#   purpose='assistants'
# )

# assistant = client.beta.assistants.create(
#     name="Business Analyst",
#     instructions=f"""
#     """,
#     # tools=[{"type": "code_interpreter"}],
#     model="gpt-4-1106-preview",
#     #file_ids=[file.id]
# )

thread = client.beta.threads.create()  
  
def assistant_api_target_markets(descr):
  
  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      #content=f"Description: {descr}\nAttributes: {str(attributes)}"
      content=f"Description: {descr}"
  )

  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    #assistant_id="asst_lbTXOZP8wYJMHiIhvSNIvJCn", # gpt-4o (second step with descriptions + guidelines)
    #assistant_id="asst_kZGJYQhhipPQVoWLU9fwZjH5", # gpt-4o (one single step with descriptions + guidelines)
    assistant_id="asst_0zWn9c7AvR6lfwFf4ZnzHTnE", # gpt-4o (one single step with descriptions + guidelines + new prompt)
    #assistant_id="asst_4TBdnMNsROF5dndlo7Ss8Zmx" # gpt-4o (guidelines + browse the website)
    # assistant_id=assistant.id
    )

  '''
  gpt-4o (one single step with descriptions + guidelines)
  
  
  You will be provided with the description of a company. \
  We define 4 entites of a company: \
  Type 1: Organizations, individuals, or entities that the given company currently directly serves. \
  Type 2: Competitors, suppliers, indirect customers (e.g., clients of clients), previously served clients, and any organizations not currently directly served by the company. \
  Type 3: the products, services, or solutions directly and currently offered by the given company. \
  Type 4: Products from clients, competitors, suppliers, discontinued products, and any products not directly provided by the company. \
  There are 13 classes with 2-digital TM-code and the definition in the provided file.
  Use the following step-by-step instructions to generate the response: \
  Step 1 - Extract entities 1-4 from the description.
  Step 2 - Map each entity in type 1 to the most suitable TM-code in the provided file based on the definition with the help of the description. \
  Step 3 - For each entity in type 3, infer the organization most likely to use it with the help of the description, and determine the most suitable TM-code in the provided file that the organization belongs to based on the definition. \
  Step 4 - If a company provides their products or services directly to natural persons in general or groups of natural persons, e.g. the attribute values are women, students, elderly persons, cancer patients, university graduates, etc.  then the TM-code should be "00".\
  Step 5 - If there is no suitable TM-code in the provided file, return TM-code as "-1".
  Step 6 - Don't generate TM-codes not in the provided files. Don't generate any inference process, explanations, or intermediate results. Just respond a dictionary with the following format: \
  {{
      "relevant organizations": [
          {{"extracted organization 1": "TM-code 1"}},
          {{"extracted organization 2": "TM-code 2"}},
          ...
      ],
      "relevant products": [
          {{"extracted product 1": "TM-code 1"}},
          {{"extracted product 2": "TM-code 2"}},
          ...
      ]
  }} \
  '''


  '''
  gpt-4o (one single step with descriptions + guidelines + new prompt)
  
  
  You will be provided with the description of a company. \
  Your goal is to find its corresponding target markets (defined in the provided file) based on the description. \
  Given a company, its target markets are the group(s) of natural or legal persons (companies, institutions, individuals) to which it provides some of its products or services in order to generate value. \
  There are 13 classes of target markets with 2-digital TM-code and the definition in the provided file.
  Use the following step-by-step instructions to generate the response: \
  Step 1 - Read each sentence to determine if it explicitly mentions the target market.
  Step 2 - If there is one or more explicitly mentioned target markets in the sentence, find the most suitable TM-code in the provided file based on the definition. \
  Step 3 - The TM-codes must be in the provided files. \
  Step 4 - Don't generate any inference process, explanations, or intermediate results. Just respond a list of dictionary with the following format: \
  [
    {{"sentence explicited mentioned target market": [
      {{"TM-code 1": ["supported piece of text in description", "corresponding sentence in definition"]}}, 
      {{"TM-code 2": ["supported piece of text in description", "corresponding sentence in definition"]}},
      ...
      ]
    }},
    {{"sentence explicited mentioned target market": [
      {{"TM-code 1": ["supported piece of text in description", "corresponding sentence in definition"]}}, 
      {{"TM-code 2": ["supported piece of text in description", "corresponding sentence in definition"]}},
      ...
      ]
    }},
    ...
  ] \
  '''

  '''
  gpt-4o (guidelines + browse the website)
  
  You will be provided with the website of a company. \
  Your goal is to find its corresponding target markets (defined in the provided file) by browsing the website. \
  Given a company, its target markets are the group(s) of natural or legal persons (companies, institutions, individuals) to which it provides some of its products or services in order to generate value. \
  There are 13 classes of target markets with 2-digital TM-code and the definition in the provided file.
  Use the following step-by-step instructions to generate the response: \
  Step 1 - Read each webpage to determine if it explicitly mentions the target market.
  Step 2 - If there is one or more explicitly mentioned target markets in the webpage, find the most suitable TM-code in the provided file based on the definition. \
  Step 3 - The TM-codes must be in the provided files. \
  Step 4 - Don't generate any inference process, explanations, or intermediate results. Just respond a list of dictionary with the following format: \
  [
    {{"webpage url 1": [
      {{"TM-code 1": ["supported piece of text in the webpage", "corresponding text in definition"]}}, 
      {{"TM-code 2": ["supported piece of text in the webpage", "corresponding text in definition"]}},
      ...
      ]
    }},
    {{"webpage url 2": [
      {{"TM-code 1": ["supported piece of text in the webpage", "corresponding text in definition"]}}, 
      {{"TM-code 2": ["supported piece of text in the webpage", "corresponding text in definition"]}},
      ...
      ]
    }},
    ...
  ] \
  '''

  while True:
    time.sleep(2)
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )
    if run.status == 'completed':
      break
    else:
      pass

  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )

  # messages = client.beta.threads.messages.retrieve(
  #   thread_id=thread.id,
  #   message_id=message.id
  # )

  # print(messages)

  # print('\n*******************************')
  # for msg in messages.data:
  #   print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
  #   print(msg.content[0].text.value)

  # print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
  # print(messages[-1].content[0].text.value)

  num_response = 0
  for msg in messages.data:
    print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(msg.content[0].text.value)
    if num_response == 0:
      response_str = str(msg.content[0].text.value)
      response_str = response_str.replace('```json', '')
      response_str = response_str.replace('```', '')
      res = json.loads(response_str)
    num_response += 1
  return res


if __name__ == "__main__":
  # input_file = './data/input.jsonl'
  # for line_id, line in enumerate(open(input_file, 'r')):
  #   time.sleep(1)
  #   if line_id >= 1:
  #       break
  #   dict = json.loads(line)
  #   descr = str(dict["text"])
  
  #descr = "At BrainGu, our platforms deliver automated solutions that foster an environment where developers can thrive, and deliver high-quality software with efficiency, confidence, and peace of mind. Our extensive knowledge of distributed systems, honed expertise in complex architectures, and skills in IaC and CaC make us the ultimate partner for organizations that demand unwavering reliability. 's DevSecOps Platform Suite, Structsure®, is a solution that delivers exceptional developer experience, with security baked in, at every stage of the Software Development Life Cycle. BrainGu is a technology company specializing in developer-centric DevSecOps platforms and operator-driven mission applications. At BrainGu, we're passionate about transforming technology. We believe in a human-centered approach to incubating and scaling technologies that tackle real-world problems. Pillars of Creation quickly validates and prepares code updates, guaranteeing they don't disrupt the current application and ensuring its seamless operation before users interact with it. Other platforms focus on delivering solutions that impact individual stages of the Software Development Life Cycle. Learn more about our Government Solutions and how we drive results in weeks, not years. Our commitment to reliability starts with our architecture, which is meticulously designed to withstand the toughest challenges. Visit BrainGu at AFA Warfare Symposium 2024. It empowers software development teams to deliver business-critical applications securely, with the agility to scale and adapt to challenges. BrainGu is your ideal tech partner because your mission is our driving force. This means that data analysis can now occur on a smart device at the network's edge. Empowering Security & Mission Success Through DevSecOps Excellence. Gaylord Rockies Resort & Convention Center. Structsure understands the intricacies of scalability. BrainGu develops custom DevSecOps software that enables mission success and boasts exceptional user and developer experience by working directly with end-users to solve their real-life problems and continuously improve capabilities. By automating pinch points, BrainGu innovates new ways to solve mission problems. Our vision is to solve complex national security challenges for the United States and its allies by incubating and scaling technology solutions that emphasize fielded, meaningful military capability in the hands of operators and mission owners. BrainGu is setting the standard for rapid deployment and scalability of mission applications. As part of our Mission App as a Service solution offering, BrainGu offers subscription and packaged app timeline products that are aligned to BrainGu’s overall mission to provide the best, cutting-edge technology to the warfighter at the tactical edge."
  #attributes = { "irrelevant organizations": ["Gaylord Rockies Resort & Convention Center"], "relevant organizations": ["organizations that demand unwavering reliability", "Government Solutions", "United States and its allies", "end-users", "warfighter"], "irrelevant products": ["AFA Warfare Symposium 2024"], "relevant products": ["automated solutions", "DevSecOps Platform Suite", "Structsure®", "Pillars of Creation", "custom DevSecOps software", "Mission App as a Service solution", "subscription and packaged app timeline products"] }
  
  
  #descr = "Bioservices , a leading supplier of kits, consumables and instruments in DNA/RNA extraction and PCR equipment, will be at LabDays 2023 in Oslo on October 11-12, 2023, where they will be showcasing their latest developments in medical devices, including a high-tech acid extraction instrument which uses Neonode technology to enable contactless operation. Neonode will be available on the Bioservice's booth (5A) to answer your questions about how our contactless solutions can improve workflows in laboratory and hospital environments, and how touchless technology can be safely used to remove any risk of cross contamination in sterile environments. Neonode is attending LabDays 2023 together with Bioservices, where we will be showcasing the latest in contactless medtech devices for laboratories and hospital environments. LabDays is a two day trade fair and conference for professionals in working in hospitals, biotech, pharmaceuticals, research and life sciences."
  
  #descr = "As the largest owner/operator of imaging centers in the U.S., RadNet leverages its IT solutions, quality initiatives, utilization management program, specialty health services, and 30+ years of experience across all facilities in the network. Interventional Radiology is loosely defined by its minimally invasive image-guided diagnostic and therapeutic procedures, giving Interventional Radiologists the ability to harness the power of advanced imaging (CT, MRI, Ultrasound, and other innovative modalities). Borg and Ide Imaging (BII) Culver Park Imaging center is located off of Keeler St. Expressway East and directly off Culver Road; we are 16 minutes from Strong Memorial Hospital. At this full-service imaging center, we offer 3T MRI, 1.2T Open/High Field MRI, CT, Coranary CT Angiography (CCTA), PET/CT, Nuclear Medicine, Arthrography, 3D Mammography, Lung Cancer Screening, Ultrasound, Interventional Radiology, and more. At its inception, RadNet provided billing and administrative services to radiology groups in the Los Angeles area, and it opened its first imaging center across from Cedars-Sinai Medical Center in 1981. RadNet's national network of imaging centers, payor relationships , and physician resources is linked by state-of-the-art cloud technology powered by our own IT division, eRAD. For over 90 years, Borg and Ide Imaging has proudly offered radiology services across the Rochester region. - RadNet, Inc. (NASDAQ:RDNT), a national leader in providing high-quality, cost-effective, fixed-site outpatient diagnostic imaging services, announced today the closing of its underwritten public offering of 5,232,500 shares of its common stock at a price to the public of $44.00 per share, which includes the exercise in full by the underwriters of their option to purchase up to 682,500 additional shares of its common stock. We look forward to serving you!Please note that, although similar in name, Hudson Valley Radiology Associates is not affiliated with Hudson Valley Imaging. As such, patients can expect the same caring service and unmatched quality imaging and interpretation that you've come to expect. Those without health insurance, or with high deductible plans, can contact a local center to inquire about pricing. RadNet was founded by six medical doctors, including Dr. Howard Berger, our Chairman and Chief Executive Officer. In 1990, Dr. Berger and Dr. Michael Krane, our Director of Utilization Management, purchased the interests of their four other partners, and became the sole owners of RadNet. Total number of our imaging centers across the U.S. - in MD, DE, NY, NJ, FL, CA, AZ. Our complete radiology solution puts us in the best position to be strategic about the future of healthcare. RadNet recognizes that value is a key factor in navigating your healthcare. These minimally invasive treatments can alleviate symptoms of vascular disease, stroke, cancer, and other conditions. Our Clinton Crossings location also offers Interventional Radiology. Join us for Stuart Cardiology's 'And The Beat Goes On' 5K! Conveniently located along the RTS bus route, this location is right across the street from South Pointe Landing and just a few blocks south of the Erie Canal. Flexible exam hours designed around your schedule. In March 2006, RadNet completed a $161 million re-capitalization through a syndicated loan transaction arranged by GE."
  
  
  descr = "HCL Global Systems is one of the best IT consulting firm specialized in Application development, Quality Testing, IT Courses Training, staffing and recruitment services. Top 4 reasons why customers choose us as their software company. HCL Global Systems as a leading consulting, business solution and systems integration firm delivering solutions that benefit our clients by applying our Knowledge and experience and create a curriculum that fits industry standards with a unique blend of services. HCL Global Systems provides solutions to various industries including Healthcare, Manufacturing, Insurance, Engineering, Financial services, Banking, Consumer retail, Telecommunications and Aerospace. We always recruit outstanding consultants with a strong technical and functional knowledge in their respective areas of expertise. Our Technical teams at HCL Global Systems obtain interesting jobs dealing with top-notch tools and up-to-date technologies, competitive salary and benefits, much room for personal and career advancement. All we do is help clients realize value from their software. We are a fast growing software consulting company offering software development solutions to all our clients through offshore and onsite services. HCL Global Systems is a leading consulting, business solution and systems integration firm with a unique blend of services. We would like to deliver solutions that benefit our clients by applying our Knowledge and experience and create a curriculum that fits industry standards. HCL Global Systems offers a broad range of professional consulting, systems analysis & development, systems integration and support services. With solid, broad based experience, we are confident in our ability to help our customers grow and improve their businesses. More than likely, regardless of the nature and scope of the problem, our dedicated team of professionals can help you achieve a cost effective business solution."
  
  
  # descr = "Working hand-in-hand with their customers Woolman is the leading Full-Service Partner helping large complex businesses to achieve rapid growth with their D2C strategies through a data-driven first approach. Our breakthrough is in behavior-based recommendations, which enable businesses to provide highly relevant recommendations to each user within a couple clicks - all without using personal data. Our platform offers custom-tailored AI for the nuances of your specific store, giving you the customization tools and white-glove service you need to fuel your next phase of growth. From strategy and ecommerce solutions to innovative design and growth marketing, our expertise drives business profitability all while making consumers fall in love with your brand. Crossing Minds was able to clean, consolidate, and analyze Camp's catalog data in order to serve highly relevant recommendations to Camp's customers via email. To do so, we make AI technology that fuels the smartest recommender system for ecommerce, marketplaces, streaming services, and more. Electric Orange is a Brooklyn-based Digital Marketing agency specializing in data-driven Paid Media and SEO for high-growth companies across the globe. It has been a joy working with their data-obsessed team to provide recommendations and content that's hyper-relevant to our customers. 30-day free trial to A/B test and customize the smartest recommendations for your unique scenario. Deliver an interactive search & discovery experience with a personalized LLM. GPT Spotlight is an intuitive way to discover new products that consolidates search and recommendations into one discovery experience. Crossing Minds truly partnered with us to adapt and adjust the recommendation platform for our needs to deliver effective, quality recommendations. The combination of Crossing Minds' AI for true 1: personalization and Klaviyo's email marketing platform dramatically reduced unsubscribes and juiced up email conversion rates. We launch eCommerce brands to market, grow early stage businesses, and partner with industry leaders - forming long-term relationships that are built upon a shared trust & vision. Camp was looking to increase the value of its omnichannel efforts by ensuring its emails provided highly relevant product recommendations while also mitigating the risk of mailing list unsubscribes. Our easy-to-integrate platform makes advanced AI accessible for any business. Get an overview of Crossing Minds and its features. Its popular brick-and- mortar locations - featuring expertly curated toys and games as well as activities - were far exceeding its capabilities online, however. Crossing Minds is an extremely powerful tool to have in your arsenal. See the volume of each trend and make appropriate merchandising adjustments. Get insights on top trends, searches, and requests from customers. Conversational search & discovery with ChatGPT for e-commerce. Crossing Minds is the only AI recommender system backed by Shopify. Get insights into shopping trends on your site. Free trial to A/B test and customize with your brand voice. Roswell is a full service eCommerce agency, Shopify Plus Partner and Klaviyo Platinum Partner. ChatGPT for Shopify has never been more intuitive. actually just show me the options you have for floral print, not the others. Website Audit and Optimization Strategye. increase in GMV through personalized emails. this needs to be comfortable for an outdoor wedding in Miami in July. Commerce Strategy (Business, Functional, and Technical). looking for some shirts for a casual event, i look good in green. give me a belt that would match my brown leather Italian shoes. Crossing Minds is the smartest platform powering perceptive recommendations that drive online discovery and engagement. Founded and led by world-renowned AI pioneers and powered by the latest advances in deep learning, Crossing Minds instantly delivers precise, session-based recommendations that don’t infringe on or jeopardize customer privacy. We help businesses engage their customers. We help people discover products they love. We help turn curiosity into loyalty."
  
  # descr = "We are a leading provider of technology-enabled credit card processing services, with expertise and experience in meeting the unique needs of all types of businesses. From website development and SEO to custom software and mobile app development, we can eliminate your fear of being left behind in today's digital age. I would 100% recommend Next Level Studio if you are a business owner looking to boost your online presence. We are a Mobile, AL based web design and software development firm. Very positive experience with Next Level Studio. Being in this city has also allowed us to become a leading technology provider in the maritime and logistics industry which is what helped us spread around the country and the rest of the world in just a few years. We are proud to be headquartered in such a beautiful region and are proud to be serving both small and large businesses in Mobile and its surrounding locales. From the most beautiful beaches in the world to the birth place of Mardi Gras, this city is truly a gem. Based in Mobile, AL and serving the globe. In today’s digital world, your digital presence is extremely important. You have a great business, so, shouldn't your website and internal processes be great too? Not only do we want your product to be the best, we also want to ensure your success. Next Level Studio offers a variety of solutions from custom software to responsive web design and development."
  
  
  target_markets = assistant_api_target_markets(descr=descr)
  output_str = ""
  
  for tm in target_markets:
    for key, val in tm.items():
      output_str += f"\n* Sentence (explicit): {key}"
      for tm_codes in val:
        tm_code = list(tm_codes.keys())[0]
        content = tm_codes[tm_code]
        output_str += f"\n\t- {tm_code}: \n\t\tSupport text: {content[0]}\n\t\tCorresponding definition: {content[1]}"
  print('#############################')
  print(output_str)