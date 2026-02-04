from app.records.response import Response

class NOT_FOUND_404(Response):
    
    def __init__(self, page, path):
        return super().__init__(f"Not Found Page: {page} in {path}", 404)

class INTERNAL_ERROR_500(Response):
    
    def __init__(self):
        self.content: str = "Internal Server Error"
        self.status_code = 500
        super().__init__()

class ERROR_DURING_PROCESS_515(Response):
    
    def __init__(self, e):
        return super().__init__(f"ERROR DURING PROCESS: {e}", 515)

