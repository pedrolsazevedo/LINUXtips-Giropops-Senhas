# LINUXtips-Giropops-Senhas


docker run -it --rm -v ${PWD}:/app --name python --hostname python-container python:3.9.20-bookworm bash

```shell
docker build . \
  -t psazevedo/linuxtips-giropops-senhas:1.1-distroless \
  --no-cache \
  -f Dockerfile.distroless
```
Links:  
[Docker hub](https://hub.docker.com/r/psazevedo/linuxtips-giropops-senhas)