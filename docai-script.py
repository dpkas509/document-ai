from google.api_core.client_options import ClientOptions
from google.cloud import documentai
#import google.cloud.documentai_v1 as documentai
from google.oauth2 import service_account
import os
from typing import Iterator, MutableSequence, Optional, Sequence, Tuple
from tabulate import tabulate


#PROJECT_ID              = "docaiproject-397718"
PROJECT_ID              = "432504274180"

LOCATION                = "us" 
PROCESSOR_ID            = "5bf13d718d639b30" 
PROCESSOR_DISPLAY_NAME  = "docai-proc" 
PROCESSOR_PATH          = "projects/432504274180/locations/us/processors/5bf13d718d639b30"
FILE_PATH1               = "D:/Pyscripts/document-ai/docaivenv/Winnie_the_Pooh_3_Pages.pdf"
FILE_PATH2               = "D:/Pyscripts/document-ai/docaivenv/health-intake-form.pdf"
MIME_TYPE               = "application/pdf"

#authentication
SERVICE_ACCOUNT_FILE    = 'D:/Pyscripts/document-ai/docaiproject-service-account-397718-31c1dbd5e485.json'
credentials             = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)


# Instantiates a client
docai_client = documentai.DocumentProcessorServiceClient(credentials=credentials,
    client_options=ClientOptions( api_endpoint=f"{LOCATION}-documentai.googleapis.com")
)

parent = docai_client.common_location_path(PROJECT_ID, LOCATION)


def list_processors() -> MutableSequence[documentai.Processor]:
    processors = docai_client.list_processors(parent=parent)
    for processor in processors:
        print("processorname:",processor.name)
        print(processor.display_name)




def process_winnie_pdf():
    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    RESOURCE_NAME = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
    print("Document processing in progressś")
    # Read the file into memory
    with open(FILE_PATH1, "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=MIME_TYPE)

    # Configure the process request
    request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)

    # Use the Document AI client to process the sample form
    result = docai_client.process_document(request=request)

    document_object = result.document
    print("Document processing complete.")
    print(f"Text: {document_object.text}")



def process_form_file(processor: documentai.Processor, file_path: str, mime_type: str,) -> documentai.Document:
    with open(file_path, "rb") as document_file:
        document_content = document_file.read()
    document = documentai.RawDocument(content=document_content, mime_type=mime_type)
    request = documentai.ProcessRequest(raw_document=document, name=PROCESSOR_PATH)
    response = docai_client.process_document(request)

    return response.document

list_processors()
#process_winnie_pdf()
process_form_file(documentai.Processor,  FILE_PATH2, MIME_TYPE)
