import openai

# Set up your OpenAI API credentials
openai.api_key = ''

api_input = {
    "email": "abc@gmail.com",
    "description": """
Create an AWS Lambda function that uses ChatGPT to extract information from documents and creates structured content in JSON format.
1. The lambda function will be invoked by a website with an S3 bucket and a folder object.
2. The function will fetch all files contained inside the folder. Any zip files will be extracted, and it's contents saved to a sub-folder inside the bucket.
3. The contents of all files of filetype pdf, docx, and doc are extracted, and sent to ChatGPT for processing
4. The results from ChatGPT are processed to extract pertinent information, and create a single JSON object, which is saved as a JSON file to the bucket
5. When the function is complete, a webhook is sent to the website with the URI of the JSON object.
""",
    "services": ["Web development", "Artificial Intelligence"],
    "features": [""],
    "timeline": "8 weeks",
    "launch_date": "1 June 2023",
    "budget": "$10000"
}

# Define the prompt
scope_prompt = f"""
Provide milestones, sprints of each milestone, modules of each sprint, description of each module, external API if applicable, timeline and deliverable:
Milestone #: content
Sprint #: content 
Module #: content 
Description: content
External API Key Names: content
Timeline: content
Deliverable: content

here is the description:\n{api_input['description']}\n
for services: {', '.join(api_input['services'])}\n
and timeline is {api_input['timeline']}
"""

# Generate the table using OpenAI API
response = openai.Completion.create(
    engine='text-davinci-003',
    prompt=scope_prompt,
    max_tokens=3000,
    n=1,
    stop=None,
    temperature=0.5
)

# Extract the generated completion
completion = response.choices[0].text.strip()

# Splitting the response into milestones
milestones = completion.split("Milestone")[1:]

# Initialize empty lists for data columns
milestone_nums = []
sprint_nums = []
module_nums = []
module_titles = []
module_descs = []
timelines = []
deliverables = []
APIs_req = []

# Process each milestone
for milestone in milestones:
    lines = milestone.strip().split("\n")
    milestone_num = lines[0].strip().split(":")[0]

    for line in lines[1:]:
        line = line.strip()
        if line.startswith("Sprint"):
            sprint_num = line.split(":")[0].strip()
        elif line.startswith("Module"):
            module_parts = line.split(":")
            module_num = module_parts[0].strip()
            module_title = module_parts[1].strip()
        elif line.startswith("Description"):
            module_desc = line.split(":")[1].strip()
        elif line.startswith("External API Key Names"):
            API_req = line.split(":")[1].strip()
        elif line.startswith("Timeline"):
            timeline = line.split(":")[1].strip()
        elif line.startswith("Deliverable"):
            deliverable = line.split(":")[1].strip()

            # Append data to the lists
            milestone_nums.append(milestone_num)
            sprint_nums.append(sprint_num)
            module_nums.append(module_num)
            module_titles.append(module_title)
            module_descs.append(module_desc)
            timelines.append(timeline)
            deliverables.append(deliverable)
            APIs_req.append(API_req)

def generate_proposal(api_input):
    title_prompt = f"Create title of the project having description: {api_input['description']}\n"
    summary_prompt = f"what Job we will do: Description Summary to the client who provided us the description of the job without the headings: {api_input['description']} for services {', '.join(api_input['services'])}\n"

    feasibility_prompt = "Write Technical Feasibility without the heading. Our company can work on these technologies which are MERN Stack, MEAN Stack, FERN Stack. In mobile: android, ios, unity, react native. In backend: java, node js, php, python. In front end: angular js, bootstrap, jQuery. In frameworks: express.js, vue.js, laravel, django. In databases: My SQL, Firebase, AWS Dynamo DB, MongoDB. In content management: system Joomla, Drupal, Opencms, Wordpress. In Ecommerce: Ecommerce, Woocommerce, Big commerce, Prestashop. In cloud: Amazon cloud, Openstack, google cloud, Azure. Choose the technology individually according to the project requirement to make scope. here are the features:\n"
    for feature in api_input['features']:
        feasibility_prompt += f"- {feature}\n"

    resources_prompt = f"provide only the names line by line of human resources required for a project: {api_input['description']}."

    message_prompt = "This is the AI generated proposal. For specific details and timelines, our team will shortly contact you. (Paraphrased using OpenAI)\n"
    
    overview = """Codistan is a complete design studio with web design and development, software development, mobile app development, brand design, social media marketing and internet marketing. The company aims to holistically cover all areas of the virtual market by providing an integrated ecommerce solution to its customers. 

In addition to the development of every kind, we also provide Social Media Marketing and Management services. These services include an amalgam of photography,videography, content and artwork generation, graphic designing and response handling as well as employing marketing strategies to promote business.

We aim to provide our customers with a 360 degree solution by catering to all aspects of the virtual market from coding to handling the aesthetics thereby providing them with a one stop panacea."""
  
    title = openai.Completion.create(
        engine="text-davinci-003",
        prompt=title_prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7
    ).choices[0].text.strip()
    
    summary = openai.Completion.create(
        engine="text-davinci-003",
        prompt=summary_prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    ).choices[0].text.strip()
    
    feasibility = openai.Completion.create(
        engine="text-davinci-003",
        prompt=feasibility_prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7
    ).choices[0].text.strip()
    
    resources = openai.Completion.create(
        engine="text-davinci-003",
        prompt=resources_prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    ).choices[0].text.strip()   
    
    message = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message_prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    ).choices[0].text.strip()
    
    address_lines = [
        "Codistan Ventures Building Plot no 15, I-11/3 Islamabad, 44000, Pakistan",
        "contact@codistan.org",
        "sales@codistan.org",
        "6343 N Sacramento Ave #2w, Chicago, IL 60659",
        "tel:7738002704"
    ]
    
