# Detectron2 Vertex-ai
How to deploy on vertex ai a custom model

### Requirements
* [Pyenv]: pyenv lets you easily switch between multiple versions of Python. It's simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well.
* [Poetry]: Poetry comes with all the tools you might need to manage your projects in a deterministic way.
* [gcloud]: The gcloud command-line interface is the primary CLI tool to create and manage Google Cloud resources.
* [poethepoet]: A task runner that works well with poetry.


## Runing on local
```bash
    # install poetry package
    poetry install 
    
    # runing poe task
    poe torch 
    poe detectron2 
 ```   
## Runing on local
```bash
    poetry run uvicorn src.main:app --reload
```

[Poetry]: https://python-poetry.org/
[gcloud]: https://cloud.google.com/sdk/gcloud/
[Pyenv]: https://github.com/pyenv/pyenv
[poethepoet]: https://github.com/nat-n/poethepoet
