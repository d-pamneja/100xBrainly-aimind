# Importing the dependencies
from .dependencies import *
from src.dependencies import *
from src.query_doc.utils import *
from src.query_doc.prompts import *
from .data_model import *


# Initialising the API from FastAPI and APIRouter
app = FastAPI(prefix="/aimind")
origins = [
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return "Hello from 100xBrainly AI Mind!"

# VectorDB Record Creation Endpoint
@app.post("/aimind/storeDoc",response_model = UpsertResponse)
async def storeDoc(query: StoreDoc = Body(...)):
    """AI Mind endpoint to store a Text/PDF document as pinecone records."""
    try:
        if(validators.url(query.initial_query.file_url)):
            # Initial document Creation
            all_documents = load_data(query.initial_query.file_url,query.initial_query.file_type)
            logging.info("Initial document chunk set.")

            # Chunked documents Creation
            all_chunked_documents = chunk_data(all_documents)
            logging.info("Chunked documents set.")
            
            # Pinecone Record Creation
            vectors = create_vectors(all_chunked_documents,query.doc_info.key,query.doc_info.userID,query.doc_info.type)
            logging.info("Records list created.")
            
            # Pinecone Record Upload
            record_status = upsert_vectors(PINECONE_INDEX_NAME,vectors)
            final_upload_status = {"response": {"upserted_count": record_status.get('upserted_count', 0)}}
            logging.info("Records uploaded.")
            
            return final_upload_status
        else :
            raise HTTPException(status_code=400, detail="Invalid link type")
        
    except CustomException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# VectorDB Record Deletion Endpoint
@app.delete("/aimind/deleteDoc",response_model = DeleteResponse)
async def deleteDoc(query: DeleteDoc = Body(...)):
    """AI Mind endpoint to delete all records of a given document."""
    try:
        # Deleting documents
        key = query.key.replace(" ", "_")
        final_response = delete_vectors(key)
        if(final_response=={}):
            logging.info("Response for query generated by LLM.")
            answer = {"response" : f"All records associated with {query.key} deleted successfully"}
            return answer
        else:
            raise HTTPException(status_code=400, detail="Could not delete vectors from pinecone index")
        
    except CustomException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
@app.post("/aimind/chat",response_model=RAGResponse)
async def chat(query : GetRAGResponse = Body(...)):
    """AI Mind endpoint to fetch answer of a query from relevant documents."""
    try:
        # Query processing
        final_response = get_final_response(query.user_query,query.userID,query.key)
        logging.info("Response for query generated by LLM.")
        
        answer = {"response": final_response}
        logging.info(f"Final answer : {answer}")
        return answer
        
    except CustomException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")