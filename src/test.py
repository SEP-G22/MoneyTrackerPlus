
if __name__ == '__main__':
    pass


def test_service():
    # Example usage of DataService and CloudSyncService

    from services import DataService
    from services import CloudSyncService

    # Initialize DataService with a local JSON file path
    data_service = DataService('data.json')

    # Add a new record
    new_record = {'id': 1, 'name': 'Sample Record', 'amount': 100}
    data_service.add_record(new_record)

    # Read data
    data = data_service.read_data()
    print('Data read from local file:', data)

    # Update a record
    updated_record = {'id': 1, 'name': 'Updated Record', 'amount': 150}
    data_service.update_record(1, updated_record)

    # Delete a record
    data_service.delete_record(1)

    # Initialize CloudSyncService with Firebase credentials
    cloud_sync_service = CloudSyncService('path/to/credentials.json')

    # Upload data to Firestore
    cloud_sync_service.upload_data('collection_name', data)

    # Download data from Firestore
    downloaded_data = cloud_sync_service.download_data('collection_name')
    print('Data downloaded from Firestore:', downloaded_data)
