import webbrowser
from slither import api


class WebOpen(api.PXComputeNode):
    Type = "webOpen"

    def compute(self, context):

        url = context.url.value()
        webbrowser.open_new_tab(url)


class WebDownload(api.PXComputeNode):
    Type = "webDownload"

    def compute(self, context):
        from urllib import request
        url = context.url.value()
        filePath = context.filePath.value()
        fileName, _ = request.urlretrieve(url, filePath or None)
        context.outputPath.setValue(fileName)
