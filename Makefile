
.PHONY: start
start:
	docker run -it --network=api-backend_default \
		-v $(PWD):/opt/reconmap-job-processing-svc \
		-p 8765:8765 \
		--env-file env/dev.env \
		reconmap/job-processing-svc:dev

.PHONY: build-dev
build-dev:
	docker build -t reconmap/job-processing-svc:dev .

.PHONY: push-dev
push-dev:
	docker push reconmap/job-processing-svc:dev

