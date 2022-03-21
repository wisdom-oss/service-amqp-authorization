"""A collection of tools which are used multiple times in this service"""
import asyncio


async def is_host_available(
        host: str,
        port: int,
        timeout: float = 10.0
) -> bool:
    """
    Check if the specified host is reachable on the specified port.
    
    :param host: The hostname or ip-address of the service that shall be checked
    :type host: str
    :param port: The port of the service which shall be checked
    :type port: int
    :param timeout: The time that is waited until the operation times out
    :type timeout: float
    :return: ``True`` if the host is reachable on the specified port
    :rtype: bool
    """
    try:
        # Try opening a stream to the specified host and port
        _reader, _writer = await asyncio.wait_for(
            asyncio.open_connection(
                host,
                port
            ), timeout=timeout
        )
        # Close the writer and wait until it is closed
        _writer.close()
        await _writer.wait_closed()
        return True
    except:  # pylint: disable=bare-except
        return False
