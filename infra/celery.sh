#!/bin/bash

celery -A tasks.tasks:app worker --loglevel=INFO