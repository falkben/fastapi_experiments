


blocksize = int(1024 * 1024 / 4)

async def stream_command_async(proc, logger=None, blksize=blocksize):
    """
        Generator
        Yields the result of a unix command in chunks of blocksize
    """
    # TODO: Change this to pass in the command and create the process here
    # proc = await asyncio.create_subprocess_exec(*cmd,
    #                                             stdout=asyncio.subprocess.PIPE)

    # proc. returncode does not get set all the time so we can't use this
    # to test when to stop. Instead we stop when there is no more data to read
    data = await proc.stdout.read(blksize)
    while len(data) != 0:
        yield data
        data = await proc.stdout.read(blksize)
    # TODO: Do we want to catch/log asyncio.CancelledError here?

    try:
        if proc.returncode is None:
            proc.terminate()
            code = await proc.wait()
        else:
            code = proc.returncode

        # If we have a non-zero exit code and pass in a logger, log the error code
        if code != 0 and logger:
            logger.error("Stream command exited with error: %s", code)

    except ProcessLookupError:
        # Occasionally the process is terminated and already gone
        # from the os, so we have to catch and ignore this error
        pass

