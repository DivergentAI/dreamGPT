import random

def combinePrompt(dreamPair):
    PERSONAS = ["I want to you to act as an Ideation Expert. An Ideation Expert has strong creative, problem-solving and analytical skills, " \
                  "with knowledge of research methods and design thinking. They should be adept at identifying " \
                  "opportunities and generating ideas, as well as have the ability to communicate and collaborate " \
                  "with others. Additionally, they must have an understanding of the latest trends and technology " \
                  "in their industry.",
                "I want to you to act as an Idea Generator. An Idea Generator has an innovative mindset and a " \
                  "creative spirit, which they use to develop unique concepts and solutions. They should have " \
                  "extensive knowledge of various industries, trends, and technologies. Additionally, they should " \
                  "possess strong research skills and the ability to think critically and objectively. Communication " \
                  "and collaboration skills are also essential to work effectively with other stakeholders." ]
    PROMPT_SYSTEM = random.choice(PERSONAS)
    PROMPT_USER_INPUT_1 = """
Given the following JSON, create a novel concept which takes both ideas and combines a single, 
coherent and useful idea. The resulting JSON will return a single JSON object with the following fields:
  - title
  - description
  - noveltyScore: measures how unique and distinct this concept is from anything else seen before.
  - marketScore: measures the potential market ($$$) for this concept.
  - usefulnessScore: measures the potential benefit of use of this concept.
  - easeOfImplementationScore: measures how easy it would be to make this concept a reality.
  - impactScore: measures the potential positive impact in the world of this concept.

This is the JSON to use as input:
[
  {
    "title": "Smart Home Garden",
    "description": "A device that can be used to grow plants indoors using hydroponics and AI. The device will be able to detect the needs of the plants and adjust the environment accordingly. It will also be able to connect to a smartphone app, where users can monitor and control the device."
  },
  {
    "title": "Virtual Personal Stylist",
    "description": "A virtual assistant that uses AI to recommend clothing and accessories based on a person's preferences, body type, and occasion. The assistant will take into account the user's budget and suggest items from different brands and retailers."
  }
]
"""
    PROMPT_EXAMPLE_1 = """{
  "title": "Smart Wardrobe",
  "description": "A device that combines a smart home garden and a virtual personal stylist. The device will be able to recommend clothing and accessories based on a person's preferences, body type, and occasion. It will also be able to grow plants indoors using hydroponics and AI, which can be used to make natural dyes or fabrics. The device will connect to a smartphone app where users can monitor and control the device.",
  "noveltyScore": 0.8,
  "marketScore": 0.3,
  "usefulnessScore": 0.2,
  "easeOfImplementationScore": 0.2,
  "impactScore": 0.2
}"""
    PROMPT_QUERY = f"""
Do the same with the following pair. Create a novel concept which takes both ideas and combines a single, coherent and useful idea.

[
  {'{'}
    "title": "{dreamPair[0].title}",
    "description": "{dreamPair[0].description}"
  {'}'},
  {'{'}
    "title": "{dreamPair[1].title}",
    "description": "{dreamPair[1].description}"
  {'}'}
]

Return only one JSON object (like before).
"""

    return [
        {"role": "system", "content": PROMPT_SYSTEM},
        {"role": "user", "content": PROMPT_USER_INPUT_1},
        {"role": "assistant", "content": PROMPT_EXAMPLE_1},
        {"role": "user", "content": PROMPT_QUERY}
      ]