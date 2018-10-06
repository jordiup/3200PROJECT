class DocumentEntity:
    def __init__(self, archive_number, date_written, document_type, language, place_written, sender_name, receiver_name):
        self.archive_number = archive_number
        self.date_written = date_written
        self.document_type = document_type
        self.language = language
        self.place_written = place_written
        self.sender_name = sender_name
        self.receiver = receiver_name