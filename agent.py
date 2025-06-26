from json import load
import json
import asyncio
import requests
import logging
# Configure the API key for Google Generative AI
api_key="Your API KEY HERE in"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def gen(prompt,api_key=api_key):
    try:
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # Check for HTTP errors
        if not response.ok:
            logging.error(f"API request failed with status {response.status_code}: {response.text}")
            return None

        data = response.json()
        
        # Safely access nested dictionary keys
        try:
            content = data['candidates'][0]['content']['parts'][0]['text']
            return content
        except (KeyError, IndexError) as e:
            logging.error(f"Unexpected response structure: {str(e)}")
            logging.debug(f"Full response: {data}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Network/connection error occurred: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        return None

# Example usage:
# if __name__ == "__main__":
#     main("your_api_key_here")

class Asseten:
    def __init__(self, name: str = 'asseten', genfun=gen):
        self.name = name
        self.genfun = gen
        self.requests = {}
        self.counter = 0

    def new_request(self, id, prompt):
        self.counter += 1
        self.requests[id] = {}
        self.requests[id]['prompt'] = prompt

    async def send_to_db(self, id):
        # add_to_db(Response, **self.requests[id])
        self.requests.pop(id, '')

    async def detect_user_entity(self, id):
        self.requests[id]['UE'] = await self.genfun(
            f"study this prompt and detect user entity in only one sentence: {self.requests[id]['prompt']}\nexamples:\n'write me a story':'user want a english story',\n'hello':'user is greeting he want me to answer him',"
        )
        print('UI-done')
        return {'status':'done'}

    async def detect_needed_data(self, id):
        self.requests[id]['NDQ'] = await self.genfun(
            f"study this prompt and detect needed data as a list of informaition: {self.requests[id]['prompt']}.\nnote if data is not enough return genral data.\nreturn information only with qutitions."
        )
        self.requests[id]['ND'] = await self.genfun(
            f"You are a user and you goved the AI assestent the prompt: {self.requests[id]['prompt']}.\The assestent sudanesed you with the qutitions{self.requests[id]['NDQ']}.So answer it"
        )
        print('ND-done')
        return {'status':'done'}

    async def write(self,text):
        text = await self.genfun(
            f'''study this text and write it agine in html.Only write html pragreph without body,html,header tag or (` for code).make it color full with bootstrap@5.3.6 classes ,icon-fontawesome-5 ,icon-lineawesome and icon-remixicon icons and seo optimized and interactive with hover.text:{text}.\nAdd amizing effect and transfom and glow and any beautifull effect you think it will greate with the text.'''
            )
        print(text)
        return text
    async def topicer(self, title):
        text = await self.genfun(
            f"study this title and suggest a list of 100 topics that they are realated to it and new and seo optimized and inter-reseting\ntitle:{title}.\nreturn a list like this:\ntopic1.\ntopic2.\ntopic3.write topic list only and no more.\ntitles must be in same language to given title.")
        return text
    async def planer(self, id):
        self.requests[id]['STRdes'] = await self.genfun(f'study tis prompt and descid if it is complex(coding math sinctifcal quize or some thing need thinking) answer with True else if it not compelx(greeting ask about name your self or want a joke or story) answer with False,you answer must be True or False only,promt"{self.requests[id]["prompt"]}"')
        self.requests[id]['des'] =True if 'T' in self.requests[id]['STRdes'] else False
        if (self.requests[id]['des']):
            await self.detect_user_entity(id)
            await self.detect_needed_data(id)
            self.requests[id]['plan'] = await self.genfun(
            f"you are ai asseten, I will provide you with prompt, user entity, needed data your task to make a step by step plan to do the task it make steps in shape of list: prompt:{self.requests[id]['prompt']},\nuser entity: {self.requests[id]['UE']},\nneed data: {self.requests[id]['ND']}"
            )
            print('plan-done')
        return {'status':'done'}
    
    async def recustom(self, id):
        self.requests[id]['restyle']=await self.genfun(f"study tis prompt and descid if it asked to edit style <example:make text color blue, or make border thick, or make back ground full of ice img,or any other change in page css or  page structure(make side bar right or hide tool bar or some thing like this)>{self.requests[id]['prompt']} answer must be a json with keys type value newValue attribute. else if it not is not asked for changing stlye answer with False.exmples:\nmake back ground blue:"+'{"type":"tag","value":"body","attribute":"style.color","newValue":"bule"}.\nmake post text red:{"type":"class","value":"card","attribute":"style.text","newValue":"red"}.\nmake all div with id call have display none:{"type":"id","value":"call","attribute":"style.display","newValue":"None"}\nmake class card-body with larger text {"type": "class","value": "card-body","attribute": "style.fontSize","newValue": "20px"}'+"""\nexplain ids and class:{
  "classes": {
    "loading": "Container for the page loader animation",
    "loading-center": "Centers the loader content",
    "wrapper": "Main wrapper for the entire page content",
    "iq-sidebar": "Main sidebar container",
    "sidebar-default": "Default styling for the sidebar",
    "sidebar-scrollbar": "Enables scrolling within the sidebar",
    "iq-sidebar-menu": "Container for sidebar menu items",
    "iq-menu": "Styles the list of menu items in sidebar",
    "iq-submenu": "Styles dropdown submenu items",
    "iq-top-navbar": "Container for the top navigation bar",
    "iq-navbar-custom": "Custom styling for the navbar",
    "iq-navbar-logo": "Styles the logo section in navbar",
    "iq-menu-bt": "Styles the menu button in navbar",
    "wrapper-menu": "Wrapper for menu button elements",
    "main-circle": "Styles the circular menu button",
    "iq-search-bar": "Styles the search bar container",
    "device-search": "Indicates search functionality for devices",
    "searchbox": "Styles the search form",
    "search-link": "Styles the search icon link",
    "search-input": "Styles the search input field",
    "navbar-list": "Styles the list of navigation items",
    "sub-drop": "Styles dropdown submenus",
    "sub-drop-large": "Styles larger dropdown submenus",
    "iq-friend-request": "Styles friend request items",
    "iq-sub-card": "Styles sub-cards within dropdowns",
    "iq-sub-card-big": "Styles larger sub-cards",
    "active-faq": "Styles active FAQ items",
    "header-title": "Styles header titles in cards",
    "card-title": "Styles card titles",
    "accordion-details": "Styles accordion content areas",
    "iq-accordion": "Styles accordion containers",
    "career-style": "Specific accordion style variant",
    "faq-style": "Styles FAQ elements",
    "iq-accordion-block": "Styles individual accordion blocks",
    "iq-footer": "Styles the footer container",
    "iq-bg-primary-hover": "Primary color hover effect",
    "iq-bg-warning-hover": "Warning color hover effect",
    "iq-bg-danger-hover": "Danger color hover effect",
    "bg-soft-primary": "Light primary background",
    "bg-soft-warning": "Light warning background",
    "bg-soft-danger": "Light danger background",
    "iq-sign-btn": "Styles sign-in/out buttons",
    "offcanvas": "Styles offcanvas containers",
    "share-offcanvas": "Specific style for share offcanvas"
  },
  "ids": {
    "loading": "Main loader container ID",
    "loading-center": "Loader center content ID",
    "iq-sidebar-toggle": "ID for sidebar toggle elements",
    "pages": "ID for pages dropdown menu",
    "navbarSupportedContent": "ID for collapsible navbar content",
    "group-drop": "ID for group dropdown",
    "notification-drop": "ID for notifications dropdown",
    "mail-drop": "ID for messages dropdown",
    "drop-down-arrow": "ID for user profile dropdown",
    "content-page": "ID for main content area",
    "share-btn": "ID for share offcanvas element",
    "shareBottomLabel": "ID for share offcanvas label"
  }
}""")
        return {'status':'done'}
        
        #if bool():
            #self.requests[id]['new_style'] = await self.genfun(
                #f"{self.requests[id]['plan']}"
            #)
            # add_to_db()

    def style_to_json(self, id):
        return load(self.requests[id]['new_style'])
    
    async def answer(self, prompt):
        userId = 1
        id = str(self.counter)
        self.new_request(str(self.counter), prompt)
        await self.planer(id)
        if (self.requests[id]['des']):
            self.requests[id]['task'] = await self.genfun(
                f"you are expered prompt engeneer ,your task is to write a prompt to ai model to do the plan as user enity work if the prompt is comlex but if it is dircet like greeting,thanking,asking about name tell the model to give basic answer for it in one and if user asked you to change some thing in page style say to him it is done.sentence \nprompt:{self.requests[id]['prompt']}, spicify the expected out put language and write prompt in the excpected out put language then give the model instrucation to have excpected out put instrucation ,ai most answer what ever happened ,it can give some suggestion on the last line.\nplan:{self.requests[id]['plan']},\nuser entity:{self.requests[id]['UE']}.\ensttraction of answer:\n.answer must be lovly and lovful.\n.answer must not contain useless data.\n.of the task is diffecalt make it esyer."
            )
        else:self.requests[id]['task']=self.requests[id]['prompt']
        self.requests[id]['answer'] = await self.genfun(self.requests[id]['task'])
        print('AN-done')
        #await self.detect_user_filling(id, userId)
        await self.recustom(id)
        return (self.requests[id])

    async def detect_user_filling(self, id, userId):
        # user = load_data(User, id=userId)[0]
        self.requests[id]['UF'] = await self.genfun(f"{self.requests[id]['answer']}")
        self.requests[id]['IM'] = await self.genfun(
            f"{self.requests[id]['answer']}, {self.requests[id]['UF']}"
        )
        # user.assetenEnest = await self.genfun(f"{self.requests[id]['IM']}, {self.requests[id]['IM']}")
        # db.session.commit()


# Example usage with asyncio
async def main():
    a = Asseten()
    d= await a.write('Sudan is a big country.\nIt is friendy & quit.\nThe must famous sudanese town‘s are:Kahrtoum,Wad-madnai,Port-Sudan')
    return d


# Run the asyncio event loop
if __name__ == "__main__":
    d=asyncio.run(main())
    print(d)