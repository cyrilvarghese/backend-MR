# slides_generator.py
import json
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import uuid

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations']

def create_title_slide(service, presentation_id, title):
    title_id = f'title_{uuid.uuid4().hex}'
    
    requests = [
        {
            'createSlide': {
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE'
                },
                'placeholderIdMappings': [
                    {
                        'layoutPlaceholder': {
                            'type': 'CENTERED_TITLE'
                        },
                        'objectId': title_id
                    }
                ]
            }
        }
    ]

    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()

    requests = [
        {
            'insertText': {
                'objectId': title_id,
                'text': title
            }
        }
    ]

    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()

def create_content_slide(service, presentation_id, title, bullet_points):
    title_id = f'title_{uuid.uuid4().hex}'
    body_id = f'body_{uuid.uuid4().hex}'
    
    requests = [
        {
            'createSlide': {
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_BODY'
                },
                'placeholderIdMappings': [
                    {
                        'layoutPlaceholder': {
                            'type': 'TITLE'
                        },
                        'objectId': title_id
                    },
                    {
                        'layoutPlaceholder': {
                            'type': 'BODY'
                        },
                        'objectId': body_id
                    }
                ]
            }
        }
    ]

    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()

    requests = [
        {
            'insertText': {
                'objectId': title_id,
                'text': title
            }
        },
        {
            'insertText': {
                'objectId': body_id,
                'text': '\n'.join(f'• {point}' for point in bullet_points)
            }
        }
    ]

    service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()

def create_presentation(json_data):
    """Create a Google Slides presentation from a JSON object."""
    
    # Initialize the Google Slides API client
    creds = None
    filePath= os.path.expanduser("~/backend-mr/app/helper/credentials.json")
    flow = InstalledAppFlow.from_client_secrets_file(filePath, SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('slides', 'v1', credentials=creds)

    # Create a new presentation
    presentation = service.presentations().create(body={'title': json_data['title']}).execute()
    presentation_id = presentation['presentationId']

    # Create title slide
    create_title_slide(service, presentation_id, json_data['title'])

    # Create content slides
    for slide in json_data['content']:
        create_content_slide(service, presentation_id, slide['heading'], slide['bullet_points'])

    return f'Presentation created: https://docs.google.com/presentation/d/{presentation_id}'

# Example function usage
def main():
    # Example JSON input
    json_data = {
        "title": "Sample Presentation",
        "content": [
            {
                "heading": "Introduction",
                "bullet_points": ["Point 1", "Point 2", "Point 3"]
            },
            {
                "heading": "Conclusion",
                "bullet_points": ["Final Point"]
            }
        ]
    }

    # Create the presentation from the JSON object
    presentation_url = create_presentation(json_data)
    print(presentation_url)

if __name__ == '__main__':
    main()
