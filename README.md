# Build infos generator

## Goals
Provide a simple and clear way for software to identify their version at build time (and preferably report it at runtime themselves).

## What is it doing
### Versioning logic
- If you're on a tag, the version will be the tag name
- Otherwise, the version will be a long named version

### Limitations
It's currently dependant on a `package.json` to make some checks. This limitation could be easily removed.

### Generated files
This generate two files:

- `build.json` looking like this:
```json
{
    "version": "1.17.0-20180923-2004-174e781-test-sentry-cli",
    "git_hash": "174e781",
    "git_date": "20180923-2004",
    "git_branch": "test/sentry-cli",
    "build_date": "2018-09-29T21:42:11.091593"
}
```

- `version.txt` looking like this:
```
1.17.0-20180923-2004-174e781-test-sentry-cli
```

## Using it
To test it locally, execute:
```bash
docker run -v $(pwd):/work -ti habx/devops-build-infos
```

To use it with drone, add this line to the drone build file:
```yaml
  get-build-infos:
      image: habx/devops-build-infos
```
