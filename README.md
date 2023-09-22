# Sisyphus API Server

## Introduction

The `sisyphus-server` is the central API server that coordinates all of the activities from clients and is responsible for doling out the harshness (also known as jobs).  It also hosts all of the module-specific data so that modules can reference server-side data to make creating jobs and passing information easier.

## Quick Start

### Prerequisites

- `docker` installed

### Procedure

1. Navigate to the `docker` folder and run the following command.  This will start **Redis**, **MongoDB**, and **Mongo Express**.  It will also build the `sisyphus-server` container and get that running as well.  The `sisyphus-server` should be available on port `5000`.

   ```console
   $ docker compose up -d
   ```

# Architecture

## Endpoints

### Data

The `/data` routes are used for Sisyphus modules to push, pull, or delete data from the server.

| Route | Method | Description |
|---|:---:|---|
| `/data/{module}/{name}` | **GET** | Get information stored for `module` with the name `name` in the database. |
| `/data/{module}/{name}` | **POST** | Push JSON information for `module` with the name `name` into the database. |
| `/data/{module}/{name}` | **DELETE** | Delete JSON information for `module` with the name `name` into the database. |

### Jobs

The `/jobs` routes control job information for things that are currently in the queue.  Any jobs that have finished being processed by a given client/worker will not be accessible from this endpoint.

| Route | Method | Description |
|---|:---:|---|
| `/jobs/{job_id}` | **GET** | Get the job information for the job with job ID `job_id` |
| `/jobs/{job_id}` | **DELETE** | Delete the job with job ID `job_id` |
| `/jobs/{job_id}/completed` | **PATCH** | Change the status of the job with job ID `job_id`. Used post-processing to remove it from the queue to the proper **MongoDB** location via the `failed` option. |

### Queue

The `/queue` routes control queue operations to include posting jobs onto the queue, removing jobs from the queue, and other queue operations.

| Route | Method | Description |
|---|:---:|---|
| `/queue` | **GET** | Get all of the job information currently on the queue. Results are returned in queue order. |
| `/queue` | **POST** | Put a job onto the queue.  This will also add the job to the appropriate places and make it accessible via `/jobs` routes. |
| `/queue` | **DELETE** | Delete all of the jobs currently on the queue and their associated job data. |
| `/queue` | **PATCH** | This sets attributes on the queue.  For example, the `disabled` option set to `true` will disabled the queue globally. |
| `/queue/poll` | **GET** | Pull the next job off of the queue. |

### Status

The `/status` routes just return the current server config and a health check endpoint.

| Route | Method | Description |
|---|:---:|---|
| `/status/config` | **GET** | Returns the backend configuration for **Redis** and **MongoDB** along with server version and current uptime for the server. |
| `/status/health` | **GET** | Returns status code 200 if it's still running and accessible. |

### Workers

The `/workers` routes facilitates client heartbeat messaging, client statuses, and controlling per-worker attributes.

| Route | Method | Description |
|---|:---:|---|
| `/workers` | **GET** | Get all workers and their associated statuses. |
| `/workers/{worker_id}` | **GET** | Get a worker's status information via their worker UUID. |
| `/workers/{worker_id}` | **POST** | Push a worker's status into the database. |
| `/workers/{worker_id}` | **DELETE** | Delete a worker's status from the database. |
| `/workers/{worker_id}` | **PATCH** | This sets attributes on the worker.  For example, the `disabled` option set to `true` will disable the worker from pulling jobs from the queue. |

## Technologies

The main API server is written in **Flask** combined with the `flask-restx` plugin to help with Swagger documentation.  Since all of the documentation is applied as decorators around the various classes, it makes it easy to see where things are in code and where the inevitable mistake that I've made creeps up.

The job queue and worker status information is stored in **Redis** which makes things pretty easy to implement and pull from.  I prefer using `keydb`, but **Redis** proper will work just as well as there's nothing particularly complicated about the implementation.

All of the actual job information and module data is stored in **MongoDB**.  For the job collections, I'd recommend tossing an index on the `job_id` key, but other than that things should simply just work.  All of the `data` routes pull from **MongoDB**, and the `queue`/`job` routes do the same for their information.

## Settings

Below is a table of environment variables that can be set, what they do, and what their defaults are.

| Variable | Description |
|:--|:--|
| `REDIS_URI` | The URI for where **Redis** is configured.  Defaults to `redis://localhost:6379`. |
| `MONGO_URI` | The URI for where **MongoDB** is configured.  Defaults to `mongodb://root:root@localhost:27017` |
| `CLIENT_EXPIRY` | The number of seconds a worker/client lives in **Redis** before expiring.  The default is 30 seconds. |
| `REDIS_QUEUE_NAME` | The name of the queue in **Redis**.  This also determines where the attributes for the queue will be stored in **Redis** as well. Defaults to `queue`. |
| `MONGO_DATA_DB` | The database to store module data in **MongoDB**.  The default is `sisyphus_modules`. |
| `MONGO_DATA_COLL_PREFIX` | The prefix for the **MongoDB** collection to use on a per-module basis.  For example, if the `ffmpeg` module needs to store information, the collection it would use would be `data_ffmpeg` given `MONGO_DATA_COLL_PREFIX` is set to `data_`.  The default is `data_`. |
| `MONGO_JOB_DB` | The database to store job information in **MongoDB**. Defaults to `sisyphus_jobs`. |
| `MONGO_JOB_COLL_FAILED` | The collection to store failed jobs in **MongoDB**. Defaults to `failed`. |
| `MONGO_JOB_COLL_COMPLETED` | The collection to store completed jobs in **MongoDB**. Defaults to `completed`. |
| `MONGO_JOB_COLL_QUEUED` | The collection to store queued jobs in **MongoDB**. Defaults to `queued`. |
