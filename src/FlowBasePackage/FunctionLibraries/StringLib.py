import random

from uflow.Core import FunctionLibraryBase, IMPLEMENT_NODE
from uflow.Core.Common import *


class StringLib(FunctionLibraryBase):
    """doc string for StringLib"""

    def __init__(self, packageName):
        super(StringLib, self).__init__(packageName)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def lower(s=("StringPin", "")):
        return str.lower(s)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def upper(s=("StringPin", "")):
        return str.upper(s)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def tostring(s=("AnyPin", 0)):
        return str(s)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def isEmpty(s=("StringPin", "")):
        return len(s) <= 0

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def notEmpty(s=("StringPin", "")):
        return len(s) > 0

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("BoolPin", False),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def equal(l=("StringPin", ""), r=("StringPin", "")):
        return l == r

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def strimp(s=("StringPin", ""), chars=("StringPin", "")):
        return s.strip(chars)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def lstrip(s=("StringPin", ""), chars=("StringPin", "")):
        return s.lstrip(chars)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def rstrip(s=("StringPin", ""), chars=("StringPin", "")):
        return s.rstrip(chars)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=(
            "StringPin",
            [],
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.ENABLED_OPTIONS: PinOptions.ArraySupported,
            },
        ),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def split(s=("StringPin", ""), sep=("StringPin", "")):
        return str.split(s, sep)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=(
            "StringPin",
            [],
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.ENABLED_OPTIONS: PinOptions.ArraySupported,
            },
        ),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def starstWith(
        s=("StringPin", ""),
        prefix=(
            "StringPin",
            "",
            {
                PinSpecifiers.ENABLED_OPTIONS: PinOptions.ArraySupported
                | PinOptions.ChangeTypeOnConnection
            },
        ),
    ):
        return s.startswith(prefix)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=(
            "StringPin",
            [],
            {
                PinSpecifiers.CONSTRAINT: "1",
                PinSpecifiers.ENABLED_OPTIONS: PinOptions.ArraySupported,
            },
        ),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def endsWith(
        s=("StringPin", ""),
        suffix=(
            "StringPin",
            "",
            {
                PinSpecifiers.ENABLED_OPTIONS: PinOptions.ArraySupported
                | PinOptions.ChangeTypeOnConnection
            },
        ),
    ):
        return s.endswith(suffix)

    @staticmethod
    @IMPLEMENT_NODE(
        returns=("StringPin", ""),
        meta={NodeMeta.CATEGORY: "String", NodeMeta.KEYWORDS: []},
    )
    def concat(s1=("AnyPin", ""), s2=("AnyPin", "")):
        return str(s1) + str(s2)
