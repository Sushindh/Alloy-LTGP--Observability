from flask import Flask
import logging

from opentelemetry import metrics, trace
from opentelemetry.sdk.resources import Resource
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

# Resource definition
resource = Resource.create({
    ResourceAttributes.SERVICE_NAME: "flask-otel-app",
    "deployment.environment": "dev"
})

# Metrics
metric_exporter = OTLPMetricExporter(endpoint="alloy:4317", insecure=True)
metric_reader = PeriodicExportingMetricReader(metric_exporter)
metrics_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(metrics_provider)
meter = metrics.get_meter(__name__)
compute_request_count = meter.create_counter(
    name="app_compute_request_count",
    description="Counts the requests",
    unit="1"
)

# Tracing
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
trace_exporter = OTLPSpanExporter(endpoint="alloy:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(trace_exporter))

# Logging
logger_provider = LoggerProvider(resource=resource)
log_exporter = OTLPLogExporter(endpoint="alloy:4317", insecure=True)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
logging_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.basicConfig(level=logging.INFO, handlers=[logging_handler])
logger = logging.getLogger("myapp")

# Flask app
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Test log
logger.info("Startup complete.")

@app.route("/home")
def home():
    compute_request_count.add(1, {"endpoint": "/home"})
    logger.info("Home endpoint hit")
    return "Home"

@app.route("/cart")
def cart():
    compute_request_count.add(2, {"endpoint": "/cart"})
    logger.info("Cart endpoint hit")
    return "Cart"

@app.route("/payment")
def payment():
    compute_request_count.add(3, {"endpoint": "/payment"})
    logger.info("Payment endpoint hit")
    return "Payment"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
