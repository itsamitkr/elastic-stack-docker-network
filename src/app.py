from flask import Flask, render_template, request
import requests
import json
from multiprocessing import Pool
from functools import partial

app = Flask(__name__)


@app.route("/")
def init():
    return render_template("index.html")


@app.route('/api/v1/about', methods=["GET"])
def about_view():
    return render_template("api-docs.html")


@app.route('/api/v1/index/<index_name>', methods=["GET", "POST"])
def index(index_name):
    print(index_name)
    try:
        if request.method == "GET":
            if ElasticClient.index_exists(index_name):
                return "Index Exists", 200
            else:
                return "Index not found", 204
    except Exception as e:
        return str(e), 400


@app.route('/api/v1/index/{index_name}/upload', methods=["PUT"])
def upload():
    return render_template("api-docs.html")


class ElasticClient:
    URL = 'http://elastic-search-service:9200'
    PARALLEL_PROCESSES = 50

    @staticmethod
    def index_exists(index_pattern: str) -> bool:
        resource_url = "{}/{}".format(ElasticClient.URL, index_pattern)
        response = requests.head(resource_url)
        try:

            return False if response.status_code == 404 else True
        except Exception as e:
            raise e

    @staticmethod
    def create_index(index_pattern: str, time_series=None):
        resource_url = "{}/{}".format(ElasticClient.URL, index_pattern)
        headers = {"Content-Type": "application/json"}
        config = {"settings": {"number_of_shards": "1", "number_of_replicas": "1"}}
        if time_series:
            config["mappings"] = {"properties": {"{}".format(time_series): {"type": "date"}}}

        try:
            response = requests.put(url=resource_url, headers=headers, data=json.dumps(config))
            return response
        except Exception as e:
            raise e

    @staticmethod
    def post_to_es(index_pattern: str, data: dict):
        resource_url = "{}/{}/{}/{}".format(ElasticClient.URL, index_pattern, "_doc", data.get(id))
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.put(url=resource_url, headers=headers, data=json.dumps(data))
            return response
        except Exception as e:
            raise e

    @staticmethod
    def bulk_post(index_pattern: str, index_id: str, data: list):
        pool = Pool(ElasticClient.PARALLEL_PROCESSES)
        try:
            pool.map(partial(ElasticClient.post_to_es, index_pattern=index_pattern, index_id=index_id), data)
            pool.close()
        except Exception as e:
            pool.terminate()
            raise e
        finally:
            pool.join()

    def __repr__(self):
        return "Elastic search class: {}".format(self.__dict__)

    def __str__(self):
        return "Elastic search class: {}".format(self.__dict__)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


