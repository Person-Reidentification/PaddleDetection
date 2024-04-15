import os
import uvicorn
import subprocess
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Define the FastAPI app
app = FastAPI()

# Define the route to execute the bash command
@app.post("/track")
def track(video_file: str):
    database_path = '/database'
    video_path = os.path.join(database_path, 'partition_videos', '_'.join(video_file.split('_')[:-1]) + '_total', video_file)
    command = f"python deploy/pipeline/pipeline.py --config deploy/pipeline/config/infer_cfg_pphuman.yml " \
              f"--video_file={video_path} --device=gpu"
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return JSONResponse({"output": result.stdout,
                             "error": result.stderr})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Run the FastAPI app with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8060)
