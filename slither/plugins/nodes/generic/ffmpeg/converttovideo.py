import os

from slither import api


class ConvertToVideo(api.ComputeNode):
    Type = "convertToVideo"
    # category = "ffmpeg"
    # documentation = "convert's an image sequence to a video"
    # directory = api.AttributeDefinition(input=True, type_=api.types.kDirectory, default="", required=True)
    # pattern = api.AttributeDefinition(input=True, type_=api.types.kString, default="%03d", required=True)
    # framerate = api.AttributeDefinition(input=True, type_=api.types.kInt, default=25, required=True)
    # outputPath = api.AttributeDefinition(input=True, type_=api.types.kFile, default="", required=True)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFile, array=True, default="")

    def execute(self, context):
        import ffmpeg
        directory = os.path.normpath(context.directory.value())
        (
            ffmpeg
                .input(os.path.join(directory, context.pattern.value()), framerate=context.framerate.value())
                .output(context.outputPath.value())
                .run()
        )
