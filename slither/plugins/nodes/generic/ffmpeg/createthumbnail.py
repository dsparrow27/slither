import ffmpeg

from slither.core import attribute
from slither.core import node


class ConvertToVideo(node.BaseNode):
    Type = "ConvertToVideo"
    category = "ffmpeg"
    documentation = "Convert's an image sequence to a video"
    input = attribute.AttributeDefinition(isInput=True, type_="directory", default="", required=True)
    frame = attribute.AttributeDefinition(isInput=True, type_="int", default=0, required=True)
    outputPath = attribute.AttributeDefinition(isInput=True, type_="file", default="", required=True)
    output = attribute.AttributeDefinition(isOutput=True, type_="file", array=True, default="")

    def execute(self):
        (
            ffmpeg
                .input(self.input.value(), ss=1)
                .output(self.outputPath.value(), vframes=1)
                .run()
        )
