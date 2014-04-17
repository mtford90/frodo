from runner.frodo_base import FrodoBase


class XCToolConfig(FrodoBase):
    """XCTool configuration"""
    required_attr = 'workspace', 'scheme', 'sdk'