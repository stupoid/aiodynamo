from pyperf import Runner
from utils import generate_data

from new_deserialize import deserialize

data = generate_data()


def deserialize_new():
    result = [{k: deserialize(v, float) for k, v in item.items()} for item in data]


Runner().bench_func("deserialize", deserialize_new)
