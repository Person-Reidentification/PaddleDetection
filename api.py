import os
import subprocess
from fastapi import FastAPI

# Define the FastAPI app
app = FastAPI()

# Define the route to execute the bash command
@app.post("/track")
async def track(video_file: str):
    database_path = '/paddle'
    video_path = os.path.join(database_path, 'partition_videos', '_'.join(video_file.split('_')[:-1])+'_total', video_file)
    print(video_path)
    command = f"python deploy/pipeline/pipeline.py --config deploy/pipeline/config/infer_cfg_pphuman.yml " \
              f"--video_file={os.path.join(database_path, 'partition_videos', video_file)} --device=gpu"
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {"output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"error": str(e)}

# Run the FastAPI app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8060)
