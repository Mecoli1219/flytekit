import shlex
import subprocess
import tempfile

from flytekit.loggers import logger


def check_call(cmd_args, **kwargs):
    if not isinstance(cmd_args, list):
        cmd_args = shlex.split(cmd_args)

    # Jupyter notebooks hijack I/O and thus we cannot dump directly to stdout.
    with tempfile.TemporaryFile() as std_out:
        with tempfile.TemporaryFile() as std_err:
            ret_code = subprocess.Popen(cmd_args, stdout=std_out, stderr=std_err, **kwargs).wait()

            # Dump sub-process' std out into current std out
            std_out.seek(0)
            logger.info("Output of command '{}':\n{}\n".format(cmd_args, std_out.read()))

            if ret_code != 0:
                std_err.seek(0)
                err_str = std_err.read()
                logger.error("Error from command '{}':\n{}\n".format(cmd_args, err_str))

                raise RuntimeError(
                    "Called process exited with error code: {}.  Stderr dump:\n\n{}".format(ret_code, err_str)
                )

    return 0