#     contact = "\n".join(address_lines)
        
    api_output = {
        "Overview of Our Company": overview,
        "Job Title": title,
        "Job Description Summary": summary,
        "Problem Statement": api_input['description'],
        "Technical Feasibility": feasibility,
        "Resources Required": resources,
        "Contact Details": address_lines,
        "Note": message,
    }
    
    return api_output

api_output = generate_proposal(api_input)
print(api_output)

html = '''
<!DOCTYPE html>
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        margin: 50px;
          text-align: justify;
          padding: 70px;
      }}

      h1 {{
        font-size: 24px;
        margin-top: 40px;
      }}
      
    h1.title {{
        text-align: center;
        font-size: 32px;
        color: #333;
        margin-top: 40px;
        text-transform: uppercase;
        letter-spacing: 2px;
  }}

    h2 {{
    font-size: 20px;
    margin-top: 30px;
    }}
      p {{
        font-size: 16px;
        line-height: 1.5;
      }}

      table {{
        border-collapse: collapse;
        width: 100%;
      }}

      th, td {{
        border: 1px solid black;
        padding: 8px;
        text-align: center;
      }}

      th.sprint-no {{
        width: 80px;
      }}

      th.sr-no {{
        width: 60px;
      }}

      th {{
        background-color: #f2f2f2;
        font-weight: bold;
      }}

      ul {{
        list-style-type: none;
        margin: 0;
        padding: 0;
      }}

      ul li {{
        margin-bottom: 10px;
      }}
    </style>
  </head>
  <body>
      <h1 class="title">Project Proposal</h1>
    <h1>Overview of Our Company:</h1>
    <p>{}</p>
    <h1>Job Title:</h1>
    <p>{}</p>
    <h1>Job Description Summary:</h1>
    <p>{}</p>
    <h1>Problem Statement:</h1>
    <p>{}</p>
    <h1>Proposed Solution:</h1>
    <h2>Technical Feasibility:</h2>
    <p>{}</p>
    <h1>Scope:</h1>
    <table>
      <tr>
        <th class="sprint-no">Sprint No.</th>
        <th>Module Title</th>
        <th class="sr-no">Sr. No.</th>
        <th>Module Description</th>
        <th>Timeline</th>
        <th>Requirements</th>
        <th>Deliverables</th>
      </tr>
      <tr>
        <th colspan="7">Milestone 1</th>
      </tr>
'''

# Iterate over the list and add rows for each module
for index, module_name in enumerate(module_titles):
    module_description = module_descs[index]
    timeline_value = timelines[index]
    deliverable = deliverables[index]
    requirement = APIs_req[index]
    
    html += f'''
      <tr>
        <th>Sprint {index+1}</th>
        <td>{module_name}</td>
        <td>{index+1}</td>
        <td>{module_description}</td>
        <td>{timeline_value}</td>
        <td>{requirement}</td>
        <td>{deliverable}</td>
      </tr>
'''
    if (index+1) % 2 == 0 and index+1 != len(module_titles):
        milestone_number = (index+1) // 2
        html += f'''
      <tr>
        <th colspan="7">Milestone {milestone_number + 1}</th>
      </tr>
'''
        
html += '''
    </table>
    <h1>Resources Required:</h1>
    <p>{}</p>
    <h1>Contact Details:</h1>
    <p>{}</p>
    <h1>Note:</h1>
    <p>{}</p>
  </body>
</html>
'''

resources_list = api_output['Resources Required'].split('\n')

resources_html = '<ul style="list-style-type: none;">'
for resource in resources_list:
    resources_html += f'<li>{resource}</li>'
resources_html += '</ul>'

contact_html = '<ul style="list-style-type: none;">'
for line in api_output['Contact Details']:
    contact_html += f'<li>{line}</li>'
contact_html += '</ul>'

html = html.format(
    api_output['Overview of Our Company'],
    api_output['Job Title'],
    api_output['Job Description Summary'],
    api_output['Problem Statement'],
    api_output['Technical Feasibility'],
    resources_html,
    contact_html,
    api_output['Note']
)

filename = "output7.html"

with open(filename, "w") as file:
    file.write(html)

print("HTML exported successfully to", filename)