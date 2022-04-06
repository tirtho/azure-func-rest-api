import logging
from stat import FILE_ATTRIBUTE_ARCHIVE

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    restMethod = req.method
    requestFiles = req.files
    logging.info('Received HTTP %s request' %restMethod)

    if (restMethod == 'GET'):
        name = req.params.get('name')
        if not name:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                name = req_body.get('name')

        if name:
            return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
        else:
            return func.HttpResponse(
                "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
                status_code=200
            )
    if (restMethod == 'POST'):
        attachedFileCount = 0
        try:
            for file in req.files.values():
                filename = file.filename
                #contents = filename.stream.read()
                logging.info('Attached file name is %s' %filename)
                #logging.info('Contents:')
                #logging.info(contents)
                attachedFileCount += 1
        except ValueError:
            logging.info("Failed to parse the attached file from http %s request" %restMethod)
        return func.HttpResponse(f"%s number of attached files read from HTTP %s request" %(attachedFileCount, restMethod), status_code=200)
            
    return func.HttpResponse(f"%s request is not yet implemented" %restMethod)