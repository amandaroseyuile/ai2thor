import json

assetList = {
    "availableObjects": [
        {"pair": 1, "objectId": "Tomato|-05.00|+00.00|+00.00", "x": -.34, "y": .818, "z": -.279}
        ],
    
    "availableCovers": [
        {"pair": 1, "objectId": "Pot|-05.00|+00.00|+00.00", "x": 0, "y": .89, "z": -.244}
    ]
}

with open("scripts/assetList.json", "w") as outfile:
    json.dump(assetList, outfile)
