# Importing the dependencies
import uvicorn
from API.resource import app

# Running the App with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="100x-brainly-aimind.vercel.app", port=8080)