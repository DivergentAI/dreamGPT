import argparse
from dreamgpt.constants import MAX_ITERATIONS
from dreamgpt.engine.dreamEngine import DreamEngine

def main():
    dreams = []
    engine = DreamEngine()
    parser = argparse.ArgumentParser(description='dreamGPT')
    parser.add_argument('-t', '--theme', type=str, help='Specify a theme for your dreams')
    args = parser.parse_args()
    themeSeeds = engine.expandTheme(args.theme)
    maxIterations = MAX_ITERATIONS
    while maxIterations > 0:
        newDreams = engine.dream(themeSeeds)
        combinedDreams = engine.combine(newDreams + dreams)
        dreams = engine.pick(combinedDreams + newDreams + dreams)
        maxIterations -= 1
