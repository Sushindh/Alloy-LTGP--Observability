from flask import Flask, request, jsonify
import logging

from opentelemetry import metrics, trace
from opentelemetry.sdk.resources import Resource,SERVICE_NAME
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.semconv.resource import ResourceAttributes
#Name
resource = Resource.create({ResourceAttributes.SERVICE_NAME:"flask-otel-app","deployment.environment":"dev","host.name":"flask-container","job": "flask-app"})

#Initialize Opentelemetry SDK

#Metrics

# resource = Resource(attributes={SERVICE_NAME: "flask-app"})
exporter = OTLPMetricExporter(endpoint="otel-collector:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

#Metrics instruments
compute_request_count = meter.create_counter(
    name='app_compute_request_count',
    description='Counts the requests to compute-service',
    unit='1'
)

#Tracing
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
span_exporter = OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(span_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

#Logs
logger_provider = LoggerProvider(resource=resource)
log_exporter = OTLPLogExporter(endpoint="otel-collector:4317",insecure=True)
log_processor = BatchLogRecordProcessor(log_exporter)
logger_provider.add_log_record_processor(log_processor)
handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route('/home')
def home():
    compute_request_count.add(1, {"endpoint": "/home"})
    logger.info("Home endpoint Hi", extra={
    "service.name": "flask-otel-app",
    "deployment.environment": "dev",
    "host.name": "flask-container",
    "job": "flask-app"
})
    return "Home"

@app.route('/cart')
def cart():
    compute_request_count.add(1, {"endpoint": "/cart"})
    logger.info("Home endpoint Hi", extra={
    "service.name": "flask-otel-app",
    "deployment.environment": "dev",
    "host.name": "flask-container",
    "job": "flask-app"
})
    return "Cart"

@app.route('/payment')
def payment():
    compute_request_count.add(1, {"endpoint": "/payment"})
    logger.info("Home endpoint Hi", extra={
    "service.name": "flask-otel-app",
    "deployment.environment": "dev",
    "host.name": "flask-container",
    "job": "flask-app"
})
    return "Payment"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)