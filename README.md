[![CI](https://github.com/mebaysan/donation-app/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/mebaysan/donation-app/actions/workflows/ci.yaml) [![CI](https://github.com/mebaysan/donation-app/actions/workflows/ci.yaml/badge.svg?branch=develop)](https://github.com/mebaysan/donation-app/actions/workflows/ci.yaml)

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Introducing the Donation App - Empowering Non-Profits](#introducing-the-donation-app---empowering-non-profits)
- [For Development](#for-development)
- [Backup](#backup)
- [Codebase Related Topic](#codebase-related-topic)
  - [Static \& Media Files for Production](#static--media-files-for-production)
  - [Custom Authentication Backend](#custom-authentication-backend)
  - [API Endpoints](#api-endpoints)
  - [Implemented Banks](#implemented-banks)
- [Development Environment](#development-environment)
  - [Run Project](#run-project)
  - [Test Project](#test-project)
- [Environment Variables](#environment-variables)
- [Docker](#docker)
- [Dummy Payment Request](#dummy-payment-request)
- [Caprover Nginx Configuration](#caprover-nginx-configuration)
  - [Backent Applicaton Static Files Config](#backent-applicaton-static-files-config)
  - [Frontend Application Config for Proxying](#frontend-application-config-for-proxying)


# Introducing the Donation App - Empowering Non-Profits

Welcome to the Donation App, a testament to the power of open-source collaboration. This project has its roots in a
dream – a dream of developing a Software as a Service (SaaS) solution tailor-made for non-profit organizations. However,
through interactions with various charitable entities, it became evident that many sought a more personalized approach.
Concerns over data privacy, varying donation volumes, and the desire for local financial autonomy led me to rethink my
approach. Thus, I embarked on a journey to create a versatile, multi-instance backend that empowers organizations to set
up their own donation infrastructure within their preferred systems, be it on a hybrid cloud, private cloud, or other
solutions. The result? A cost-effective and customizable platform that allows non-profits to receive donations directly
via local banks, reducing their reliance on third-party payment providers. I am excited to share this project with the
volunteers who are passionate to work for non-profits and invite you to explore, contribute, and make it even better.
Together, let's make a positive impact! Explore the code and contribute
on [GitHub](https://github.com/mebaysan/donation-app).

You can access the Docker image from [Docker Hub](https://hub.docker.com/r/mebaysan/donation-app).

![Donation App](./readme/wallpaper.png)
*Image above is example of one of the pre-built apps that are used this project. In the future, the frontend repository
will be open-source.

# For Development

You can use [dev-postgres.sh](scripts/dev-postgres.sh) to create a development database.

# Backup

You can use [backuper-db.sh](scripts/backuper-db.sh) to backup your database inside Docker container.

You can use [backuper-web.sh](scripts/backuper-web.sh) to backup your django data inside Docker container.

You can create a crontab by using the command below.

```
sudo crontab -e
```

# Codebase Related Topic

## Static & Media Files for Production

```bash
STATIC_URL = "/django-static/" # for proxy purposes

MEDIA_URL = "/django-media/" # for proxy purposes
```

## Custom Authentication Backend

For this app, **we can be logged in via username or phone_number**. Application
uses [`apps.management.authentication.JWTAuthentication`](./src/apps/management/authentication.py) class for rest
framework views.

To obtain a token, we use `/api/token/` endpoint. It uses [`ObtainTokenView`](./src/apps/management/api/views.py) view.

## API Endpoints

You can easily import Postman collection from [here](./postman/BaysanSoft-Donation-App.postman_collection.json).

Also you can check `/api/docs` endpoint for API documentation.


## Implemented Banks

- [x] [Kuveyt Türk](https://www.kuveytturk.com.tr/). You can see its provider under
  [`helpers.payment.providers`](./src/helpers/payment/providers.py#L202) module.

# Development Environment

## Run Project

To override the config variables, you can update the variables in [`src/.env.dev`](./src/.env.dev) file.

```bash
mv src/.env.dev src/.env # create .env file
make install # install the requirements
make create-devdb # create project dev db (you have to have Docker on your machine)
make migration # create the db
make load_countries_states # load country and state_provinces data
make superuser # create a super user 
make runserver # run the project
```

## Test Project

```bash
make install # install the requirements
make format # format the code
make lint # lint the code
make test # run the tests
```

# Environment Variables

You can check [`.env.dev`](./src/.env.dev) file to see the environment variables. All environment variables are have to
be provided in production environment.

# Docker

You can access the Docker image from [Docker Hub](https://hub.docker.com/r/mebaysan/donation-app).

```bash
docker image pull mebaysan/donation-app:latest # pull the latest image
docker image pull mebaysan/donation-app:develop # pull the develop image
```

# Dummy Payment Request

```python
new_dummy_response = HttpResponse(
            content=b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head runat="server">    <title></title></head><body onload="OnLoadEvent();">    <form name="downloadForm"        action="http://127.0.0.1:8000/api/payment/payment-fail/"        method="POST">         <input type="hidden"  name="AuthenticationResponse" value="%3c%3fxml+version%3d%221.0%22+encoding%3d%22utf-8%22%3f%3e%3cVPosTransactionResponseContract+xmlns%3axsd%3d%22http%3a%2f%2fwww.w3.org%2f2001%2fXMLSchema%22+xmlns%3axsi%3d%22http%3a%2f%2fwww.w3.org%2f2001%2fXMLSchema-instance%22%3e%3cIsEnrolled%3etrue%3c%2fIsEnrolled%3e%3cIsVirtual%3efalse%3c%2fIsVirtual%3e%3cResponseCode%3eCommonThreedControlsReturnedFail%3c%2fResponseCode%3e%3cResponseMessage%3e%c4%b0%c5%9flem+ger%c3%a7ekle%c5%9ftirilemedi.%3c%2fResponseMessage%3e%3cOrderId%3e0%3c%2fOrderId%3e%3cTransactionTime%3e0001-01-01T00%3a00%3a00%3c%2fTransactionTime%3e%3cMerchantOrderId%3edb926ff3-a12a-4a2c-88d5-7c15ce3c6494%3c%2fMerchantOrderId%3e%3cReferenceId%3e13144df6b8ad4bfb97c78236f1e610d9%3c%2fReferenceId%3e%3cMerchantId%3e57902%3c%2fMerchantId%3e%3cBusinessKey%3e0%3c%2fBusinessKey%3e%3c%2fVPosTransactionResponseContract%3e">        <!-- To support javascript unaware/disabled browsers -->        <noscript>    <center>Please click the submit button below.<br>    <input type="submit" name="submit" value="Submit"></center>  </noscript>    </form>    <script language="Javascript">         function OnLoadEvent() {document.downloadForm.submit();}   </script></body></html>',
            headers={"Content-Type": "text/html; charset=utf-8"},
            status=200,
        )
```

# Caprover Nginx Configuration


[Django Deployment on Caprover by Docker Image](https://medium.com/codex/django-deployment-on-caprover-by-docker-image-669e87ea81e7)

## Backent Applicaton Static Files Config

```nginx
<%
if (s.forceSsl) {
%>
    server {

        listen       80;

        server_name  <%-s.publicDomain%>;

        # Used by Lets Encrypt
        location /.well-known/acme-challenge/ {
            root <%-s.staticWebRoot%>;
        }

        # Used by CapRover for health check
        location /.well-known/captain-identifier {
            root <%-s.staticWebRoot%>;
        }

        location / {
            return 302 https://$http_host$request_uri;
        }
    }
<%
}
%>


server {

    <%
    if (!s.forceSsl) {
    %>
        listen       80;
    <%
    }
    if (s.hasSsl) {
    %>
        listen              443 ssl http2;
        ssl_certificate     <%-s.crtPath%>;
        ssl_certificate_key <%-s.keyPath%>;
    <%
    }
    %>

        client_max_body_size 500m;

        server_name  <%-s.publicDomain%>;

        # 127.0.0.11 is DNS set up by Docker, see:
        # https://docs.docker.com/engine/userguide/networking/configure-dns/
        # https://github.com/moby/moby/issues/20026
        resolver 127.0.0.11 valid=10s;
        # IMPORTANT!! If you are here from an old thread to set a custom port, you do not need to modify this port manually here!!
        # Simply change the Container HTTP Port from the dashboard HTTP panel
        set $upstream http://<%-s.localDomain%>:<%-s.containerHttpPort%>;

        location / {


	<%
	if (s.redirectToPath) {
	%>
	    return 302 <%-s.redirectToPath%>;
	<%
	} else {
	%>

		    <%
		    if (s.httpBasicAuthPath) {
		    %>
			    auth_basic           "Restricted Access";
			    auth_basic_user_file <%-s.httpBasicAuthPath%>; 
		    <%
		    }
		    %>

			    proxy_pass $upstream;
			    proxy_set_header Host $host;
			    proxy_set_header X-Real-IP $remote_addr;
			    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			    proxy_set_header X-Forwarded-Proto $scheme;

		    <%
		    if (s.websocketSupport) {
		    %>
			    proxy_set_header Upgrade $http_upgrade;
			    proxy_set_header Connection "upgrade";
			    proxy_http_version 1.1;
		    <%
		    }
		    %>
    
    
	<%
	}
	%>
	
        }

        # Used by Lets Encrypt
        location /.well-known/acme-challenge/ {
            root <%-s.staticWebRoot%>;
        }
        
        # Used by CapRover for health check
        location /.well-known/captain-identifier {
            root <%-s.staticWebRoot%>;
        }

        error_page 502 /captain_502_custom_error_page.html;
        location = /captain_502_custom_error_page.html {
                root <%-s.customErrorPagesDirectory%>;
                internal;
        }



        #BAYSAN ADDED
        location /django-static/ {
            alias /nginx-shared/YOUR-PATH-ON-HOST/static/;
         }

        location /django-media/ {
            alias /nginx-shared/YOUR-PATH-ON-HOST/media/;
        }
}
```

## Frontend Application Config for Proxying

```nginx
<%
if (s.forceSsl) {
%>
    server {

        listen       80;

        server_name  <%-s.publicDomain%>;

        # Used by Lets Encrypt
        location /.well-known/acme-challenge/ {
            root <%-s.staticWebRoot%>;
        }

        # Used by CapRover for health check
        location /.well-known/captain-identifier {
            root <%-s.staticWebRoot%>;
        }

        location / {
            return 302 https://$http_host$request_uri;
        }
    }
<%
}
%>


server {

    <%
    if (!s.forceSsl) {
    %>
        listen       80;
    <%
    }
    if (s.hasSsl) {
    %>
        listen              443 ssl http2;
        ssl_certificate     <%-s.crtPath%>;
        ssl_certificate_key <%-s.keyPath%>;
    <%
    }
    %>

        client_max_body_size 500m;

        server_name  <%-s.publicDomain%>;

        # 127.0.0.11 is DNS set up by Docker, see:
        # https://docs.docker.com/engine/userguide/networking/configure-dns/
        # https://github.com/moby/moby/issues/20026
        resolver 127.0.0.11 valid=10s;
        # IMPORTANT!! If you are here from an old thread to set a custom port, you do not need to modify this port manually here!!
        # Simply change the Container HTTP Port from the dashboard HTTP panel
        set $upstream http://<%-s.localDomain%>:<%-s.containerHttpPort%>;
        set $donation_be_upstream http://srv-captain--YOUR-BACKEND-SERVICE:8000; # # YOUR UPSTREAM SERVICE IN CAPROVER (BACKEND)

        location / {


	<%
	if (s.redirectToPath) {
	%>
	    return 302 <%-s.redirectToPath%>;
	<%
	} else {
	%>

		    <%
		    if (s.httpBasicAuthPath) {
		    %>
			    auth_basic           "Restricted Access";
			    auth_basic_user_file <%-s.httpBasicAuthPath%>; 
		    <%
		    }
		    %>

			    proxy_pass $upstream;
			    proxy_set_header Host $host;
			    proxy_set_header X-Real-IP $remote_addr;
			    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			    proxy_set_header X-Forwarded-Proto $scheme;

		    <%
		    if (s.websocketSupport) {
		    %>
			    proxy_set_header Upgrade $http_upgrade;
			    proxy_set_header Connection "upgrade";
			    proxy_http_version 1.1;
		    <%
		    }
		    %>
    
    
	<%
	}
	%>
	
        }

        # Used by Lets Encrypt
        location /.well-known/acme-challenge/ {
            root <%-s.staticWebRoot%>;
        }
        
        # Used by CapRover for health check
        location /.well-known/captain-identifier {
            root <%-s.staticWebRoot%>;
        }

        error_page 502 /captain_502_custom_error_page.html;
        location = /captain_502_custom_error_page.html {
                root <%-s.customErrorPagesDirectory%>;
                internal;
        }

   #BAYSAN
    location /django-static/ {
            alias /nginx-shared/YOUR-PATH-ON-HOST/static/; # YOUR SHARED FILES OF BACKEND PROJECT'S STATIC
         }

        location /django-media/ {
            alias /nginx-shared/YOUR-PATH-ON-HOST/media/;
        }

   # Django App
    location /cockpit {
        proxy_pass $donation_be_upstream; # YOUR UPSTREAM SERVICE IN CAPROVER (BACKEND)
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /api {
        proxy_pass $donation_be_upstream; # YOUR UPSTREAM SERVICE IN CAPROVER (BACKEND)
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

}
```