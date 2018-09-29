Build infos generator

To test it locally, execute:
```bash
docker run -v $(pwd):/work -ti habx/devops-build-infos
```

To use it with drone, add this line to the drone build file:
```yaml
  get-build-infos:
      image: habx/devops-build-infos
```
