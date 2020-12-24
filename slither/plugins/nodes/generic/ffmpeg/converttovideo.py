import os

from slither import api


class ConvertToVideo(api.PXComputeNode):
    Type = "convertToVideo"

    def compute(self, context):
        import ffmpeg
        directory = os.path.normpath(context.directory.value())
        (
            ffmpeg
                .input(os.path.join(directory, context.pattern.value()), framerate=context.framerate.value())
                .output(context.outputPath.value())
                .run()
        )
