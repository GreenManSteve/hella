def handler(event, context):
    """
    Legacy health check handler - used by 'Hella' to determine whether service
    is healthy. This mechanism was agreed prior to the IT team involvement
    there is a view this endpoint is not effective in determining API health
    and another mechanism should be used - TBC
    :param event: AWS Event
    :param context: AWS Context
    :return:
    """
    return {
        "statusCode": 200,
        "body": 'ok',
        "headers": {"Content-Type": "application/json"},
    }
