from dreamgpt.engine.dreamEngine import DreamEngine

def main():
    dreams = []
    engine = DreamEngine()
    maxIterations = 5
    while maxIterations > 0:
        newDreams = engine.dream()
        combinedDreams = engine.combine(newDreams + dreams)
        dreams = engine.pick(combinedDreams + newDreams + dreams)
        maxIterations -= 1
