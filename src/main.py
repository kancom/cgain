import os
import sys
from typing import List, Optional

import dotenv
import uvicorn
from fastapi import FastAPI

import cgain.restapi.api as api_pkg
import cgain.restapi.api_main as api
from cgain.deps import Container


def main(argv: Optional[List[str]]):
    config_path = os.environ.get(
        "CONFIG_PATH",
        os.path.join(os.path.dirname(__file__), os.pardir, ".env"),
    )
    dotenv.load_dotenv(config_path)
    container = Container()
    container.config.api_key.from_env("CG_API_KEY")
    container.config.secret_key.from_env("CG_SECRET_KEY")
    container.wire(packages=[api_pkg])
    pfx = os.environ.get("API_PREFIX", "")
    api_url = pfx + os.environ.get("API_V1_STR", "")

    app = FastAPI(
        title=os.environ.get("PROJECT_NAME", "CGAIN test"),
        openapi_url=f"{api_url}/openapi.json",
        docs_url=f"{pfx}/docs",
    )
    app.include_router(api.api_router, prefix=api_url)
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("REST_PORT", 8000))


if __name__ == "__main__":
    main(sys.argv[1:])
