ARG docker_image_tag
FROM ryechus/scavenger-wagtail:$docker_image_tag

COPY . /app/scavenger

WORKDIR /app/scavenger
