#!/bin/bash

celery -A tasks.tasks:app flower