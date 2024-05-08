from fastapi import FastAPI,WebSocket, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import fitz  # PyMuPDF
import os
import uvicorn
from nltk.tokenize import sent_tokenize
from tqdm import tqdm
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
import logging
# Ensure NLTK data is downloaded
import nltk
from openai import OpenAI, AuthenticationError
import openai

def is_api_key_valid(key):
    client = OpenAI(
        api_key=key
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-3.5-turbo",
        )
        return True  # 如果没有错误，返回 True 表示密钥有效
    except AuthenticationError:
        return False  # 如果捕获到 AuthenticationError，返回 False 表示密钥无效
    except Exception as e:
        return False  # 如果捕获到其他异常，也返回 False 表示可能存在其他问题


nltk.download('punkt')
# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except Exception as e:
        await websocket.close()
        print(f"WebSocket closed with exception: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def load_from_text(fstarter : str, text: str, split_size : int, overlap : int):
    text = sent_tokenize(text)
    i = 0
    data = []
    while i < len(text):
        splits = [fstarter]
        splits.extend(text[i:i+split_size])
        data.append(" ".join(splits))
        i = i + (split_size - overlap)

    return data

def extract_text_from_pdf(content):
    """Extract text from PDF bytes."""
    with fitz.open(stream=content, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

@app.post("/process-filings/")

async def process_filings(
    file: UploadFile = File(...),
    openai_key: str = Form(...),
    # fmp_key: str = Form(...),
    query: str = Form(...),

):
    if not is_api_key_valid(openai_key):
        return JSONResponse(content={"message": "ERROR: Your openai_key not vaild"})

    # 使用 logger.info() 来代替 print()
    logger.info("11")
    logger.info("Received openai_key:", openai_key)
    # logger.info("Received fmp_key:", fmp_key)
    logger.info("Received query:", query)



    # Read the uploaded PDF file
    file_contents = await file.read()
    if not file_contents:
        raise HTTPException(status_code=400, detail="File is empty")
    # Read the uploaded PDF file
    logger.info("Received file size:", len(file_contents))

    if not file_contents:
        raise HTTPException(status_code=400, detail="File is empty")
    document_text = extract_text_from_pdf(file_contents)

    # Setup environment and APIs
    os.environ["OPENAI_API_KEY"] = openai_key

    # Process the text from the PDF
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    split_size = 15
    overlap = 1
    fstarter = "Information extracted from the uploaded document."
    chunked_data = load_from_text(fstarter, document_text, split_size, overlap)

    if not os.path.exists("./content/faiss_db"):
        vectorstore = FAISS.from_texts(chunked_data, embedding=embeddings)
        vectorstore.save_local(folder_path="./content", index_name="FinancialIndex")

    vectorstore = FAISS.load_local(
        folder_path="./content",
        embeddings=embeddings,
        index_name="FinancialIndex",
        allow_dangerous_deserialization=True)

    sources = vectorstore.similarity_search_with_relevance_scores(query, k=10)
    top_k_docs = 3

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, max_retries=10)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": top_k_docs})
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        verbose=True,
        return_source_documents=True
    )

    result = qa(query)

    # Return the query results
    return JSONResponse(content={"message": result["result"]})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
