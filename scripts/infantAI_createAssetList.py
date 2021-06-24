import json

assetList = {
    "availableObjects": [
        {"pair": 1, "objectID": "Tomato|-05.00|+00.02|+00.00", "x": 0, "y": .022, "z": -.402}
    ],
    "availableContainers": [
        {"pair": 1, "objectID": "Pot|-05.00|+00.00|+00.00", "x": 0, "y": 0, "z": 0}
    ]
}

with open("scripts/assetList.txt", "w") as outfile:
    json.dump(assetList, outfile)
