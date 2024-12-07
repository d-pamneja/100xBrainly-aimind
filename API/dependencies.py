from fastapi import FastAPI, Depends, HTTPException, status, Query,Body, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, ValidationError
from typing import List, Union, Dict, Optional