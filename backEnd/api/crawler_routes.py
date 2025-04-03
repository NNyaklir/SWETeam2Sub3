from fastapi import APIRouter, Request, Query,HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from services.crawlerManager.content_crawler import crawl_site, load_urls_from_csv
from services.scanningManager.scan_service import ScanService
import tempfile
import shutil
import os
import json
from pathlib import Path

scan_service = ScanService()

router = APIRouter()

@router.post("/crawl")
async def start_crawl(url: str = Query(...), depth: int = Query(2)):
    crawled_data = await crawl_site(url, depth)

    urls = [entry['url'] for entry in crawled_data]

    return {
        "message": "Crawling completed",
        "urls_crawled": len(urls),
        "crawled_urls": urls
    }

@router.post("/treeCrawl")
async def crawl(
    project_id: str,
    target_url: str = Form(...),
    user_agent: str = Form(None),
    proxy: str = Form(None),
    delay: float = Form(0),
    dictionary: UploadFile = File(...)
):
    # project = project_service.get_project_by_id(project_id)
    # if not project:
    #     raise HTTPException(status_code=404, detail="Project not found")
    
    # Save the uploaded file to a temporary file
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(dictionary.file, tmp)
            tmp_path = tmp.name
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to process uploaded file: {str(e)}"})
    
    try:
        tree = scan_service.run_wfuzz(target_url, tmp_path, user_agent, proxy, delay)
        if tree:
            scan_service.save_tree_to_file(tree, project_id, target_url)
            return {"success": "Crawl Done Successfully"}
        else:
            return JSONResponse(status_code=500, content={"error": "Failed to run wfuzz or build tree."})
    finally:
        # Clean up the temporary file
        os.unlink(tmp_path)


# Need to fix
@router.post("/treeCrawl")
def list_project_outputs(project_id: str):
    """
    Lists all output folders for a given project ID.
    """
    base_path = Path("output") / project_id
    if not base_path.exists() or not base_path.is_dir():
        raise HTTPException(status_code=404, detail="Project not found or has no outputs.")
    
    folders = []
    for folder in base_path.iterdir():
        if folder.is_dir():
            folders.append({
                "host": folder.name,
                "path": str(folder),
                "tree_file": str(folder / "tree.json") if (folder / "tree.json").exists() else None
            })
    
    return JSONResponse(content={"project_id": project_id, "targets": folders})

@router.post("/projects/{project_id}/outputs/{host}/tree")
def get_tree_json(project_id: str, host: str):
    """
    Returns the contents of the tree.json file for a specific project and host.
    """
    tree_path = Path("output") / project_id / host / "tree.json"
    if not tree_path.exists():
        raise HTTPException(status_code=404, detail="Tree JSON not found.")
    
    try:
        with open(tree_path, "r") as f:
            tree_data = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")
    
    return JSONResponse(content=tree_data)