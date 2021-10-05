import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "routes.routes:app",
        reload=True,
        port=5000,
        host="0.0.0.0",
    )
