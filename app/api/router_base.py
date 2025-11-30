from fastapi import APIRouter


router_admin = APIRouter(prefix="/admin", tags=["Admin"])
router_auth = APIRouter(prefix="/auth", tags=["Auth"])
router_credit = APIRouter(prefix="/credit", tags=["Credit"])
router_health = APIRouter(prefix="/health", tags=["Health"])
router_video = APIRouter(prefix="/video", tags=["Video"])
router_runpod = APIRouter(prefix="/runpod", tags=["Runpod"])


routers = [router_admin, router_auth, router_credit, router_health, router_video, router_runpod]