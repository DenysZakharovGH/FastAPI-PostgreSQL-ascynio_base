import uvicorn
from fastapi import FastAPI

app = FastAPI


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    # Will watch for changes in these directories
    # create automatic reload with saving files,
    # show path to file and fast API object to reload

