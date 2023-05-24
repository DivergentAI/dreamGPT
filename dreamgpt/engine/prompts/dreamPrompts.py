import random
import os

from dreamgpt.constants import THEME_SEEDS_WEIGHT

def dreamPrompt(themeSeeds, count = 6):
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "commonWords.txt")
    wordFile = open(file_path, "r")
    words = wordFile.readlines()
    wordFile.close()
    cleanWords = [line.strip() for line in words]
    randomTopics = []
    if len(themeSeeds) > 0:
        seedTopicCount = int(count * THEME_SEEDS_WEIGHT)
        seedTopics = random.sample(themeSeeds, seedTopicCount)
        randomTopics = seedTopics + random.sample(cleanWords, count - seedTopicCount)
    else:
        randomTopics = random.sample(cleanWords, count)
    print(randomTopics)
    PERSONAS = ["I want to you to act as an Ideation Expert. An Ideation Expert has strong creative, problem-solving and analytical skills, " \
                  "with knowledge of research methods and design thinking. They should be adept at identifying " \
                  "opportunities and generating ideas, as well as have the ability to communicate and collaborate " \
                  "with others. Additionally, they must have an understanding of the latest trends and technology " \
                  "in their industry.",
                "I want to you to act as a Creative director. A Creative Director is an experienced and knowledgeable leader with a passion for visual arts and design. " \
                  "They have a keen eye for detail and a strong understanding of the principles of design. " \
                  "They also possess excellent communication skills, problem-solving abilities, and the ability " \
                  "to manage teams and projects. They also have a deep knowledge of the latest industry trends and technology.",
                "I want to you to act as an Idea Generator. An Idea Generator has an innovative mindset and a " \
                  "creative spirit, which they use to develop unique concepts and solutions. They should have " \
                  "extensive knowledge of various industries, trends, and technologies. Additionally, they should " \
                  "possess strong research skills and the ability to think critically and objectively. Communication " \
                  "and collaboration skills are also essential to work effectively with other stakeholders." ]
    PROMPT_SYSTEM = random.choice(PERSONAS)
    PROMPT_USER_INPUT_1 = "You will generate a list of random ideas and concepts that " \
                  "can be used to spark creativity and inspire new projects. You will consider a wide range of topics, " \
                  "such as art, technology, business, and more, in order to come up with original ideas that can be used " \
                  "in various contexts.\n" \
                  "Think out of the box and bring concepts from nature, science, art, etc. " \
                  "Each item will be scored in a scale from 0 to 1 based on the following criteria:\n" \
                  " - noveltyScore: measures how unique and distinct this concept is from anything else seen before.\n" \
                  " - marketScore: measures the potential market ($$$) for this concept.\n" \
                  " - usefulnessScore: measures the potential benefit of use of this concept.\n" \
                  " - easeOfImplementationScore: measures how easy it would be to make this concept a reality.\n" \
                  " - impactScore: measures the potential positive impact in the world of this concept.\n\n" \
                  "You will generate a JSON list with 1 concept related to [\"art\"]."
    PROMPT_EXAMPLE_1 = """[
  {
    "title": "Interactive Art Installation",
    "description": "A large-scale art installation that encourages public interaction and engagement, using elements such as sound, light, and motion.",
    "noveltyScore": 0.4,
    "marketScore": 0.3,
    "usefulnessScore": 0.3,
    "easeOfImplementationScore": 0.2,
    "impactScore": 0.5
  }
]"""
    PROMPT_USER_INPUT_2 = "You will generate a JSON list with 2 concepts related to [\"healthcare\", \"fashion\"]. Don't repeat the previous examples."
    PROMPT_EXAMPLE_2 = """[
  {
    "title": "AR-Assisted Healthcare",
    "description": "An augmented reality system that helps healthcare providers visualize and interact with patient data and medical images in real-time.",
    "noveltyScore": 0.4,
    "marketScore": 0.3,
    "usefulnessScore": 0.3,
    "easeOfImplementationScore": 0.2,
    "impactScore": 0.5
  },
  {
    "title": "Sustainable Fashion Line",
    "description": "A fashion line that uses sustainable materials and ethical production practices to reduce its impact on the environment.",
    "noveltyScore": 0.5,
    "marketScore": 0.7,
    "usefulnessScore": 0.6,
    "easeOfImplementationScore": 0.3,
    "impactScore": 0.8
  }
]"""
    SEPARATOR = "\", \""
    PROMPT_QUERY = f"You will generate a JSON list with {count} concepts related to [{SEPARATOR.join(randomTopics)}]. Don't repeat the previous examples."

    return [
        {"role": "system", "content": PROMPT_SYSTEM},
        {"role": "user", "content": PROMPT_USER_INPUT_1},
        {"role": "assistant", "content": PROMPT_EXAMPLE_1},
        {"role": "user", "content": PROMPT_USER_INPUT_2},
        {"role": "assistant", "content": PROMPT_EXAMPLE_2},
        {"role": "user", "content": PROMPT_QUERY}
      ]