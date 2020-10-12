from slither import api


class ConvertToVideo(api.ComputeNode):
    Type = "convertToVideo"
    # category = "ffmpeg"
    # documentation = "Convert's an image sequence to a video"
    # input = api.AttributeDefinition(input=True, type_=api.types.kDirectory, default="", required=True)
    # frame = api.AttributeDefinition(input=True, type_=api.types.kInt, default=0, required=True)
    # outputPath = api.AttributeDefinition(input=True, type_=api.types.kFile, default="", required=True)
    # output = api.AttributeDefinition(output=True, type_=api.types.kFile, array=True, default="")

    def execute(self, context):
        import ffmpeg

        (
            ffmpeg
                .input(context.input.value(), ss=1)
                .output(context.outputPath.value(), vframes=1)
                .run()
        )
        
