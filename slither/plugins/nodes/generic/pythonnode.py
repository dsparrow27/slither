from slither import api


class PythonNode(api.PXComputeNode):
    Type = "python"

    def compute(self, context):
        script = context.script.value()
        if not script:
            raise ValueError("")
        script = script.replace(u"\u2029", "\n")
        evalCode = True
        _locals = {"context": context}
        try:
            outputCode = compile(script, "<string>", "eval")
        except SyntaxError:
            evalCode = False
            outputCode = compile(script, "<string>", "exec")
        except Exception:
            raise
        # ok we've compiled the code now exec
        if evalCode:
            try:
                eval(outputCode, globals(), _locals)
            except Exception:
                raise
        else:
            try:
                exec(outputCode, globals(), _locals)
            except Exception:
                raise
