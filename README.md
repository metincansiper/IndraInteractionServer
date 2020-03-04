# IndraInteractionServer

## Installing the Dependencies

- Download [Bioagents](https://github.com/sorgerlab/bioagents) and add it to the PYTHONPATH.
- Download [Bionetgen](https://www.csb.pitt.edu/Faculty/Faeder/?page_id=409) add add it to the PYTHONPATH.
- Set envrionment variables ``INDRA_DB_REST_URL`` and ``INDRA_DB_REST_API_KEY``as it is mentioned [here](https://indra.readthedocs.io/en/latest/modules/sources/indra_db_rest/#module-indra.sources.indra_db_rest).
- Run ``pip3 install requirements.txt``.

## Configuration

The configurations can be made by using the following environment variables:

- `HOST` : the host where the server will be running, the default value is `127.0.0.1`.
- `PORT` : the port where the server will be running, the default value is `8000`.
- `INDRA_GROUND_URL`: the url to query grounding of entities through INDRA, the default value is `http://grounding.indra.bio/ground`

## Running the Server
```
cd indra_intn_server
python3 server.py
```

## DOCKER
```
docker build --build-arg indra_db_api_key=<YOUR_INDRA_DB_API_KEY> -f Dockerfile -t indra_intn_server .
docker run -d -it -p <port>:8000 indra_intn_server
```

## Query Format

The server accepts the following get parameters:

- `source`: the name of source entity. There must be one source parameter for the directed interactions while there must be 2 of them for the undirected interactions.
- `target`: the name of target entity for the directed interactions.
- `sign`: represents how the source affects the target for the directed interactions. `N` represents a negative effect while `P` represents a positive effect.

## Example Query

Assuming that the host is `localhost` and the port is `8000`:

- localhost:8000/find-interactions?source=MDM2&target=EGFR&sign=N
- localhost:8000/find-interactions?source=MDM2&source=EGFR
