from utils.google_client import get_service


async def spreadsheets_create(label: str) -> str:
    async for aiogoogle in get_service():
        sheets = await aiogoogle.discover('sheets', 'v4')
        spreadsheet_body = {
            'properties': {
                'title': f'Отчет {label}',
                'locale': 'ru_RU'
            },
            'sheets': [{
                'properties':
                    {
                        'sheetType': 'GRID',
                        'sheetId': 0,
                        'title': 'Лист1'
                    }
            }]
        }
        response = await aiogoogle.as_service_account(
            sheets.spreadsheets.create(json=spreadsheet_body)
        )
        spreadsheet_id = response['spreadsheetId']
        return spreadsheet_id


async def set_user_permissions(spreadsheet_id: str) -> None:
    async for aiogoogle in get_service():
        permissions_body = {
            'type': 'anyone',
            'role': 'writer'
        }
        drive = await aiogoogle.discover('drive', 'v3')
        await aiogoogle.as_service_account(drive.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(spreadsheet_id: str, data: list) -> None:
    async for aiogoogle in get_service():
        sheets = await aiogoogle.discover('sheets', 'v4')
        update_body = {
            'majorDimension': 'ROWS',
            'values': data
        }
        await aiogoogle.as_service_account(sheets.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:D{len(data)+10}',
            valueInputOption='USER_ENTERED',
            json=update_body
        ))
