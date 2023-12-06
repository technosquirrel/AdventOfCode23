import re
import time

def main():

    start_time = time.time()
    input = "input.txt"
    seeds, mappings = loadInput(input)
    mappings = processMappings(mappings)
    
    locations = []
    for seed in seeds:
        locations.append(getLocation(seed, mappings))
    print(time.time() - start_time)
    print(min(locations))

    # Part 2
    # The plan is to get the lowest and highest value from each mapping range for each seed
    start_time = time.time()
    seedRanges = getRanges(seeds)
    # Sort stuff to make processing easier
    collapseAndSort(seedRanges)

    for mapping in mappings:
        # Sort to make finding ranges easier
        mapping.sort(key=lambda m: m["start"])
        mapping = fillGaps(mapping)
        seedRanges = getSplitRanges(seedRanges, mapping)
        buffer = []
        for r in seedRanges:
            buffer.append({
                "start" : mapSeed(mapping, r["start"]),
                "end" : mapSeed(mapping, r["end"])
            })
        collapseAndSort(buffer)
        seedRanges = buffer
    print(time.time() - start_time)
    print(seedRanges[0]["start"])
    


def loadInput(filename):

    seeds = []
    mappings = []
    with open(filename) as file:
        seeds = [int(x) for x in file.readline().strip().split() if x.isnumeric()]
        dump = file.read()
        mappings = getMappings(dump)

    return [seeds, mappings]


def getMappings(s):

    mappings = []
    matches = re.findall(r"(?::\n)((?:(?:\d+ \d+ \d+)\n?)+)(?:\n\n)?", s, re.MULTILINE)

    for match in matches:
        buffer = match.strip().split("\n")
        mapping = []
        for item in buffer:
            mapping.append([int(n) for n in item.split()])
        mappings.append(mapping)

    return mappings


def processMappings(maps):

    processed = []
    for map in maps:
        newMap = []
        for line in map:
            newMap.append({
                "start" : line[1],
                "end" : line[1] + line[2] - 1,
                "difference" : line[0] - line[1],
            })
        processed.append(newMap)
    return processed


def getLocation(seed, mappings):

    n = seed
    for map in mappings:
        n = mapSeed(map, n)

    return n


def mapSeed(map, n):

    for m in map:
        if m["start"] <= n <= m["end"]:
            return n + m["difference"]

    return n


def getRanges(arr):
    
    buffer = []
    for i in range(0, len(arr), 2):
        buffer.append({
            "start" : arr[i],
            "end" : arr[i] + arr[i + 1] - 1 
        })
    return buffer

def collapseAndSort(arr):

    arr.sort(key=lambda s: s["start"])
    for i in range(len(arr) - 1, 0, -1):
        if arr[i]["start"] - 1 <= arr[i - 1]["end"]:
            arr[i - 1]["end"] = arr[i]["end"] if arr[i]["end"] > arr[i - 1]["end"] else arr[i - 1]["end"]
            del arr[i]


def getSplitRanges(arr, mapping):

    buffer = []

    for r in arr:
        currentRange = r
        for map in mapping:
            if currentRange["start"] > map["end"]:
                continue
            elif currentRange["start"] >= map["start"] and currentRange["end"] <= map["end"]:
                buffer.append(currentRange)
                break
            elif currentRange["start"] >= map["start"] and currentRange["end"] > map["end"]:
                buffer.append({
                        "start" : currentRange["start"],
                        "end" : map["end"]
                    })
                currentRange = {
                        "start" : map["end"] + 1,
                        "end" : currentRange["end"]
                    }
            else:
                raise Exception("Case not found!!!")
        if currentRange not in buffer:
            buffer.append(currentRange)

    return buffer


def fillGaps(mapping):

    if mapping[0]["start"] != 0:
            mapping.insert(0, {
                "start" : 0,
                "end" : mapping[0]["start"] - 1,
                "difference" : 0
            })

    buffer = []

    for i in range(len(mapping) - 1):
        buffer.append(mapping[i])
        if mapping[i]["end"] + 1 < mapping[i + 1]["start"]:
            buffer.append({
                "start" : mapping[i]["end"] + 1,
                "end" : mapping[i + 1]["start"] - 1,
                "difference" : 0
            })
    
    buffer.append(mapping[-1])
    return buffer


if __name__ == "__main__":
    main()