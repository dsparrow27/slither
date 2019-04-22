import ffmpeg

from slither import api


class ConvertToVideo(api.ComputeNode):
    Type = "ConvertToVideo"
    category = "ffmpeg"
    documentation = "Convert's an image sequence to a video"
    input = api.AttributeDefinition(isInput=True, type_=api.types.kDirectory, default="", required=True)
    frame = api.AttributeDefinition(isInput=True, type_=api.types.kInt, default=0, required=True)
    outputPath = api.AttributeDefinition(isInput=True, type_=api.types.kFile, default="", required=True)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFile, array=True, default="")

    def execute(self, context):
        (
            ffmpeg
                .input(self.input.value(), ss=1)
                .output(self.outputPath.value(), vframes=1)
                .run()
        )
