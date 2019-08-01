import sys
sys.path.insert(0, './AirSim/car')
import setup_path
import airsim
import json


def read_json(fn):

    with open(fn) as json_file:
        data = json.load(json_file)
        for key in data:
            print(data[key])


if __name__ == "__main__":
    args = sys.argv
    args.pop(0)

    fn_json = 'lidar.json'
    read_json(fn_json)

