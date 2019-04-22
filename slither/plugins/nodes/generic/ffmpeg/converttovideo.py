import os

import ffmpeg

from slither import api


class ConvertToVideo(api.ComputeNode):
    Type = "ConvertToVideo"
    category = "ffmpeg"
    documentation = "convert's an image sequence to a video"
    directory = api.AttributeDefinition(isInput=True, type_=api.types.kDirectory, default="", required=True)
    pattern = api.AttributeDefinition(isInput=True, type_=api.types.kString, default="%03d", required=True)
    framerate = api.AttributeDefinition(isInput=True, type_=api.types.kInt, default=25, required=True)
    outputPath = api.AttributeDefinition(isInput=True, type_=api.types.kFile, default="", required=True)
    output = api.AttributeDefinition(isOutput=True, type_=api.types.kFile, array=True, default="")

    def execute(self, context):
        directory = os.path.normpath(self.directory.value())
        (
            ffmpeg
                .input(os.path.join(directory, self.pattern.value()), framerate=self.framerate.value())
                .output(self.outputPath.value())
                .run()
        )
