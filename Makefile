
.PHONY: start
start:
	docker run -it --network=api-backend_default \
		-v $(PWD):/opt/reconmap-job-processing-svc \
		-p 8765:8765 \
		--env-file env/dev.env \
		reconmap/job-processing-svc

.PHONY: prepare
prepare:
	docker build -t reconmap/job-processing-svc .

