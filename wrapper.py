class Wrapper(object):

    xctool_loc = '/Users/mtford/Scripts/XCTool/build/Products/Release/xctool'

    cmd = "{xctool} " \
          "-workspace {workspace} " \
          "-scheme {scheme} " \
          "test -only '{only}' " \
          "-sdk {sdk} -reporter json-stream"

    def __init__(self):
        super(Wrapper, self).__init__()

    def _build_only(self, test):
        """-only target:test_case/test"""
        pass

    # def _build_bash_cmd(self, test, only):
    #     return self.cmd.format(xctool=self.xctool_loc,
    #                       workspace=)