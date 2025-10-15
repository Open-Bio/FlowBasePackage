import random

from uflow.Core import FunctionLibraryBase, IMPLEMENT_NODE
from uflow.Core.Common import *


class RandomLib(FunctionLibraryBase):
    """doc string for RandomLib"""

    def __init__(self, packageName):
        super(RandomLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=None,
        meta={
            NodeMeta.CATEGORY: "Math|random",
            NodeMeta.KEYWORDS: [],
            NodeMeta.CACHE_ENABLED: False,
        },
    )
    # Return a random integer N such that a <= N <= b
    def randint(start=("IntPin", 0), end=("IntPin", 10), Result=(REF, ("IntPin", 0))):
        """Return a random integer N such that a <= N <= b."""
        Result(random.randint(start, end))

    @staticmethod
    @IMPLEMENT_NODE(
        returns=None, meta={NodeMeta.CATEGORY: "Math|random", NodeMeta.KEYWORDS: []}
    )
    # Shuffle the sequence x in place
    def shuffle(
        seq=("AnyPin", [], {PinSpecifiers.CONSTRAINT: "1"}),
        Result=(REF, ("AnyPin", [], {PinSpecifiers.CONSTRAINT: "1"})),
    ):
        """Shuffle the sequence x in place."""
        random.shuffle(seq)
        Result(seq)
