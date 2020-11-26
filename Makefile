
CONTAINER_TAG=quay.io/reconmap/ws-server:latest

.PHONY: start
start:
	docker run -it --network=api-backend_default \
		-v $(PWD):/opt/reconmap/ws-server \
		-p 8765:8765 \
		--env-file env/dev.env \
		$(CONTAINER_TAG)	

.PHONY: build
build:
	docker build -t $(CONTAINER_TAG) .

.PHONY: push
push:
	docker push $(CONTAINER_TAG) 

