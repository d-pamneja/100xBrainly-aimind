# Importing the dependencies
import uvicorn
from API.resource import app

# Running the App with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
