import os

import ffmpeg

from slither.core import attribute
from slither.core import node


class ConvertToVideo(node.BaseNode):
    Type = "ConvertToVideo"
    category = "ffmpeg"
    documentation = "convert's an image sequence to a video"
    directory = attribute.AttributeDefinition(isInput=True, type_="directory", default="", required=True)
    pattern = attribute.AttributeDefinition(isInput=True, type="str", default="%03d", required=True)
    framerate = attribute.AttributeDefinition(isInput=True, type="int", default=25, required=True)
    outputPath = attribute.AttributeDefinition(isInput=True, type_="file", default="", required=True)
    output = attribute.AttributeDefinition(isOutput=True, type_="file", array=True, default="")

    def execute(self):
        directory = os.path.normpath(self.directory.value())
        (
            ffmpeg
                .input(os.path.join(directory, self.pattern.value()), framerate=self.framerate.value())
                .output(self.outputPath.value())
                .run()
        )
