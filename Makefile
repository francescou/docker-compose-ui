

build:
	git clone https://gitlab.pic.s1.p.fti.net/dfyarchicloud/docker-compose-ui-projects.git
	docker build -t sebmoule/docker-compose-ui .
	rm -rf docker-compose-ui-projects


rebase:
	git rebase francescou/master
