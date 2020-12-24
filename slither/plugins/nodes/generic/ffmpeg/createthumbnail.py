from slither import api


class ConvertToVideo(api.PXComputeNode):
    Type = "convertToVideo"

    def compute(self, context):
        import ffmpeg

        (
            ffmpeg
                .input(context.input.value(), ss=1)
                .output(context.outputPath.value(), vframes=1)
                .run()
        )
