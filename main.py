from api.api_core import app
from mongo.mongo_data import mongo_data_main, mongo_start_data
from config_core import get_config, put_config

if get_config('MONGODB', 'create_collections') == 'True':
    mongo_data_main()
    put_config('MONGODB', 'create_collections', 'False')
if get_config('MONGODB', 'create_data') == 'True':
    mongo_start_data()
    put_config('MONGODB', 'create_data', 'False')

if __name__ == "__main__":
    import uvicorn
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)