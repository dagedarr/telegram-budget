#!/bin/bash

celery -A tasks.mail_send:app flower