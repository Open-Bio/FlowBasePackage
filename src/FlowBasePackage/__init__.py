import os
from uflow.Core.PackageBase import PackageBase


class FlowBasePackage(PackageBase):
    """Base uflow package"""

    def __init__(self):
        super(FlowBasePackage, self).__init__()
        self.analyzePackage(os.path.dirname(__file__))
