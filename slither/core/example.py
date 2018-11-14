from slither import api

application = api.currentInstance
root = application.root
fileDir = application.createNode("files", "FilesInDirectory", parent=root)
fileDir.directory.setValue("~\Documents")
fileDir.recursive.setValue(True)
application.execute(root, application)
fileDir.output.value()


